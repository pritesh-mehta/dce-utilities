"""
@author: pritesh-mehta
"""

import os
import dicom2nifti
from argparse import ArgumentParser

def dce_dicom2nifti_case(case_dir, output_dir, reorient_nifti=False, extension='.nii.gz'):
    """convert DCE case from DICOM to NIfTI
    """
    case_name = os.path.split(case_dir)[-1]
    output_case_dir = os.path.join(output_dir, case_name)
    if not os.path.exists(output_case_dir):
        os.mkdir(output_case_dir)
    for timepoint_dir in os.listdir(case_dir):
        dicom_dir = os.path.join(case_dir, timepoint_dir)
        output_file = os.path.join(output_case_dir, timepoint_dir + extension)
        dicom2nifti.dicom_series_to_nifti(dicom_dir, 
                                          output_file, reorient_nifti=reorient_nifti)
    return None

def dce_dicom2nifti_dir(cases_dir, output_dir, reorient_nifti=False, extension='.nii.gz'):
    """convert DCE cases in directory from DICOM to NIfTI
    """
    for case_name in os.listdir(cases_dir):
        case_dir = os.path.join(cases_dir, case_name)
        print("Processing:", case_dir)
        dce_dicom2nifti_case(case_dir, output_dir, reorient_nifti=reorient_nifti, 
                     extension=extension)
    return None
         
def process():
    parser = ArgumentParser()
    parser.add_argument('--input_dir', required=True, type=str)
    parser.add_argument('--output_dir', required=True, type=str)
    parser.add_argument('--case', required=False, action="store_true")
    parser.add_argument('--reorient_nifti', required=False, action="store_true")
    parser.add_argument('--extension', required=False, type=str, default='.nii.gz')
    
    args = parser.parse_args()
    
    if args.case:
        dce_dicom2nifti_case(args.input_dir, args.output_dir, 
                                 args.reorient_nifti, args.extension)
    else:
        dce_dicom2nifti_dir(args.input_dir, args.output_dir,
                                args.reorient_nifti, args.extension)
    
if __name__ == "__main__":
    process()


