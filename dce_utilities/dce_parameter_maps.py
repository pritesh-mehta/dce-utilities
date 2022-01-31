"""
@author: pritesh-mehta
"""

import numpy as np
from pathlib import Path
from argparse import ArgumentParser

import dce_utilities.nifti_utilities as nutil

def dce_parameter_maps_case(case_path, temporal_resolution, window_size, 
                        onset_time_constraint, final_slope_time, 
                        save_case=False, output_dir=None, mask_path=None):
    """DCE parameter map computation 
    (initial slope, max enhancement, time to max enhancement, final_slope)
    args:
        case_path: 4D DCE nifti
        output_directory: for storing parameter maps
        temporal_resolution: time interval between DCE timepoints (seconds)
        window_size: sliding window length for initial slope calculation (number of timepoints)
        onset_time_constraint: constraint before which enhancement onset must occur (minutes)
        final_slope_time: time interval to calculate the final slope over (minutes)
        mask_path: 3D mask in DCE space (used for alternative normalization of voxels containing erronerous values)
    """
    
    case_name, case_nii, case_data = nutil.load(case_path)    
    case_shape = np.shape(case_data)
    
    x_dim = case_shape[0]
    y_dim = case_shape[1]
    z_dim = case_shape[2]
    t_dim = case_shape[3]
                
    # reshape case_data (for vectorised operations)
    y = np.reshape(case_data, (x_dim * y_dim * z_dim, t_dim), order='C')
        
    # time resolution vector in minutes
    x = np.arange(t_dim) * temporal_resolution / 60
    
    # find the first 3 non-zero value timepoints 
    # and normalise by their average intensity (Kubassova et al.)    
    y_count_non_zero = np.zeros((np.shape(y)[0], np.shape(y)[1] - 3 + 1))
    for i in range(t_dim):
        if i < t_dim - 3 + 1:
            y_window_count_non_zero = np.count_nonzero(y[:, i: i + 3], axis=1)
            y_count_non_zero[:, i] = y_window_count_non_zero
            
    y_norm_index = np.argmax(y_count_non_zero, axis=1)
    
    b_1 = np.zeros((np.shape(y)[0], 1))
    b_2 = np.zeros((np.shape(y)[0], 1))
    b_3 = np.zeros((np.shape(y)[0], 1))
    
    for i in range(np.shape(b_1)[0]):
        b_1[i][0] = y[i][y_norm_index[i]]
        b_2[i][0] = y[i][y_norm_index[i] + 1]
        b_3[i][0] = y[i][y_norm_index[i] + 2]
        
    b = (b_1 + b_2 + b_3) / 3        
    
    b = np.reshape(b, (np.shape(b)[0], 1))
    
    if mask_path is None:
       y_norm = y / b 
    else:
        # find alternative normalisation value (if b too small)
        mask_name, mask_nii, mask_data = nutil.load(mask_path)
        masked_case_data_t0 = np.ma.array(case_data[:, :, :, 0], mask=(mask_data - 1) * (-1))
        c = np.percentile(masked_case_data_t0.compressed(), 1)
        
        e = np.maximum(b, c)
        
        y_norm = y / e

    # moving gradient calculation for initial slope and onset time calculation (Kubassova et al.)
    y_grads = np.zeros((np.shape(y)[0], np.shape(y)[1] - window_size + 1))
    for i in range(t_dim):
        if i < t_dim - window_size + 1:
            y_window = y_norm[:, i: i + window_size]
            y_window = np.transpose(y_window)
            x_window = x[i: i + window_size]
            z = np.polyfit(x_window, y_window, 1)
            z = np.transpose(z)
            y_grads[:, i] = z[:, 0]
        
    # onset time constraint
    idx_time_constraint = int(np.where(
            np.max(x[np.where(x <= onset_time_constraint)]) == x)[0][0])
    
    initial_slope = np.max(y_grads[:, 0: idx_time_constraint + 1], axis=1)
    initial_slope = np.reshape(initial_slope, (np.shape(initial_slope)[0],1))
    idx_initial_slope_unique = np.argmax(y_grads == initial_slope, axis=1)
    
    # onset time calculation (Kubassova et al.)
    t_onset = x[idx_initial_slope_unique]
    
    # maximum enhancement calculation (Zelhof et al.)
    max_enhancement = np.max(y_norm, axis=1)
    max_enhancement = np.reshape(max_enhancement, (np.shape(max_enhancement)[0], 1))
    idx_max_enhancement_unique = np.argmax(y_norm == max_enhancement, axis=1)

    # time to max enhancement calculation (Zelhof et al.)
    t_max = x[idx_max_enhancement_unique] - t_onset
        
    # moving gradient calculation for final slope (Zelhof et al.)
    window_size_fs = int(final_slope_time / (x[1] - x[0]))
    y_grads_fs = np.zeros((np.shape(y)[0], np.shape(y)[1] - window_size_fs + 1))
    for i in range(t_dim):
        if i < t_dim - window_size_fs + 1:
            y_window = y_norm[:, i: i + window_size_fs]
            y_window = np.transpose(y_window)
            x_window = x[i: i + window_size_fs]
            z = np.polyfit(x_window, y_window, 1)
            z = np.transpose(z)
            y_grads_fs[:, i] = z[:, 0]
            
    final_slope = y_grads_fs[:, -1]
    final_slope = np.reshape(final_slope, (np.shape(final_slope)[0], 1))
    
    # reshape
    initial_slope = np.reshape(initial_slope, (x_dim, y_dim, z_dim), order='C')    
    max_enhancement = np.reshape(max_enhancement,(x_dim, y_dim, z_dim), order='C')    
    t_max = np.reshape(t_max, (x_dim, y_dim, z_dim), order='C')
    final_slope = np.reshape(final_slope, (x_dim, y_dim, z_dim), order='C')
    
    if save_case:
        output_path = Path(output_dir) / ("IS_" + case_name)
        nutil.save(output_path, case_nii, initial_slope)
        
        output_path = Path(output_dir) / ("ME_" + case_name)
        nutil.save(output_path, case_nii, max_enhancement)
        
        output_path = Path(output_dir) / ("TM_" + case_name)
        nutil.save(output_path, case_nii, t_max)
        
        output_path = Path(output_dir) / ("FS_" + case_name)
        nutil.save(output_path, case_nii, final_slope)

    return initial_slope, max_enhancement, t_max, final_slope

