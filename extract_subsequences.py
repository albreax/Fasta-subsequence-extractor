#!/usr/bin/env python3
 
import sys
import os
import re
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import gzip

__author__ = 'albrecht.naumann@posteo.de'

"""
The script extract subsequences from a given fasta file by a given
coordinate txt. All extracted subsequences resulting in a output fasta file.
"""


def is_valid_file(s_file_path, s_file_type):
    """return True if file exists"""
    return (os.path.isfile(s_file_path) and
            s_file_path.lower().endswith(s_file_type))


def parse_coordinate_line(line):
    """
    parse a line of the coordinate file and return a coordinate dictionary
    """

    # return if line is empty or a comment
    l = re.sub(re.compile(r'\s+'), '', line)
    if l == '' or l.startswith("#"):
        return

    pttn = re.compile(r"(.+)\s+([0-9]+)\s+([0-9]+)")
    m = re.match(pttn, line)

    if not m:
        raise Exception("ERROR coordinate file error in line:\n\t%s"
                        % (line)
                        )
    # create coordinate dictionary
    c = {
        "id": m.group(1),
        "start": int(m.group(2)),
        "end": int(m.group(3))
    }

    if c["end"] < c["start"]:
        start = c["end"]
        c["end"] = c["start"]
        c["start"] = start

    return c


def main(argv):
    fasta_file = False
    coordinate_file = False
    output_file = False
    margin = 0
    
    args = ' '.join(argv)

    for arg in ['-s', '-c', '-o', '-m']:
        regex = re.compile(r"%s\s+(\S+)" % (arg))
        m = re.search(regex, args)

        if not m:
            sys.exit(
                "ERROR: Missing parameter\n" +
                "read README.md for more information")

        # if fasta file is zipped, open it with gzip
        if arg == '-s' and is_valid_file(m.group(1), '.gz'):
            fasta_file = gzip.open(m.group(1), 'rt')
        if arg == '-s' and is_valid_file(m.group(1), '.fasta'):
            fasta_file = m.group(1)
        elif arg == '-c' and is_valid_file(m.group(1), '.txt'):
            coordinate_file = m.group(1)
        elif arg == '-o':
            output_file = m.group(1)
        elif arg == '-m':
            margin = int(m.group(1))

    # is a fasta file passed
    if not fasta_file:
        sys.exit(
            "ERROR: Missing fasta file\nread README.md for more information")
    if not coordinate_file:
        sys.exit(
            "ERROR: Missing coordinate " +
            "file\nread README.md for more information")
    if not output_file:
        sys.exit(
            "ERROR: Missing output fasta " +
            "file\nread README.md for more information")

    coordinates = {}
    # read given coordinate file and save each coordinate
    with open(coordinate_file) as fh:
        for line in fh:
            # save sequence ID start and end in coordinates
            try:
                result = parse_coordinate_line(line)
                if not result:
                    continue

                if not result['id'] in coordinates:
                    coordinates[result['id']] = []

                c = {"start": result['start'], "end": result['end']}

                if c not in coordinates[result['id']]:
                    coordinates[result['id']].append(c)

            except Exception as e:
                sys.exit(e)
    # clear file
    open(output_file, 'w').close()
    oh = open(output_file, "a")

    # read given fasta file and process each sequence record
    for seq_record in SeqIO.parse(fasta_file, "fasta"):

        if seq_record.id in coordinates:
            for c in coordinates[seq_record.id]:
                start = int(c["start"]) - margin
                end = int(c["end"]) + margin
                # extract fragment sequence
                fragment = Seq(str(seq_record.seq)[start:end])
                # fragment description
                description = "fragment start: %s end: %s" % (
                    str(start), str(end))
                
                # validate fragment length
                # print("fragment length: ", len(fragment), "start: ", start, "end: ", end, "start:end", end - start)
                if len(fragment) != (end - start):
                  print("ERROR: fragment length not equal to given coordinates")
                  continue
                
                # create output record
                out_record = SeqRecord(
                    fragment.upper(),
                    id=seq_record.id,
                    description="<%s>" % (description)
                )
                # append output record to output sequences
                SeqIO.write(out_record, oh, "fasta")

    oh.close()

if __name__ == "__main__":
    main(sys.argv)
    print("done")