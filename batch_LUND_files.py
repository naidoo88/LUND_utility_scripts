"""
Create LUND files with a set number of events, either combining or splitting source files.

Reads files line by line, grouping events into an input buffer, which are then added
to an output buffer, until the desired number of events is reached.  This is then 
written to a new file.

Any files left over under the desired event count are also written, but named with 
a 'REMAINDER" in the filename to indicate they are under the count, and to allow
easy selection in a subsequent merging if desired.

All sourcefiles are left intact.

Tested with Python 3.6 and above (choose you binary wisely!)

Usage: 
python3 OSGbatch.py -i /source/files/path -o /output/files/path -p "*neut*.txt"

"""

__author__ = "Paul Naidoo"
__date__ = "November 2021"

import argparse
from pathlib import Path

def LUND_batch(source_files_path: str, 
    output_files_path: str, 
    event_batch_size: int,
    selection_regex: str
    ) -> None:

    event_buffer = []
    output_file_buffer = []
    Total_N_events = 0
    N_events = 0
    N_files = 0
    source_file_counter = 0

    source_files = Path(source_files_path).glob(selection_regex)
    for file in source_files:
        source_file_counter+=1

        print(f"\nProcessing #{source_file_counter}: {file}")

        with open(file, 'r') as current_file:
            for line in current_file:
                # check if event header (skip first header as nothing to write yet)
                if is_header(line) is True:
                    if len(event_buffer) != 0: #needed for passing the first event
                        output_file_buffer.append(event_buffer)
                        event_buffer = []
                        N_events += 1

                        # print(f"Another header.  N_events: {N_events}")

                        if N_events == event_batch_size:
                            output_str = f"{output_files_path}/grouped_{event_batch_size}_{N_files}.txt"
                            write_buffer_to_file(output_file_buffer, 
                                output_path=output_str) 
                            N_files+=1

                            print(f"A FILE WRITTEN: #{N_files}")
                            print(f"{output_str}")

                            #clean up and reinitialise:
                            del output_file_buffer
                            output_file_buffer = []
                            Total_N_events+=N_events
                            N_events = 0

                event_buffer.append(line)

    #Catch any last events at the end under batch_size threshold
    if len(output_file_buffer) != 0: 
        output_file_buffer.append(event_buffer)
        output_str = f"{output_files_path}/grouped_{event_batch_size}_{N_files}_REMAINDER.txt"
        write_buffer_to_file(output_file_buffer, 
            output_path=output_str)

        print(f"A FILE WRITTEN: #{N_files}")
        print(f"{output_str}")

        Total_N_events+=N_events

        
    print(f"Total number of events written: {Total_N_events}")


def write_buffer_to_file(buffer, output_path):
    with open(output_path, 'w') as output_file:
        for events in buffer:
            output_file.writelines(events)

def is_header(line):
    N_entries = len(line.split())
    header=False
    if N_entries == 10:
        header=True

    return header


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Parse LUND files into new files with a specified number of events."
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
        "--input_pattern",
        "-p",
        required=True,
        type=str,
        help="Pattern to select desired events within input directory. TO pass a Rexeg, must use \'-p=\"\*.txt\"\'."
    )
    parser.add_argument(
        "--N_events",
        "-N",
        type=int,
        default=10000,
        help="Number of events to be written to file.",
    )

    args = parser.parse_args()

    LUND_batch(
        source_files_path=args.input_path,
        output_files_path=args.output_path,
        selection_regex=args.input_pattern,
        event_batch_size=args.N_events
    )
    # LUND_batch(
    #     source_files_path = "/u/home/pnaidoo/scripts/LUND_batchtest/",
    #     output_files_path = "/u/home/pnaidoo/scripts/LUND_batchtest/output",
    #     event_batch_size = 10000,
    #     selection_regex = "*.txt"
    # )