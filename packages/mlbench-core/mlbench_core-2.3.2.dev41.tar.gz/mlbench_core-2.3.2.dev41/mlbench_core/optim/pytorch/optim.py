from mlbench_core.utils.pytorch.distributed import AllReduceAggregation
from mlbench_core.utils.pytorch.distributed import DecentralizedAggregation

import numpy as np
import torch
import torch.distributed as dist
from torch.optim import SGD, Adam
from torch.optim.optimizer import Optimizer, required


class SparsifiedSGD(Optimizer):
    r"""Implements sparsified version of stochastic gradient descent.

    Args:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float): learning rate
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        sparse_grad_size (int): Size of the sparsified gradients vector (default: 10).

    """

    def __init__(self, params, lr=required, weight_decay=0, sparse_grad_size=10):

        if lr is not required and lr < 0.0:
            raise ValueError("Invalid learning rate: {}".format(lr))
        if weight_decay < 0.0:
            raise ValueError("Invalid weight_decay value: {}".format(weight_decay))

        defaults = dict(lr=lr, weight_decay=weight_decay)

        super(SparsifiedSGD, self).__init__(params, defaults)

        self.__create_gradients_memory()
        self.__create_weighted_average_params()

        self.num_coordinates = sparse_grad_size

    def __create_weighted_average_params(self):
        r""" Create a memory to keep the weighted average of parameters in each iteration """
        for group in self.param_groups:
            for p in group["params"]:
                param_state = self.state[p]
                param_state["estimated_w"] = torch.zeros_like(p.data)
                p.data.normal_(0, 0.01)
                param_state["estimated_w"].copy_(p.data)

    def __create_gradients_memory(self):
        r""" Create a memory to keep gradients that are not used in each iteration """
        for group in self.param_groups:
            for p in group["params"]:
                param_state = self.state[p]
                param_state["memory"] = torch.zeros_like(p.data)

    def step(self, closure=None):
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:

            weight_decay = group["weight_decay"]

            for p in group["params"]:

                if p.grad is None:
                    continue
                d_p = p.grad.data

                if weight_decay != 0:
                    d_p.add_(weight_decay, p.data)
                p.data.add_(-d_p)

        return loss

    def sparsify_gradients(self, param, lr):
        """ Calls one of the sparsification functions (random or blockwise)

        Args:
            random_sparse (bool): Indicates the way we want to make the gradients sparse
                (random or blockwise) (default: False)
            param (:obj: `torch.nn.Parameter`): Model parameter
        """
        if self.random_sparse:
            return self._random_sparsify(param, lr)
        else:
            return self._block_sparsify(param, lr)

    def _random_sparsify(self, param, lr):
        """ Sparsify the gradients vector by selecting 'k' of them randomly.

        Args:
            param (:obj: `torch.nn.Parameter`): Model parameter
            lr (float): Learning rate

        """

        self.state[param]["memory"] += param.grad.data * lr

        indices = np.random.choice(
            param.data.size()[1], self.num_coordinates, replace=False
        )
        sparse_tensor = torch.zeros(2, self.num_coordinates)

        for i, random_index in enumerate(indices):
            sparse_tensor[1, i] = self.state[param]["memory"][0, random_index]
            self.state[param]["memory"][0, random_index] = 0
        sparse_tensor[0, :] = torch.tensor(indices)

        return sparse_tensor

    def _block_sparsify(self, param, lr):
        """ Sparsify the gradients vector by selecting a block of them.

        Args:
            param (:obj: `torch.nn.Parameter`): Model parameter
            lr (float): Learning rate
        """

        self.state[param]["memory"] += param.grad.data * lr

        num_block = int(param.data.size()[1] / self.num_coordinates)

        current_block = np.random.randint(0, num_block)
        begin_index = current_block * self.num_coordinates

        end_index = begin_index + self.num_coordinates - 1
        output_size = 1 + end_index - begin_index + 1

        sparse_tensor = torch.zeros(1, output_size)
        sparse_tensor[0, 0] = begin_index
        sparse_tensor[0, 1:] = self.state[param]["memory"][
            0, begin_index : end_index + 1
        ]
        self.state[param]["memory"][0, begin_index : end_index + 1] = 0

        return sparse_tensor

    def update_estimated_weights(self, iteration, sparse_vector_size):
        """ Updates the estimated parameters

        Args:
            iteration (int): Current global iteration
            sparse_vector_size (int): Size of the sparse gradients vector
        """
        t = iteration
        for group in self.param_groups:
            for param in group["params"]:
                tau = param.data.size()[1] / sparse_vector_size
                rho = (
                    6
                    * ((t + tau) ** 2)
                    / ((1 + t) * (6 * (tau ** 2) + t + 6 * tau * t + 2 * (t ** 2)))
                )
                self.state[param]["estimated_w"] = (
                    self.state[param]["estimated_w"] * (1 - rho) + param.data * rho
                )

    def get_estimated_weights(self):
        """ Returns the weighted average parameter tensor """
        estimated_params = []
        for group in self.param_groups:
            for param in group["params"]:
                estimated_params.append(self.state[param]["estimated_w"])
        return estimated_params


