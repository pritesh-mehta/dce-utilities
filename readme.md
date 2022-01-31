# DCE-Utilities

This repository contains functionality for transforming dynamic contrast-enhanced (DCE) magnetic resonance imaging (MRI) series, including:

1) Conversion of DCE MRI dicom series to NIfTI format.

2) Conversion of 3D DCE MRI in NIfTI format to 4D (spatial dims + time dim) DCE MRI in NIfTI format.

3) Calculation of DCE parameter maps using 4D DCE data<sup>1</sup> <sup>2</sup>: initial slope, maximum enhancement, time-to-maximum enhancement, and final slope.

If you use this repository, please cite the following publication: 

[Mehta, P., Antonelli, M., Ahmed, H.U., Emberton, M., Punwani, S., Ourselin, S. Computer-aided diagnosis of prostate cancer using multiparametric MRI and clinical features: A patient-level classification framework. Medical Image Analysis 2021, 73, 102153, doi:10.1016/j.media.2021.102153.](https://www.sciencedirect.com/science/article/pii/S1361841521001997?via%3Dihub)


## Installation instructions 

1) Clone/download repository.

2) Change directory into repository.

3) Install:
	```
	pip install .
    ```
	
## How to use it 

- Function imports.

- Command line:

	- Dicom to NIfTI format conversion:
		```
		dce_dicom2nifti_convert --input_dir .\sample_data\0_sample_dce_dicom --output_dir .\sample_data\1_dce_nifti_3d
		```

	- 3D to 4D:
		```
		dce_nifti4d --input_dir .\sample_data\1_dce_nifti_3d --output_dir .\sample_data\2_dce_nifti_4d
		```

	- Parameter maps:
		```
		dce_parameter_maps --input_dir_or_path .\sample_data\2_dce_nifti_4d  --output_dir .\sample_data\3_dce_parameter_maps --temporal_resolution 3.5 --window_size 5 --onset_time_constraint 1 --final_slope_time 1 
		```
	
## References

<sup>1</sup> Zelhof, B.; Lowry, M.; Rodrigues, G.; Kraus, S.; Turnbull, L. Description of magnetic resonance imaging-derived enhancement variables in pathologically confirmed prostate cancer and normal peripheral zone regions. BJU International. 2009, 104, 621–627.

<sup>2</sup> Kubassova, O.A.; Boyle, R.D.; Radjenovic, A. Quantitative Analysis of Dynamic Contrast-Enhanced MRI Datasets of the Metacarpophalangeal Joints. Academic Radiology. 2007, 14, 1189–1200.
