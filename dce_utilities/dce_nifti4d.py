"""
@author: pritesh-mehta
"""

import numpy as np
from pathlib import Path
from argparse import ArgumentParser

import dce_utilities.nifti_utilities as nutil
    
def dce_nifti4d_case(case_dir, save_case=False, output_dir=None, extension='.nii.gz'):
    """convert 3D nifti DCE timepoints to 4D nifti
    """
    case_name = Path(case_dir).parts[-1]
    timepoint_stack = []
    timepoint_paths = nutil.path_generator(case_dir, extension=extension)
    for path in timepoint_paths:
        name, nii, data = nutil.load(path)
        timepoint_stack.append(data)
    timepoint_stack = np.moveaxis(np.array(timepoint_stack), 0, -1)
    if save_case:
        save_path = Path(output_dir) / (case_name + extension)
        nutil.save(save_path, nii, timepoint_stack)
    return timepoint_stack

def dce_nifti4d_dir(cases_dir, output_dir, extension='.nii.gz'):
    """convert directory of 3D nifti DCE timepoints to 4D nifti
    """
    for case_dir in Path(cases_dir).iterdir():
        print("Processing:", case_dir)
        dce_nifti4d_case(case_dir, save_case=True, output_dir=output_dir, extension=extension)
    return None
    
def process():
    parser = ArgumentParser()
    parser.add_argument('--input_dir', required=True, type=str)
    parser.add_argument('--output_dir', required=True, type=str)
    parser.add_argument('--case', required=False, action="store_true")
    parser.add_argument('--extension', required=False, type=str, default='.nii.gz')
    
    args = parser.parse_args()
    
    if args.case:
        dce_nifti4d_case(args.input_dir, save_case=True, output_dir=args.output_dir,
                         extension=args.extension)
    else:
        dce_nifti4d_dir(args.input_dir, args.output_dir, extension=args.extension)
    
if __name__ == "__main__":
    process()