class CentralizedSparsifiedSGD(SparsifiedSGD):
    r"""Implements centralized sparsified version of stochastic gradient descent.

    Args:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float): Learning rate
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        sparse_grad_size (int): Size of the sparsified gradients vector (default: 10)
        random_sparse (bool): Whether select random sparsification (default: `False`)
        average_models (bool): Whether to average models together (default: `True`)

    """

    def __init__(
        self,
        params,
        lr=required,
        weight_decay=0,
        sparse_grad_size=10,
        random_sparse=False,
        average_models=True,
    ):
        self.average_models = average_models
        self.world_size = dist.get_world_size()
        self.random_sparse = random_sparse
        super(CentralizedSparsifiedSGD, self).__init__(
            params, lr, weight_decay, sparse_grad_size
        )

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

            Arguments:
                closure (callable, optional): A closure that reevaluates the model and returns the loss.
        """

        loss = None

        if closure is not None:
            loss = closure()

        for group in self.param_groups:

            weight_decay = group["weight_decay"]
            lr = group["lr"]

            for p in group["params"]:
                # Sparsify the gradients
                sparse_tensor = self.sparsify_gradients(p, lr)
                # Aggregate the gradients
                gathered_list = [
                    torch.zeros_like(sparse_tensor) for _ in range(self.world_size)
                ]
                dist.all_gather(gathered_list, sparse_tensor)
                p.grad.data = torch.zeros_like(p.grad.data)

                if self.random_sparse:
                    for grad_tensor in gathered_list:
                        for index in range(grad_tensor.size()[1]):
                            p.grad.data[0, int(grad_tensor[0, index])] += grad_tensor[
                                1, index
                            ]
                else:
                    for grad_tensor in gathered_list:
                        tensor_size = grad_tensor.size()[1]
                        begin = int(grad_tensor[0, 0])
                        p.grad.data[
                            0, begin : (begin + tensor_size - 1)
                        ] += grad_tensor[0, 1:]

                if self.average_models:
                    p.grad.data /= self.world_size

                if p.grad is None:
                    continue
                d_p = p.grad.data

                if weight_decay != 0:
                    d_p.add_(weight_decay, p.data)
                p.data.add_(-d_p)

        return loss


class DecentralizedSGD(SGD):
    r"""Implements decentralized stochastic gradient descent (optionally with momentum).

    Args:
        rank (int): rank of current process in the network
        neighbors (list): list of ranks of the neighbors of current process
        model (:obj:`nn.Module`): model which contains parameters for SGD
        lr (float): learning rate
        momentum (float, optional): momentum factor (default: 0)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        dampening (float, optional): dampening for momentum (default: 0)
        nesterov (bool, optional): enables Nesterov momentum (default: False)
        average_models (bool): Whether to average models together. (default: `True`)

    """

    def __init__(
        self,
        rank,
        neighbors,
        model,
        lr=required,
        momentum=0,
        dampening=0,
        weight_decay=0,
        nesterov=False,
        average_models=True,
    ):
        super(DecentralizedSGD, self).__init__(
            model.parameters(), lr, momentum, dampening, weight_decay, nesterov
        )

        if average_models:
            self.agg_mode = "avg"
        else:
            raise NotImplementedError("Only average model is supported right now.")

        self.model = model
        self.agg = DecentralizedAggregation(rank, neighbors).agg_model

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = super(DecentralizedSGD, self).step(closure=closure)
        # Averaging the model after updating the gradient separately.
        self.agg(self.model, self.agg_mode)
        return loss


class CentralizedSGD(SGD):
    r"""Implements centralized stochastic gradient descent (optionally with momentum).

    Args:
        world_size (int): Size of the network
        model (:obj:`nn.Module`): Model which contains parameters for SGD
        lr (float): learning rate
        momentum (float, optional): momentum factor (default: 0)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        dampening (float, optional): dampening for momentum (default: 0)
        nesterov (bool, optional): enables Nesterov momentum (default: False)
        average_models (bool): Whether to average models together. (default: `True`)

    """

    def __init__(
        self,
        world_size,
        model,
        lr=required,
        momentum=0,
        dampening=0,
        weight_decay=0,
        nesterov=False,
        average_models=True,
    ):
        super(CentralizedSGD, self).__init__(
            model.parameters(), lr, momentum, dampening, weight_decay, nesterov
        )
        if average_models:
            self.agg_mode = "avg"
        else:
            raise NotImplementedError("Only average model is supported right now.")

        self.model = model
        self.agg = AllReduceAggregation(world_size=world_size).agg_grad

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        self.agg(self.model, self.agg_mode)
        loss = super(CentralizedSGD, self).step(closure=closure)
        return loss


class SignSGD(SGD):
    r"""Implements sign stochastic gradient descent (optionally with momentum).

    Args:
        params (iterable): iterable of parameters to optimize or dicts defining
            parameter groups
        lr (float): learning rate
        momentum (float, optional): momentum factor (default: 0)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        dampening (float, optional): dampening for momentum (default: 0)
        nesterov (bool, optional): enables Nesterov momentum (default: False)
        average_models (bool): Whether to average models together. (default: `True`)

    """

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            weight_decay = group["weight_decay"]
            momentum = group["momentum"]
            dampening = group["dampening"]
            nesterov = group["nesterov"]

            for p in group["params"]:
                if p.grad is None:
                    continue
                d_p = p.grad.data
                if weight_decay != 0:
                    d_p.add_(weight_decay, p.data)
                if momentum != 0:
                    param_state = self.state[p]
                    if "momentum_buffer" not in param_state:
                        buf = param_state["momentum_buffer"] = torch.zeros_like(p.data)
                        buf.mul_(momentum).add_(d_p)
                    else:
                        buf = param_state["momentum_buffer"]
                        buf.mul_(momentum).add_(1 - dampening, d_p)
                    if nesterov:
                        d_p = d_p.add(momentum, buf)
                    else:
                        d_p = buf

                # Update with the sign
                p.data.add_(-group["lr"], torch.sign(d_p))

        return loss


class CentralizedAdam(Adam):
    r"""Implements centralized Adam algorithm.

    Args:
        world_size (int): Size of the network
        model (:obj:`nn.Module`): Model which contains parameters for Adam
        lr (float, optional): learning rate (default: 1e-3)
        betas (Tuple[float, float], optional): coefficients used for computing
            running averages of gradient and its square (default: (0.9, 0.999))
        eps (float, optional): term added to the denominator to improve
            numerical stability (default: 1e-8)
        weight_decay (float, optional): weight decay (L2 penalty) (default: 0)
        amsgrad (boolean, optional): whether to use the AMSGrad variant of this
            algorithm from the paper `On the Convergence of Adam and Beyond`_
            (default: False)
        average_models (bool): Whether to average models together. (default: `True`)

    """

    def __init__(
        self,
        world_size,
        model,
        lr=1e-3,
        betas=(0.9, 0.999),
        eps=1e-8,
        weight_decay=0,
        amsgrad=False,
        average_models=True,
    ):
        super(CentralizedAdam, self).__init__(
            model.parameters(), lr, betas, eps, weight_decay, amsgrad
        )
        if average_models:
            self.agg_mode = "avg"
        else:
            raise NotImplementedError("Only average model is supported right now.")

        self.model = model
        self.agg = AllReduceAggregation(world_size=world_size).agg_grad

    def step(self, closure=None):
        """ Aggregates the gradients and performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        self.agg(self.model, self.agg_mode)
        loss = super(CentralizedAdam, self).step(closure=closure)
        return loss


