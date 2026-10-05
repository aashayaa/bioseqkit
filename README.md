## bioseqkit

A small Python toolkit for working with FASTA/FASTQ sequence files, built
on top of Biopython. It's focused on a clean I/O layer, reading,
writing, and format detection, as the foundation for QC and preprocessing
tools that are often needed.

- **`guess_format(path)`** infers whether a file is FASTA or FASTQ based
  on its extension (and it handles .gz-compressed files too)
