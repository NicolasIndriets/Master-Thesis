# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:43:03 2023

@author: Nicolas Indriets
"""

import os 
import numpy as np
import pandas as pd
import sys
from dipy.io.image import load_nifti, save_nifti
import nibabel as nib
import scipy.stats as sc
import matplotlib.pyplot as plt
import json

#%%============================================================================
# Noise vs Motion
#==============================================================================
def get_noise_vs_motion(study_path, patient_list):
    cnr_avg = []
    mot_rel = []
    mot_abs = []
    patients = []
    df = pd.DataFrame()
    for patient in patient_list :
        with open(study_path + patient + '/dMRI/preproc/eddy/' + patient + '_eddy_corr.qc/' + 'qc.json') as user_file:
            file_contents = user_file.read()  
        parsed_json = json.loads(file_contents)
        mot_rel.append(parsed_json['qc_mot_rel'])
        mot_abs.append(parsed_json['qc_mot_abs'])
        cnr_avg.append(parsed_json['qc_cnr_avg'][0])
        patients.append(patient)
    df['cnr_avg'] = cnr_avg
    df['mot_rel'] = mot_rel
    df['mot_abs'] = mot_abs
    df['patients'] = patients
    
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(df['cnr_avg'], df['mot_rel'] ,df['mot_abs'])
    ax.set_xlabel('cnr_avg')
    ax.set_ylabel('mot_rel')
    ax.set_zlabel('mot_abs')
    for i in range(len(patients)):
        ax.text(df['cnr_avg'][i] * (1 + 0.01), df['mot_rel'][i] * (1 + 0.01), df['mot_abs'][i] * (1+0.01) , patients[i], fontsize=12)
        
    
#%% ===========================================================================
# Headers
#==============================================================================
def get_headers(patient_list):
    for patient in patient_list:
        file_raw = nib.load(study_path + patient + '/dMRI/raw/' + patient + '_raw_dmri.nii.gz')
        print('raw :', file_raw.header)
        file_reslice = nib.load(study_path + patient + '/dMRI/preproc/reslice/' + patient + '_reslice.nii.gz')
        print('reslice :', file_reslice.header)

#%%============================================================================
# Main 
#==============================================================================
        
study_path = 'D:/Study/'
patient_list = ["sub-009", "sub-013", "sub-018","sub-014", "sub-017", "sub-020", "sub-021", "sub-025", "sub-026", "sub-028", "sub-032", "sub-033", "sub-036", "sub-037", "sub-038", "sub-040", "sub-041", "sub-042", "sub-043", "sub-046", "sub-047", "sub-048", "sub-049", "sub-050", "sub-051", "sub-052", "sub-054", "sub-055", "sub-056", "sub-057", "sub-059", "sub-060", "sub-061", "sub-062", "sub-063", "sub-064", "sub-065", "sub-066", "sub-067",  "sub-069",  "sub-071","sub-073", "sub-076", "sub-077", "sub-078", "sub-084", "sub-085", "sub-086",  "sub-098",   "sub-103", "sub-104","sub-106",  "sub-110", "sub-117", "sub-121", "sub-132", "sub-134", "sub-135", "sub-148", "sub-044", "sub-068", "sub-070", "sub-093", "sub-108", "sub-145"]

get_headers(patient_list)
get_noise_vs_motion(study_path, patient_list)