class PowerSGD(Optimizer):
    def __init__(
        self,
        model,
        lr=0.1,
        weight_decay=0,
        momentum=0,
        nesterov=False,
        reuse_query=False,
        rank=1,
    ):
        self.n_workers = dist.get_world_size()

        if lr is not required and lr < 0.0:
            raise ValueError("Invalid learning rate: {}".format(lr))
        if weight_decay < 0.0:
            raise ValueError("Invalid weight_decay value: {}".format(weight_decay))

        self.rank = rank
        self.p_memory = None
        self.q_memory = None
        self.reuse_query = reuse_query
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        defaults = dict(lr=lr, weight_decay=weight_decay, momentum=momentum, nesterov=nesterov)

        super(PowerSGD, self).__init__(model.parameters(), defaults)

        self.__create_gradients_memory_and_buffers()

    def __create_gradients_memory_and_buffers(self):
        self.memories = []
        self.send_buffers = []
        for group in self.param_groups:
            for p in group["params"]:
                self.memories.append(torch.zeros_like(p.data))
                self.send_buffers.append(torch.zeros_like(p.data))

    def set_random(self, vector):
        torch.manual_seed(self.rng.randint(1_000_000_000))
        vector.data[:] = torch.randn(*vector.shape, device=self.device)
        # orthogonalize(vector)

    def step(self, closure=None):
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        grads = []

        # collect gradients in 'grads'
        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                grads.append(p.grad.data)

        # accumulate
        for grad, memory, send_bfr in zip(grads, self.memories, self.send_buffers):
            send_bfr.data[:] = grad + memory

        # set 'grads' to the averaged value from the workers
        self.reduce(self.send_buffers, grads, self.memories)

        # update parameters
        i = 0
        for group in self.param_groups:
            weight_decay = group['weight_decay']
            momentum = group['momentum']
            dampening = group['dampening']
            nesterov = group['nesterov']

            for p in group['params']:
                if p.grad is None:
                    continue
                d_p = grads[i]
                i += 1
                if weight_decay != 0:
                    d_p.add_(weight_decay, p.data)
                if momentum != 0:
                    param_state = self.state[p]
                    if 'momentum_buffer' not in param_state:
                        buf = param_state['momentum_buffer'] = torch.clone(d_p).detach()
                    else:
                        buf = param_state['momentum_buffer']
                        buf.mul_(momentum).add_(1 - dampening, d_p)
                    if nesterov:
                        d_p = d_p.add(momentum, buf)
                    else:
                        d_p = buf

                p.data.add_(-group['lr'], d_p)

        return loss

    def reduce(self, grad_in, grad_out, memory_out):
        # Split the tensors into rank1-ones that will be reduced un-compressed
        # and rank > 1 tensors that are compressed
        rank1_tensors = [
            (tensor, out, mem)
            for tensor, out, mem in zip(grad_in, grad_out, memory_out)
            if tensor.ndimension() <= 1
        ]
        high_rank_tensors = [
            (tensor, out, mem)
            for tensor, out, mem in zip(grad_in, grad_out, memory_out)
            if tensor.ndimension() > 1
        ]

        # We are building a rank-1 approximation of every tensor
        # that can be interpreted as a matrix. Let the approximation be
        # M = p q^T
        # We are allocating consequtive memory for the p's and q's

        memory_is_uninitialized = self.p_memory is None

        p_total_size = 0
        q_total_size = 0
        for tensor, _, _ in high_rank_tensors:
            matrix = tensor.view(tensor.shape[0], -1)
            n, m = matrix.shape
            rank = min(n, m, self.rank)
            p_total_size += n * rank
            q_total_size += m * rank
        if self.p_memory is None:
            self.p_memory = torch.empty(p_total_size, device=self.device)
            self.q_memory = torch.empty(q_total_size, device=self.device)

        # Find them again and make lists of pointers
        ps = []
        qs = []
        p_idx = 0
        q_idx = 0
        for tensor, _, _ in high_rank_tensors:
            matrix = tensor.view(tensor.shape[0], -1)
            n, m = matrix.shape
            rank = min(n, m, self.rank)
            ps.append(self.p_memory[p_idx: p_idx + n * rank].view(n, rank))
            qs.append(self.q_memory[q_idx: q_idx + m * rank].view(m, rank))
            p_idx += n * rank
            q_idx += m * rank

        for (tensor, _, _), q, p in zip(high_rank_tensors, qs, ps):
            matrix = tensor.view(tensor.shape[0], -1)
            n, m = matrix.shape

            if self.reuse_query and not memory_is_uninitialized:
                # orthogonalize(q)
                pass
            else:
                # Sample a query vector q
                self.set_random(q)

        for (tensor, _, _), q, p in zip(high_rank_tensors, qs, ps):
            matrix = tensor.view(tensor.shape[0], -1)
            torch.matmul(matrix, q, out=p)

        all_reduce(self.p_memory)

        # Start communicating rank 1 tensors
        rank1_tensor_list = TensorBuffer([tensor for (tensor, _, _) in rank1_tensors])

        rank1_handle = rank1_tensor_list.all_reduce(async_op=True)

        for p in ps:
            orthogonalize(p)

        for p, q, (tensor, _, _) in zip(ps, qs, high_rank_tensors):
            matrix = tensor.view(tensor.shape[0], -1)
            torch.matmul(matrix.t(), p, out=q)

        all_reduce(self.q_memory)
        self.q_memory.data[:] /= self.n_workers

        for p, q, (tensor, out, mem) in zip(ps, qs, high_rank_tensors):
            # Set the output gradient
            torch.matmul(p, q.t(), out=out.data[:])
            mem.data[:] = tensor - out

        rank1_handle.wait()
        rank1_tensor_list.buffer /= self.n_workers
        rank1_tensor_list.unpack([out for (_, out, _) in rank1_tensors])


