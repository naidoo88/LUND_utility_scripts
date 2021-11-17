"""
Extract the output of an OSG job, and move all files to a single directory
with consistent naming.

Usage: 
python3 OSGbatch.py -i /source/files/path -o /output/files/path -p "*neut*.txt"

"""

__author__ = "Paul Naidoo"
__date__ = "November 2021"

import argparse
from shutil import copy
from pathlib import Path

def extract_OSG(
    OSG_job_path: str,
    output_files_path: str,
    output_files_name:str
    ) -> None:

    OSG_output_files = Path(OSG_job_path).glob("**/*.hipo")

    for ii, file in enumerate(OSG_output_files):
        #Pad the number with 0s up to 8 sig.figs.
        output_file = Path(output_files_path) / f"{output_files_name}_{ii:08}.hipo"
        copy(file, output_file)

    return

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Extract the output of an OSG job, and move all files to a single directory with consistent naming."
    )
    parser.add_argument(
        "--input_path",
        "-i",
        required=True,
        type=str,
        help="Path to input LUND files",
    )
    parser.add_argument(
        "--output_path",
        "-o",
        required=True,
        type=str,
        help="Path to output location.",
    )
    parser.add_argument(
        "--output_name",
        "-s",
        required=True,
        type=str,
        help="Name-stub for moved files."
    )
    args = parser.parse_args()

    extract_OSG(
        OSG_job_path=args.input_path,
        output_files_path=args.output_path,
        output_files_name=args.output_name
    )
