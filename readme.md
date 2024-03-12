# Fasta Subsequence Extractor
This Python script extracts subsequences from a given FASTA file based on coordinates specified in a text file. The extracted subsequences are saved to an output FASTA file. It leverages the BioPython library to handle FASTA file parsing and subsequence extraction. This README outlines the script's functionality, prerequisites, and usage instructions.

# Prerequisites
Python 3.x
BioPython library
Before running the script, ensure you have Python 3.x installed on your system and the BioPython library. You can install BioPython using pip:

```sh
pip install biopython
```

Or install via:
```sh
pip install -r requirements.txt
```

# Script Overview
The script takes three main arguments:

A FASTA file (-s) containing the sequences from which subsequences will be extracted.
A coordinate file (-c) in text format specifying the ID, start, and end positions for each subsequence to be extracted.
An output FASTA file (-o) where the extracted subsequences will be saved.
The coordinate file should be formatted with one entry per line, where each line contains the sequence ID followed by the start and end positions of the subsequence, separated by whitespace. Lines starting with "#" are considered comments and ignored.

# Usage
Run the script from the command line by providing the required arguments:

```sh
./your_script_name.py -s your_fasta_file.fasta -c your_coordinate_file.txt -o output_file.fasta
```

Replace your_script_name.py with the name of this Python script, your_fasta_file.fasta with the path to your input FASTA file, your_coordinate_file.txt with the path to your coordinate file, and output_file.fasta with the desired path for the output FASTA file containing the extracted subsequences.

# Example Coordinate File

```sql
#SequenceID Start End
Seq1 100 200
Seq2 150 250
```

This example specifies that a subsequence from Seq1 starting at position 100 and ending at position 200 should be extracted, and another subsequence from Seq2 starting at position 150 and ending at position 250 should be extracted.

# License
This script is provided "as is", without warranty of any kind. You are free to use, modify, and distribute it as you see fit.