class TensorBuffer:
    """
    Packs multiple tensors into one flat buffer for efficient
    intra-worker communication.
    """

    def __init__(self, tensors):
        indices = [0]
        for tensor in tensors:
            new_end = indices[-1] + tensor.nelement()
            indices.append(new_end)

        self._start_idx = indices[:-1]
        self._end_idx = indices[1:]
        self._tensors = tensors

        self.buffer = torch.cat([t.view(-1) for t in tensors])  # copies

    def __getitem__(self, index):
        return self.buffer[self._start_idx[index]: self._end_idx[index]].view(*self._tensors[index].shape)

    def __len__(self):
        return len(self._tensors)

    def pack(self, tensors=None):
        # Optional. init already does this.
        if tensors is None:
            tensors = self._tensors
        for tensor, entry in zip(tensors, self):
            entry[:] = tensor

    def unpack(self, tensors):
        for tensor, entry in zip(tensors, self):
            tensor[:] = entry

    def nelement(self):
        return self.buffer.nelement()

    def element_size(self):
        return self.buffer.element_size()

    def bits(self):
        return 8 * self.nelement() * self.element_size()

    def all_reduce(self, async_op=False):
        return torch.distributed.all_reduce(self.buffer, async_op=async_op)

    def all_gather(self, async_op=False):
        n_workers = torch.distributed.get_world_size() if torch.distributed.is_available() else 1
        buffers = [torch.empty_like(self.buffer) for i in range(n_workers)]
        handle = all_gather(buffers, self.buffer, async_op=async_op)
        if async_op:
            return buffers, handle
        else:
            return buffers


def all_reduce(*args, **kwargs):
    if torch.distributed.is_available() and torch.distributed.get_world_size() > 1:
        return torch.distributed.all_reduce(*args, **kwargs)


@torch.jit.script
def orthogonalize(matrix):
    n, m = matrix.shape
    for i in range(m):
        # Normalize the i'th column
        col = matrix[:, i : i + 1]
        col /= torch.sqrt(torch.sum(col ** 2))
        # Project it on the rest and remove it
        if i + 1 < m:
            rest = matrix[:, i + 1 :]
            # rest -= torch.matmul(col.t(), rest) * col
            rest -= torch.sum(col * rest, dim=0) * col


def all_gather(out_list, in_tensor, **kwargs):
    if torch.distributed.is_available() and torch.distributed.get_world_size() > 1:
        return torch.distributed.all_gather(out_list, in_tensor, **kwargs)
    else:
        assert len(out_list) == 1
        out_list[0].data = in_tensor