def dce_parameter_maps_dir(cases_dir, temporal_resolution, 
                             window_size, onset_time_constraint, 
                             final_slope_time, output_dir, mask_dir=None, 
                             extension='.nii.gz'):
    """DCE parameter map computation for directory
    """
    
    case_paths = nutil.path_generator(cases_dir, extension=extension)
    for case_path in case_paths:
        print("Processing:", case_path)
        if mask_dir is not None:
            case_name = Path(case_path).parts[-1]
            mask_path = Path(mask_dir) / case_name
        else:
            mask_path=None
        dce_parameter_maps_case(case_path, temporal_resolution, window_size, 
                        onset_time_constraint, final_slope_time, 
                        save_case=True, output_dir=output_dir, mask_path=mask_path)
    return None

def process():
    parser = ArgumentParser()
    parser.add_argument('--input_dir_or_path', required=True, type=str)
    parser.add_argument('--output_dir', required=True, type=str)
    parser.add_argument('--case', required=False, action="store_true")
    parser.add_argument('--temporal_resolution', required=True, type=float)
    parser.add_argument('--window_size', required=True, type=int)
    parser.add_argument('--onset_time_constraint', required=True, type=float)
    parser.add_argument('--final_slope_time', required=True, type=float)
    parser.add_argument('--mask_dir_or_path', required=False, type=str)
    parser.add_argument('--extension', required=False, type=str, default='.nii.gz')

    args = parser.parse_args()
    
    if args.case:
        dce_parameter_maps_case(args.input_dir_or_path, 
                            args.temporal_resolution, 
                            args.window_size, 
                            args.onset_time_constraint, 
                            args.final_slope_time,
                            save_case=True,
                            output_dir=args.output_dir, 
                            mask_path=args.mask_dir_or_path)
    else:
        dce_parameter_maps_dir(args.input_dir_or_path, 
                           args.temporal_resolution, 
                           args.window_size, 
                           args.onset_time_constraint, 
                           args.final_slope_time, 
                           args.output_dir, 
                           mask_dir=args.mask_dir_or_path,
                           extension=args.extension)
    
if __name__ == "__main__":
    process()
