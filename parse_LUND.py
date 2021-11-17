"""
Parse LUND files into a pandas dataframe.
For use in notebooks.

WARNING - uses a LOT of memory as is....

"""

__author__ = "Paul Naidoo"
__date__ = "November 2021"

import uproot
# import argparse
import numpy as np
from numpy import uint8, uint16, uint32, float16, float32
import pandas as pd
from pathlib import Path

def parse_LUND(
    source_files_path: str, 
    selection_regex: str = "*",
    parse_N: int = None
    ):

    ## work in progress to handle memory
    # columns = np.dtype([
    #     ('event_id', np.uint32),
    #     ('n_parts', np.uint8),
    #     ('target_A', np.uint8),
    #     ('target_Z', np.uint8),
    #     ('target_pol', np.float16),
    #     ('beam_pol', np.float16),
    #     ('beam_type', np.uint8),
    #     ('beam_E', np.float16),
    #     ('inter_nuc_pid', np.uint16),
    #     ('proc_id', np.uint8),
    #     ('event_weight', np.float32),
    #     ('index', np.uint8),
    #     ('life_t', np.float16),
    #     ('type', np.uint8),
    #     ('pid', np.uint16),
    #     ('parent_idx', np.uint8),
    #     ('daughter_idx', np.uint8),
    #     ('px', np.float32),
    #     ('py', np.float32),
    #     ('pz', np.float32),
    #     ('pE', np.float32),
    #     ('mass', np.float32),
    #     ('x_vert', np.float32),
    #     ('y_vert', np.float32),
    #     ('z_vert', np.float32)
    # ])

    N_events = 0
    N_files = 0

    source_files = Path(source_files_path).glob(selection_regex)

    # parsed_particles = np.empty(0, columns)
    parsed_particles = []
    for file in source_files:
        N_files+=1
        with open(file, 'r') as current_file:
            for line in current_file:
                # check if event header
                if is_header(line) is True:
                    #new header dict for event
                    event_header = parse_header(line, event_id=N_events)
                    N_events+=1

                    if parse_N == N_events:
                        lund_df = pd.DataFrame(parsed_particles)
                        print(f"Done.\n {N_files} processed.\n {N_events} parsed.")
                        return lund_df
                        
                else:
                    particle = parse_particle(line, event_header)
                    parsed_particles.append(particle)
    
    #convert list to df, and write to file.
    lund_df = pd.DataFrame(parsed_particles)
    print(f"Done.\n {N_files} processed.\n {N_events} parsed.")
    return lund_df

def is_header(line):
    N_entries = len(line.split())
    header=False
    if N_entries == 10:
        header=True

    return header

def parse_header(line, event_id):
    entries = line.split()
    event_header = {
        'event_id': uint32(event_id),
        'n_parts': uint8(entries[0]),
        'target_A': uint8(entries[1]), 
        'target_Z': uint8(entries[2]), 
        'target_pol': float16(entries[3]), 
        'beam_pol': float16(entries[4]), 
        'beam_type': uint8(entries[5]), 
        'beam_E': float16(entries[6]), 
        'inter_nuc_pid': uint16(entries[7]), 
        'proc_id': uint8(entries[8]), 
        'event_weight': float32(entries[9])
    }

    return event_header
    
def parse_particle(line, event_header):
    entries = line.split()
    particle_buff = {
        'index': uint8(entries[0]), 
        'life_t': float16(entries[1]), 
        'type': uint8(entries[2]), 
        'pid': uint16(entries[3]), 
        'parent_idx': uint8(entries[4]), 
        'daughter_idx': uint8(entries[5]), 
        'px': float32(entries[6]), 
        'py': float32(entries[7]), 
        'pz': float32(entries[8]), 
        'pE': float32(entries[9]), 
        'mass': float32(entries[10]), 
        'x_vert': float32(entries[11]), 
        'y_vert': float32(entries[12]), 
        'z_vert': float32(entries[13])
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
        parse_N = 10
    )
