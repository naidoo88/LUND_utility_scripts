"""
Takes a LUND file containing proton/neutron scattering events (from a deuteron target)
and splits them into files of only one type of scattering (one neut/proton file per input file).
"""

__author__ = "Paul Naidoo"
__date__ = "November 2021"

import argparse
from pathlib import Path

def split_LUND(source_files_path: str, 
    output_files_path: str, 
    lund_file_suffix: str = ".txt"
    ) -> None:

    N_events = 0
    N_prot_events = 0
    N_neut_events = 0

    N_files = 0

    source_files = Path(source_files_path).glob(f"*{lund_file_suffix}")

    for file in source_files:
        print(f"Processing {file}")

        event_buffer = []
        proton_file_buffer = []
        neutron_file_buffer = []
        with open(file, 'r') as current_file:

            for line in current_file:
                # check if event header (skip first header as nothing to write yet)
                if is_header(line) is True:
                    if len(event_buffer) != 0: #needed for passing the first event

                        #Check PID of current event in buffer and pass accordingly
                        recoil_PID = event_recoil_PID(event_buffer[0])
                        if recoil_PID == 2212:
                            proton_file_buffer.append(event_buffer)
                            N_prot_events+=1
                        elif recoil_PID == 2112:
                            neutron_file_buffer.append(event_buffer)
                            N_neut_events+=1
                        else:
                            print(f"Oh dear, PID is {recoil_PID}")

                        event_buffer = []
                        N_events += 1

                event_buffer.append(line)

            #catch the last event:
            if len(event_buffer) != 0: 
                header = event_buffer[0]
                recoil_PID = event_recoil_PID(header)
                if recoil_PID == 2212:
                    proton_file_buffer.append(event_buffer)
                    N_prot_events+=1
                elif recoil_PID == 2112:
                    neutron_file_buffer.append(event_buffer)
                    N_neut_events+=1
                else:
                    print(f"Oh dear, PID is {recoil_PID}")

            write_buffer_to_file(proton_file_buffer, 
                output_path=f"{output_files_path}/pi0D_prot_{N_files}.txt") 
            
            write_buffer_to_file(neutron_file_buffer, 
                output_path=f"{output_files_path}/pi0D_neut_{N_files}.txt") 
            
            N_files+=1

            print(f"Total number of events processed: {N_events}")
            print(f"Number of proton events: {N_prot_events}")
            print(f"Number of neutron events: {N_neut_events}")


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

def event_recoil_PID(line):
    header = line.split()
    return int(header[7]) #8th entry is recoil PID (2212/2112)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Parse LUND files and split into files containing only proton/neutron events."
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

    args = parser.parse_args()

    split_LUND(
        source_files_path = args.input_path,
        output_files_path = args.output_path
    )

    # split_LUND(
    #     source_files_path = "/u/home/pnaidoo/scripts/OSGbatchtest/",
    #     output_files_path = "/u/home/pnaidoo/scripts/split_py_test/output",
    # )
