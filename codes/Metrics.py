# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 14:25:17 2023

@author: Nicolas Indriets
"""
import numpy as np
from dipy.io.image import load_nifti, save_nifti
import nibabel as nib
from os.path import join as pjoin
from TIME.utils import tensor_to_DTI
import sys
 
    
#%%============================================================================
# Diamond tensor metrics
#==============================================================================

def diamond_metrics(study_path, patient_list): 
  for patient in patient_list :
  
      data, affine, img = load_nifti(study_path + patient + '/dMRI/preproc/' + patient + '_dmri_preproc.nii.gz', return_img=True)
      tensor_array_0 = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_diamond_t0.nii.gz').get_fdata()
      tensor_array_1 = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_diamond_t1.nii.gz').get_fdata()
      fractions = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_diamond_fractions.nii.gz').get_fdata()
      f0 = fractions.T[0][0].T
      f1 = fractions.T[1][0].T
      FA_0, AD_0, RD_0, MD_0 = tensor_to_DTI(tensor_array_0)
      FA_1, AD_1, RD_1, MD_1 = tensor_to_DTI(tensor_array_1)
      FA = (f0*FA_0 + f1*FA_1) / (f0 + f1)
      FA[np.isnan(FA)] = 0
      AD = (f0*AD_0 + f1*AD_1) / (f0 + f1)
      AD[np.isnan(AD)] = 0
      RD = (f0*RD_0 + f1*RD_1) / (f0 + f1)
      RD[np.isnan(RD)] = 0
      MD = (f0*MD_0 + f1*MD_1) / (f0 + f1)
      MD[np.isnan(MD)] = 0
      save_nifti(study_path + patient + '/dMRI/microstructure/diamond/' + patient +'_wFA.nii.gz', FA.astype(np.float32),affine)
      save_nifti(study_path + patient + '/dMRI/microstructure/diamond/' + patient +'_wAD.nii.gz', AD.astype(np.float32),affine)
      save_nifti(study_path + patient + '/dMRI/microstructure/diamond/' + patient +'_wRD.nii.gz', RD.astype(np.float32),affine)
      save_nifti(study_path + patient + '/dMRI/microstructure/diamond/' + patient +'_wMD.nii.gz', MD.astype(np.float32),affine)
      return 1

#%% ===========================================================================
# MF metrics 
#==============================================================================

def mf_metrics(study_path, patient_list):
  for patient in patient_list :
  
      data, affine, img = load_nifti(study_path + patient + '/dMRI/preproc/' + patient + '_dmri_preproc.nii.gz', return_img=True)
      mf_fvf_0 = nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_fvf_f0.nii.gz').get_fdata()
      mf_fvf_1 = nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_fvf_f1.nii.gz').get_fdata()
      f0 = nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_frac_f0.nii.gz').get_fdata()
      f1 = nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_frac_f1.nii.gz').get_fdata()
      mf_wfvf = (f0*mf_fvf_0 + f1*mf_fvf_1) / (f0 + f1)
      mf_wfvf[np.isnan(mf_wfvf)] = 0
      save_nifti(study_path + patient + '/dMRI/microstructure/mf/' + patient +'_mf_wfvf.nii.gz', mf_wfvf.astype(np.float32),affine)
      return 1 

#%% ============================================================================
# Main 
#===============================================================================

def main(args):
    print(args)
    study_path = args[1]
    number_of_patients = int(args[2])
    patient_list = []
    for i in range(3, 3 + number_of_patients):
        patient_list.append(args[i])
    diamond = diamond_metrics(study_path, patient_list)
    mf = mf_metrics(study_path, patient_list)

    return 1

if __name__ == "__main__":
    main(sys.argv)

