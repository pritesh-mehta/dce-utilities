"""
@author: pritesh-mehta
"""

import numpy as np
from pathlib import Path
import nibabel as nib

def path_generator(input_folder, extension='.nii.gz'):
    """Returns a generator to iterate through filepaths
    """
    input_folder = Path(input_folder)
    filepaths = input_folder.glob(f'*{extension}')  # filepaths is a generator
    return filepaths
    
def load(input_path, dtype=np.float64):
    """Returns name of input file, loaded nifti image and data array
    """
    name = Path(input_path).name
    nii = nib.load(str(input_path))
    data = nii.get_fdata(dtype=dtype)
    return name, nii, data
    
def save(output_path, nii, data):
    """saves data array using loaded nifti image affine and header to 
    output path
    """
    new_nii = nib.Nifti1Image(data, nii.affine, header=nii.header)
    new_nii.to_filename(str(output_path))
    