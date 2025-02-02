# LR-splitpipe

[![DOI](https://zenodo.org/badge/313807619.svg)](https://zenodo.org/badge/latestdoi/313807619)

LR-splitpipe is a pipeline designed for demultiplexing, debarcoding, and preparing LR-Split-seq data.

## Demultiplexing reads

<img width="450" src="demux_pipeline.png">


To demultiplex reads for their Split-seq barcodes, use `demultiplex.py`.

```
Usage: python LR-splitpipe/demultiplex.py {all, score_linkers, find_bcs, process_bcs} [options]

Subcommands:
  all                  Run all steps of demultiplexing
  score_linkers        Run steps through scoring the linkers (step 1)
                       and generate QC plots based on scored linkers
  find_bcs             Run all steps through finding the barcodes (steps 1-3)
  process_bcs          Run steps after finding barcodes (steps 4-6)

Options:
  -f                   FASTQ (gzipped or not) file output with LR-Split-seq or Split-seq reads
  -o                   Output file path / prefix
  -t                   Number of threads to run on (multithreading is recommended)
  -k                   Kit used for barcoding {WT, WT_mini, WT_mega}
  --l1_mm              Number of allowable mismatches in linker1
                        Default: 3
  --l2_mm              Number of allowable mismatches in linker2
                        Default: 3
  --chunksize          Number of lines to read in / process at a time
                        Default: 10**5
  --max_linker_dist    Maximum distance that a linker can be from the end of a read
                        Default: None (recommended ~200 based on our data)
  --max_read_len       Maximum read length to analyze for linkers / barcodes
                        Default: None
  --verbosity          Verbosity setting.
                         0: No output
                         1: QC statistics
                         2: QC statistics + progress
  --delete_input       Flag to delete temporary files (recommended!)
```

### Demultiplexing steps:

#### 1. Score linkers

First, LR-splitpipe uses alignment to find reads that have linkers in them, which are the static regions that connect each of the combinatorial barcodes. Reads that have fewer than 4 errors in each linker will then be used to find barcodes.

#### 2. Align linkers

Using the reads that had valid linkers found in them, determine the location in the read of each linker.
Note: This step typically takes the longest! Parallelization will help with this!

#### 3. Find barcodes

With the locations of the linkers from step 2, extract the barcodes from each read.

#### 4. Correct barcodes

Correct barcodes to those that are within edit distance of 3 of the list of possible Split-seq barcodes. This step uses code and assets (barcodes and barcodes within edit distance 3) from the original [Parse Biosciences](https://www.parsebiosciences.com/) Split-seq demultiplexing code, which is designed for short reads.

#### 5. Trim barcodes

After recording the barcode and UMI for each read, trim the construct off from the sequence as this part will mess up mapping.

#### 6. Filter out duplicate UMIs

Filter out reads with duplicate UMIs per barcode, keeping the longest read.

#### 7. Write to fastq

Take the barcode/UMI for each read and append it to the read name of each read. Output the trimmed reads labeled by their barcodes to a fastq file.


## Adding cell barcode as BAM tag

After running the demultiplexer, reads should be mapped and converted to a SAM file. In this file format, the barcode, which is in the read header in fastq format, can be moved to a cell barcode (CB:Z:NNNNN...) tag as part of the SAM file. This is useful to be able to run [TALON](https://github.com/mortazavilab/TALON) on the single-cell data down the line. To do this, run `add_bam_tag.py`.

Note: It is recommended to use the `--merge_primers` option. If you *don't* use this option, oligodT primed and random hexamer primed reads from the same cells won't be merged

```
Usage: python LR-splitpipe/add_bam_tag.py

Options:
  -s                   SAM file with Split-seq barcode+UMI information in
                         the read name
  -k                   Kit used for barcoding {WT, WT_mini, WT_mega}
  --merge_primers      Merge reads that come from the same cell from different
                         priming strategies
  --suffix             Suffix to add to cell barcodes. Useful if merging
                         separate LR-Split-seq experiments that might have
                         overlapping barcodes otherwise
  -o                   Output file path/prefix
```

## Citing this software

Please cite [our publication](doi.org/10.1186/s13059-021-02505-w) and / or the [Zenodo DOI]() for the release you used!
