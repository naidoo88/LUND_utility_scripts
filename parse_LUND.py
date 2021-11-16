"""
Parse LUND files into a pandas dataframe.
For use in notebooks.

"""

__author__ = "Paul Naidoo"
__date__ = "November 2021"

import uproot
# import argparse
import numpy as np
import pandas as pd
from pathlib import Path

def parse_LUND(
    source_files_path: str, 
    output_file_path: str, 
    selection_regex: str = "*"
    ) -> None:

    N_events = 0
    N_files = 0

    source_files = Path(source_files_path).glob(selection_regex)

    with uproot.recreate(output_file_path) as root_file:
        # root_file.mktree("LUND")
        for file in source_files:
            parsed_events = []
            N_files+=1

            print(f"\nProcessing #{N_files}: {file}")

            with open(file, 'r') as current_file:
                for line in current_file:
                    # check if event header
                    if is_header(line) is True:
                        #new header dict for event
                        event_header = parse_header(line, event_id=N_events)
                        N_events+=1

                    else:
                        particle = parse_particle(line, event_header)
                        parsed_events.append(particle)
        
            #at the end of each file, convert list to df, and write to file.
            lund_df = pd.DataFrame(parsed_events)


        print(f"Done.\n {N_files} Processed.\n {N_events} written.")

def is_header(line):
    N_entries = len(line.split())
    header=False
    if N_entries == 10:
        header=True

    return header

def parse_header(line, event_id):
    entries = line.split()
    event_header = {
        'event_id': int(event_id),
        'n_parts': int(entries[0]),
        'target_A': int(entries[1]), 
        'target_Z': int(entries[2]), 
        'target_pol': float(entries[3]), 
        'beam_pol': float(entries[4]), 
        'beam_type': int(entries[5]), 
        'beam_E': float(entries[6]), 
        'inter_nuc_id': int(entries[7]), 
        'proc_id': int(entries[8]), 
        'event_weight': float(entries[9])
    }

    return event_header
    
def parse_particle(line, event_header):
    entries = line.split()
    particle_buff = {
        'index': int(entries[0]), 
        'life_t': float(entries[1]), 
        'type': int(entries[2]), 
        'pid': int(entries[3]), 
        'parent_idx': int(entries[4]), 
        'daughter_idx': int(entries[5]), 
        'px': float(entries[6]), 
        'py': float(entries[7]), 
        'pz': float(entries[8]), 
        'pE': float(entries[9]), 
        'mass': float(entries[10]), 
        'x_vert': float(entries[11]), 
        'y_vert': float(entries[12]), 
        'z_vert': float(entries[13])
    }
    #combine header/particle data
    particle = {**event_header, **particle_buff}
    return particle



if __name__ == '__main__':

    # parser = argparse.ArgumentParser(
    #     description="Parse LUND file events and write to a ROOT file."
    # )
    # parser.add_argument(
    #     "--input_path",
    #     "-i",
    #     required=True,
    #     type=str,
    #     help="Path to input LUND files",
    # )
    # parser.add_argument(
    #     "--output_path",
    #     "-o",
    #     required=True,
    #     type=str,
    #     help="Path to output location.",
    # )
    # parser.add_argument(
    #     "--input_pattern",
    #     "-p",
    #     required=False,
    #     type=str,
    #     default="*",
    #     help="Pattern to select desired events within input directory. TO pass a Rexeg, must use \'-p=\"\*.txt\"\'."
    # )
    # args = parser.parse_args()

    # parse_LUND(
    #     source_files_path=args.input_path,
    #     output_file_path=args.output_path,
    #     selection_regex=args.input_pattern
    # )
    parse_LUND(
        source_files_path="/w/work3/home/pauln/sim/15_pi0_genfiles/",
        output_file_path="/home/pauln/lund.root"
    )
