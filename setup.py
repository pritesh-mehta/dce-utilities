"""
@author: pritesh-mehta
"""

from setuptools import setup, find_packages

setup(name='dce_utilities',
      version='1.0',
      description='Dynamic contrast enhanced MRI utilities',
      url='https://github.com/pritesh-mehta/dce_utilities',
      python_requires='>=3.6',
      author='Pritesh Mehta',
      author_email='pritesh.mehta@kcl.ac.uk',
      license='Apache 2.0',
      zip_safe=False,
      install_requires=[
      'dicom2nifti',
      'pathlib',
      'argparse',
      'numpy',
      'nibabel'
      ],
      entry_points={
        'console_scripts': [
            'dce_dicom2nifti_convert=dce_utilities.dce_dicom2nifti_convert:process',
            'dce_nifti4d=dce_utilities.dce_nifti4d:process',
            'dce_parameter_maps=dce_utilities.dce_parameter_maps:process',
            ],
      },
      packages=find_packages(include=['dce_utilities']),
      classifiers=[
          'Intended Audience :: Science/Research',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering',
      ]
      )