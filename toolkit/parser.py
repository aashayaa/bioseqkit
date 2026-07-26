"""
parser.py
=========
FASTA/FASTQ I/O built on top of Biopython's SeqIO.
"""


from pathlib import Path
from typing import Iterator, Iterable, Optional

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

FASTA_EXTENSIONS = {".fa", ".fasta", ".fna", ".ffn", ".faa"}
FASTQ_EXTENSIONS = {".fq", ".fastq"}


def guess_format(path: str) -> str:
    """Guess 'fasta' or 'fastq' from a file extension (handles .gz)."""
    p = Path(path)
    suffixes = [s.lower() for s in p.suffixes]
    ext = suffixes[-2] if suffixes and suffixes[-1] == ".gz" and len(suffixes) > 1 else (suffixes[-1] if suffixes else "")

    if ext in FASTA_EXTENSIONS:
        return "fasta"
    if ext in FASTQ_EXTENSIONS:
        return "fastq"
    raise ValueError(f"Could not determine format for file: {path}. Pass format explicitly.")


def read_sequences(path: str, format: Optional[str] = None) -> Iterator[SeqRecord]:
    """Lazily iterate over sequence records in a FASTA or FASTQ file."""
    fmt = format or guess_format(path)

    if path.endswith(".gz"):
        import gzip
        with gzip.open(path, "rt") as handle:
            yield from SeqIO.parse(handle, fmt)
    else:
        yield from SeqIO.parse(path, fmt)


def count_sequences(path: str, format: Optional[str] = None) -> int:
    """Count sequences without holding them all in memory."""
    return sum(1 for _ in read_sequences(path, format))


def write_sequences(records: Iterable[SeqRecord], path: str, format: Optional[str] = None) -> int:
    """Write an iterable of SeqRecords to a file. Returns count written."""
    fmt = format or guess_format(path)
    return SeqIO.write(records, path, fmt)