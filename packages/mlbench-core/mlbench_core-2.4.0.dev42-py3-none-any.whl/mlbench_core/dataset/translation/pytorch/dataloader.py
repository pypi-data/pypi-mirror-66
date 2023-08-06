import os

from mlbench_core.dataset.translation.pytorch import config
from mlbench_core.dataset.translation.pytorch.tokenizer import WMT14Tokenizer
from torchtext.data import Example, Dataset
from mlbench_core.dataset.util.tools import maybe_download_and_extract_tar_gz
import torch
from torch.utils.data import DataLoader


def _construct_filter_pred(min_len, max_len):
    """
    Constructs a filter predicate
    Args:
        min_len (int): Min sentence length
        max_len (int): Max sentence length

    Returns:
        func
    """
    filter_pred = lambda x: not (x[0] < min_len or x[1] < min_len)
    if max_len is not None:
        filter_pred = lambda x: not (
                x[0] < min_len or x[0] > max_len or x[1] < min_len or x[1] > max_len
        )

    return filter_pred


def process_data(path, filter_pred, fields, lazy=False, max_size=None):
    """Loads data from given path and processes the lines

    Args:
        path (str): Dataset directory path
        filter_pred (func): Filter predicate function (to filter inputs)
        fields (list): SRC and TRG fields
        lazy (bool): Whether to load the dataset in lazy mode
        max_size (int | None): Maximum size of dataset

    Returns:
        List: The list of examples
    """
    src_path, trg_path = tuple(os.path.expanduser(path + x) for x in config.EXTS)
    examples = []
    with open(src_path, mode="r", encoding="utf-8") as src_file, open(
            trg_path, mode="r", encoding="utf-8"
    ) as trg_file:
        for src_line, trg_line in zip(src_file, trg_file):
            src_line, trg_line = src_line.strip(), trg_line.strip()

            should_consider = filter_pred(
                (src_line.count(" ") + 1, trg_line.count(" ") + 1)
            )
            if src_line != "" and trg_line != "" and should_consider:
                if lazy:
                    examples.append((src_line, trg_line))
                else:
                    examples.append(Example.fromlist([src_line, trg_line], fields))

            if max_size and len(examples) >= max_size:
                break
    return examples


def build_collate_fn(src_tok, trg_tok, batch_first, sort):
    def collate_seq(seq, tok):
        """
        Builds batches for training or inference.
        Batches are returned as pytorch tensors, with padding.

        :param seq: list of sequences
        """
        lengths = torch.tensor([len(s) + 2 for s in seq], dtype=torch.int64)
        batch_length = max(lengths) + 2

        shape = (len(seq), batch_length)
        seq_tensor = torch.full(shape, config.PAD, dtype=torch.int64)

        for i, s in enumerate(seq):
            end_seq = lengths[i]
            segmented = torch.Tensor(tok.segment(s[:end_seq]))
            seq_tensor[i, :end_seq].copy_(segmented)

        if not batch_first:
            seq_tensor = seq_tensor.t()

        return seq_tensor, lengths

    def parallel_collate(seqs):
        """
        Builds batches from parallel dataset (src, tgt), optionally sorts batch
        by src sequence length.

        :param seqs: tuple of (src, tgt) sequences
        """
        src_seqs, trg_seqs = zip(*[(x.src, x.trg) for x in seqs])
        if sort:
            indices, src_seqs = zip(*sorted(enumerate(src_seqs),
                                            key=lambda x: len(x[1]),
                                            reverse=True))
            trg_seqs = [trg_seqs[idx] for idx in indices]

        src_seqs = collate_seq(src_seqs, src_tok)
        trg_seqs = collate_seq(trg_seqs, trg_tok)
        return src_seqs, trg_seqs

    return parallel_collate


def get_loader(data, batch_size, batch_first, num_workers, sort, pin_memory):
    collate_fn = build_collate_fn(data.fields['src'], data.fields['trg'], batch_first=batch_first, sort=sort)
    return DataLoader(
        data,
        batch_size=batch_size,
        collate_fn=collate_fn,
        num_workers=num_workers,
        pin_memory=pin_memory,
    )


class WMT14Dataset(Dataset):
    """Dataset for WMT14 en to de translation
    Based on `torchtext.datasets.WMT14`

    Args:
        root (str): Root folder where to download files
        batch_first (bool): Use batch as first dimension of ouptut
        include_lengths (bool): Include datapoint lengths
        lang (dict): Language translation pair
        math_precision (str): One of `fp16` or `fp32`. The precision used during training
        download (bool): Download the dataset from source
        train (bool): Load train set
        validation (bool): Load validation set
        lazy (bool): Load the dataset in a lazy format
        min_len (int): Minimum sentence length
        max_len (int | None): Maximum sentence length
        max_size (int | None): Maximum dataset size
    """
    urls = [
        (
            "https://storage.googleapis.com/mlbench-datasets/translation/wmt16_en_de.tar.gz",
            "wmt16_en_de.tar.gz",
        )
    ]
    name = "wmt14"
    dirname = ""

    def __init__(
            self,
            root,
            batch_first=False,
            include_lengths=False,
            lang=None,
            math_precision=None,
            download=True,
            train=False,
            validation=False,
            lazy=False,
            min_len=0,
            max_len=None,
            max_size=None,
    ):
        self.lazy = lazy

        super(WMT14Dataset, self).__init__(examples=[], fields={})
        if download:
            url, file_name = self.urls[0]
            maybe_download_and_extract_tar_gz(root, file_name, url)

        src_tokenizer = WMT14Tokenizer(
            root,
            batch_first=batch_first,
            include_lengths=include_lengths,
            lang=lang,
            math_precision=math_precision,
        )
        trg_tokenizer = WMT14Tokenizer(
            root,
            batch_first=batch_first,
            include_lengths=include_lengths,
            lang=lang,
            math_precision=math_precision,
            is_target=True,
        )

        self.vocab_size = src_tokenizer.vocab_size
        self.list_fields = [("src", src_tokenizer), ("trg", trg_tokenizer)]

        self.fields = dict(self.list_fields)
        self.max_len = max_len
        self.min_len = min_len

        if train:
            path = os.path.join(root, config.TRAIN_FNAME)
        elif validation:
            path = os.path.join(root, config.VAL_FNAME)
        else:
            raise NotImplementedError()

        self.examples = process_data(
            path,
            filter_pred=_construct_filter_pred(min_len, max_len),
            fields=self.list_fields,
            lazy=lazy,
            max_size=max_size,
        )

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        if self.lazy:
            src_line, trg_line = self.examples[item]
            return Example.fromlist([src_line, trg_line], self.list_fields)
        else:
            return self.examples[item]

    def __iter__(self):
        for x in self.examples:
            if self.lazy:
                src_line, trg_line = x
                yield Example.fromlist([src_line, trg_line], self.list_fields)
            else:
                yield x
