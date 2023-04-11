# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 10:44:44 2023

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

#%%============================================================================
# Dataframe 
#==============================================================================

def statistic(study_path, patient_list, atlas_list):
    
    df = pd.read_csv(study_path + "/Patient_data.csv", sep = ',')
    df = df.drop('Unnamed: 0', 'columns')
    raw_value = pd.DataFrame()
    grouped_raw_value1 = pd.DataFrame()
    grouped_raw_value2 = pd.DataFrame()
    for atlas in atlas_list:
        if 'mean_FA' + '_' + atlas not in df.columns:
            df['mean_FA' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_FA' + '_' + atlas not in df.columns:
            df['var_FA' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_MD' + '_' + atlas not in df.columns:
            df['mean_MD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_MD' + '_' + atlas not in df.columns:
            df['var_MD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_AD' + '_' + atlas not in df.columns:
            df['mean_AD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_AD' + '_' + atlas not in df.columns:
            df['var_AD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_RD' + '_' + atlas not in df.columns:
            df['mean_RD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_RD' + '_' + atlas not in df.columns:
            df['var_RD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
            
        if 'mean_wFA' + '_' + atlas not in df.columns:
            df['mean_wFA' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_wFA' + '_' + atlas not in df.columns:
            df['var_wFA' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_wMD' + '_' + atlas not in df.columns:
            df['mean_wMD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_wMD' + '_' + atlas not in df.columns:
            df['var_wMD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_wAD' + '_' + atlas not in df.columns:
            df['mean_wAD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_wAD' + '_' + atlas not in df.columns:
            df['var_wAD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_wRD' + '_' + atlas not in df.columns:
            df['mean_wRD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_wRD' + '_' + atlas not in df.columns:
            df['var_wRD' + '_' + atlas] = np.zeros(len(df['Patient ID']))
            
    
        if 'mean_fiso' + '_' + atlas not in df.columns:
            df['mean_fiso' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_fiso' + '_' + atlas not in df.columns:
            df['var_fiso' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_fintra' + '_' + atlas not in df.columns:
            df['mean_fintra' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_fintra' + '_' + atlas not in df.columns:
            df['var_fintra' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_fextra' + '_' + atlas not in df.columns:
            df['mean_fextra' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_fextra' + '_' + atlas not in df.columns:
            df['var_fextra' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_ODI' + '_' + atlas not in df.columns:
            df['mean_ODI' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_ODI' + '_' + atlas not in df.columns:
            df['var_ODI' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        
        if 'mean_wfvf' + '_' + atlas not in df.columns:
            df['mean_wfvf' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_wfvf' + '_' + atlas not in df.columns:
            df['var_wfvf' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'mean_fvf_tot' + '_' + atlas not in df.columns:
            df['mean_fvf_tot' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        if 'var_fvf_tot' + '_' + atlas not in df.columns:
            df['var_fvf_tot' + '_' + atlas] = np.zeros(len(df['Patient ID']))
        
        
        group1 = pd.DataFrame()
        group2 = pd.DataFrame()
        for patient in patient_list:  
            group = pd.DataFrame()
            text = patient.split("-")
            ID = int(text[1])
            for i in range(len(df["Patient ID"])):
                if(df["Patient ID"][i] == ID):
                    index = i
                    break 
            additional = pd.DataFrame()
            mask, affine_mask, img_mask = load_nifti(study_path + patient + '/transformed/' + patient + '_' + atlas + '.nii.gz', return_img=True)
            FA = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_FA.nii.gz').get_fdata() 
            MD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_MD.nii.gz').get_fdata() 
            RD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_RD.nii.gz').get_fdata() 
            AD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_AD.nii.gz').get_fdata() 
            value_FA = FA[mask > 0]
            value_MD = MD[mask > 0]
            value_RD = RD[mask > 0]
            value_AD = AD[mask > 0]
            additional['value_FA' + '_' + patient + '_' + atlas] = value_FA
            additional['value_MD' + '_' + patient + '_' + atlas] = value_MD
            additional['value_RD' + '_' + patient + '_' + atlas] = value_RD
            additional['value_AD' + '_' + patient + '_' + atlas] = value_AD
            
    
            group['value_FA' + '_' + atlas] = value_FA
            group['value_MD' + '_' + atlas] = value_MD
            group['value_RD' + '_' + atlas] = value_RD
            group['value_AD' + '_' + atlas] = value_AD
                
            wFA = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wFA.nii.gz').get_fdata() 
            wMD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wMD.nii.gz').get_fdata() 
            wRD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wRD.nii.gz').get_fdata() 
            wAD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wAD.nii.gz').get_fdata() 
            value_wFA = wFA[mask > 0]
            value_wMD = wMD[mask > 0]
            value_wRD = wRD[mask > 0]
            value_wAD = wAD[mask > 0]
            additional['value_wFA' + '_' + patient + '_' + atlas] = value_wFA
            additional['value_wMD' + '_' + patient + '_' + atlas] = value_wMD
            additional['value_wRD' + '_' + patient + '_' + atlas] = value_wRD
            additional['value_wAD' + '_' + patient + '_' + atlas] = value_wAD
            
            
            group['value_wFA' + '_' + atlas] = value_wFA
            group['value_wMD' + '_' + atlas] = value_wMD
            group['value_wRD' + '_' + atlas] = value_wRD
            group['value_wAD' + '_' + atlas] = value_wAD
             
            
            fiso = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fiso.nii.gz').get_fdata() 
            fintra = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fintra.nii.gz').get_fdata() 
            fextra = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fextra.nii.gz').get_fdata()
            ODI = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_odi.nii.gz').get_fdata() 
            value_fiso = fiso[mask > 0]
            value_fintra = fintra[mask > 0]
            value_fextra = fextra[mask > 0]
            value_ODI = ODI[mask > 0]
            
            additional['value_fiso' + '_' + patient + '_' + atlas] = value_fiso
            additional['value_fintra' + '_' + patient + '_' + atlas] = value_fintra
            additional['value_fextra' + '_' + patient + '_' + atlas] = value_fextra
            additional['value_ODI' + '_' + patient + '_' + atlas] = value_ODI
            
            
            group['value_fiso' + '_' + atlas] = value_fiso
            group['value_fintra' + '_' + atlas] = value_fintra
            group['value_fextra' + '_' + atlas] = value_fextra
            group['value_ODI' + '_' + atlas] = value_ODI
            
            wfvf = nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_wfvf.nii.gz').get_fdata() 
            fvf_tot =  nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_fvf_tot.nii.gz').get_fdata() 
            value_wfvf = wfvf[mask > 0]
            value_fvf_tot = fvf_tot[mask > 0]
            
            additional['value_wfvf' + '_' + patient + '_' + atlas] = value_wfvf
            additional['value_fvf_tot' + '_' + patient + '_' + atlas] = value_fvf_tot
            
            
            group['value_wfvf' + '_' + atlas] = value_wfvf
            group['value_fvf_tot' + '_' + atlas] = value_fvf_tot
            
            df['mean_FA' + '_' + atlas][index] = np.mean(value_FA)
            df['var_FA' + '_' + atlas][index] = np.var(value_FA)
            df['mean_MD' + '_' + atlas][index] = np.mean(value_MD)
            df['var_MD' + '_' + atlas][index] = np.var(value_MD)
            df['mean_AD' + '_' + atlas][index] = np.mean(value_AD)
            df['var_AD' + '_' + atlas][index] = np.var(value_AD)
            df['mean_RD' + '_' + atlas][index] = np.mean(value_RD)
            df['var_RD' + '_' + atlas][index] = np.var(value_RD)
            
            df['mean_wFA' + '_' + atlas][index] = np.mean(value_wFA)
            df['var_wFA' + '_' + atlas][index] = np.var(value_wFA)
            df['mean_wMD' + '_' + atlas][index] = np.mean(value_wMD)
            df['var_wMD' + '_' + atlas][index] = np.var(value_wMD)
            df['mean_wAD' + '_' + atlas][index] = np.mean(value_wAD)
            df['var_wAD' + '_' + atlas][index] = np.var(value_wAD)
            df['mean_wRD' + '_' + atlas][index] = np.mean(value_wRD)
            df['var_wRD' + '_' + atlas][index] = np.var(value_wRD)
            
            df['mean_fiso' + '_' + atlas][index] = np.mean(value_fiso)
            df['var_fiso' + '_' + atlas][index] = np.var(value_fiso)
            df['mean_fintra' + '_' + atlas][index] = np.mean(value_fintra)
            df['var_fintra' + '_' + atlas][index] = np.var(value_fintra)
            df['mean_fextra' + '_' + atlas][index] = np.mean(value_fextra)
            df['var_fextra' + '_' + atlas][index] = np.var(value_fextra)
            df['mean_ODI' + '_' + atlas][index] = np.mean(value_ODI)
            df['var_ODI' + '_' + atlas][index] = np.var(value_ODI)
            
            df['mean_wfvf' + '_' + atlas][index] = np.mean(value_wfvf)
            df['var_wfvf' + '_' + atlas][index] = np.var(value_wfvf)
            df['mean_fvf_tot' + '_' + atlas][index] = np.mean(value_fvf_tot)
            df['var_fvf_tot' + '_' + atlas][index] = np.var(value_fvf_tot)
            
            if(df["Pathologie_amyloid"][index]== 1):
                group2 = group2.append(group,ignore_index=True)
            else : 
                group1 = group1.append(group,ignore_index=True)
            
            raw_value = pd.concat([raw_value, additional], axis=1)
            
        grouped_raw_value1 = pd.concat([grouped_raw_value1, group1], axis = 1)
        grouped_raw_value2 = pd.concat([grouped_raw_value2,group2], axis = 1)
       
    grouped_raw_value1.to_csv(study_path + "/grouped1_value.csv")
    grouped_raw_value2.to_csv(study_path + "/grouped2_value.csv")
    df.to_csv(study_path + "/Patient_data.csv")
    raw_value.to_csv(study_path + "/raw_value.csv")
    return 1
    
#%%============================================================================
# Ttest and scatter plots
#==============================================================================

def Ttest_region(study_path, data = 'solo'):
    
    df = pd.read_csv(study_path + "/Patient_data.csv", sep = ',')
    if data == 'solo':
        result = pd.DataFrame()
        labels = list(df.columns[13:])
        group1 = df[df['Pathologie_amyloid'] == 0]
        group2 = df[df['Pathologie_amyloid'] == 1]
        for label in labels :
            result_ttest = sc.ttest_ind(group1[label], group2[label])
            if result_ttest[1] > 0.05:
                keep = False
            else : 
                keep = True
            result = result.append({'Label' : label, 'T_test' : result_ttest[0], 'p-value' :result_ttest[1],'keep_H0' : keep}, ignore_index=True)
        result.to_csv(study_path + '/result_solo.csv')
                 
    if data == 'duo':
        result = pd.DataFrame()
        group1 = pd.read_csv(study_path + '/grouped1_value.csv',sep=',')
        group2 = pd.read_csv(study_path + '/grouped2_value.csv',sep=',')
        labels = list(group1.columns[1:])
        for label in labels:
            result_ttest = sc.ttest_ind(group1[label].dropna(), group2[label].dropna())
            if result_ttest[1] > 0.05:
                keep = False
            else : 
                keep = True
            result = result.append({'Label' : label, 'T_test' : result_ttest[0], 'p-value' :result_ttest[1], 'keep_H0' : keep}, ignore_index=True)
        result.to_csv(study_path + '/result_duo.csv')        
    
    return 1
   
def Ttest_voxel(study_path, atlas_list, patient_list):
    result = pd.DataFrame()
    df = pd.read_csv(study_path + "/Patient_data.csv", sep = ',')
    index1 = df['Pathologie_amyloid'] == 0
    index2 = df['Pathologie_amyloid'] == 1
    for atlas in atlas_list:
        matrix = pd.DataFrame()
        for patient in patient_list : 
            mask, affine_mask, img_mask = load_nifti(study_path + patient + '/transformed/' + patient + '_' + atlas + '.nii.gz', return_img=True)
            FA = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_FA.nii.gz').get_fdata() 
            MD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_MD.nii.gz').get_fdata() 
            RD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_RD.nii.gz').get_fdata() 
            AD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_AD.nii.gz').get_fdata() 
            value_FA = FA*mask
            value_MD = MD*mask
            value_RD = RD*mask
            value_AD = AD*mask
            
            wFA = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wFA.nii.gz').get_fdata() 
            wMD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wMD.nii.gz').get_fdata() 
            wRD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wRD.nii.gz').get_fdata() 
            wAD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wAD.nii.gz').get_fdata() 
            value_wFA = wFA*mask
            value_wMD = wMD*mask
            value_wRD = wRD*mask
            value_wAD = wAD*mask    
            
            fiso = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fiso.nii.gz').get_fdata() 
            fintra = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fintra.nii.gz').get_fdata() 
            fextra = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fextra.nii.gz').get_fdata()
            ODI = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_odi.nii.gz').get_fdata() 
            value_fiso = fiso*mask
            value_fintra = fintra*mask
            value_fextra = fextra*mask
            value_ODI = ODI*mask
        
            wfvf = nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_wfvf.nii.gz').get_fdata() 
            fvf_tot =  nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_fvf_tot.nii.gz').get_fdata() 
            value_wfvf = wfvf*mask
            value_fvf_tot = fvf_tot*mask
            
            matrix = matrix.append({'FA' + '_' + atlas : value_FA, 'MD' + '_'  + atlas : value_MD, 'RD' + '_'  + atlas : value_RD, 'AD' + '_'  + atlas : value_AD , 'wFA' + '_' + atlas : value_wFA, 'wMD' + '_'  + atlas : value_wMD, 'wRD' + '_'  + atlas : value_wRD, 'wAD' + '_'  + atlas : value_wAD , 'fiso' + '_' + atlas : value_fiso, 'fintra' + '_' + atlas : value_fintra, 'fextra' + '_' + atlas : value_fextra, 'ODI' + '_'  + atlas : value_ODI, 'wfvf' + '_'  + atlas : value_wfvf, 'fvf_tot' + '_'  + atlas : value_fvf_tot}, ignore_index=True)
        print(matrix)
        for label in matrix.columns:
            t, p = sc.ttest_ind(matrix[label][index1], matrix[label][index2])
            result = result.append({'Label' : label, 'T_test': t, 'p-value' : p, 'Significant' : p < 0.05}, ignore_index=True)
    result.to_csv(study_path + '/result_voxel.csv')
    
    return 1
    
def Ttest_volume(study_path, atlas_list, patient_list):
    result = pd.DataFrame()
    volume = pd.DataFrame()
    for atlas in atlas_list:
        volume_tmp = pd.DataFrame()
        for patient in patient_list : 
            mask, affine_mask, img_mask = load_nifti(study_path + patient + '/transformed/' + patient + '_' + atlas + '.nii.gz', return_img=True)
            FA = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_FA.nii.gz').get_fdata() 
            MD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_MD.nii.gz').get_fdata() 
            RD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_RD.nii.gz').get_fdata() 
            AD = nib.load(study_path + patient + '/dMRI/microstructure/dti/' + patient + '_AD.nii.gz').get_fdata() 
            volume_FA = np.count_nonzero(FA*mask)
            volume_MD = np.count_nonzero(MD*mask)
            volume_RD = np.count_nonzero(RD*mask)
            volume_AD = np.count_nonzero(AD*mask)
            
            wFA = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wFA.nii.gz').get_fdata() 
            wMD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wMD.nii.gz').get_fdata() 
            wRD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wRD.nii.gz').get_fdata() 
            wAD = nib.load(study_path + patient + '/dMRI/microstructure/diamond/' + patient + '_wAD.nii.gz').get_fdata() 
            volume_wFA = np.count_nonzero(wFA*mask)
            volume_wMD = np.count_nonzero(wMD*mask)
            volume_wRD = np.count_nonzero(wRD*mask)
            volume_wAD = np.count_nonzero(wAD*mask)
            
            fiso = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fiso.nii.gz').get_fdata() 
            fintra = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fintra.nii.gz').get_fdata() 
            fextra = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_fextra.nii.gz').get_fdata()
            ODI = nib.load(study_path + patient + '/dMRI/microstructure/noddi/' + patient + '_noddi_odi.nii.gz').get_fdata() 
            volume_fiso = np.count_nonzero(fiso*mask)
            volume_fintra = np.count_nonzero(fintra*mask)
            volume_fextra = np.count_nonzero(fextra*mask)
            volume_ODI = np.count_nonzero(ODI*mask)
        
            wfvf = nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_wfvf.nii.gz').get_fdata() 
            fvf_tot =  nib.load(study_path + patient + '/dMRI/microstructure/mf/' + patient + '_mf_fvf_tot.nii.gz').get_fdata() 
            volume_wfvf = np.count_nonzero(wfvf*mask)
            volume_fvf_tot = np.count_nonzero(fvf_tot*mask)
            
            volume_tmp = volume_tmp.append({'FA' + '_' + atlas : volume_FA, 'MD' + '_'  + atlas : volume_MD, 'RD' + '_'  + atlas : volume_RD, 'AD' + '_'  + atlas : volume_AD , 'wFA' + '_' + atlas : volume_wFA, 'wMD' + '_'  + atlas : volume_wMD, 'wRD' + '_'  + atlas : volume_wRD, 'wAD' + '_'  + atlas : volume_wAD , 'fiso' + '_' + atlas : volume_fiso, 'fintra' + '_' + atlas : volume_fintra, 'fextra' + '_' + atlas : volume_fextra, 'ODI' + '_'  + atlas : volume_ODI, 'wfvf' + '_'  + atlas : volume_wfvf, 'fvf_tot' + '_'  + atlas : volume_fvf_tot}, ignore_index=True)
        volume = pd.concat([volume, volume_tmp], axis = 1)
     
    df = pd.read_csv(study_path + "/Patient_data.csv", sep = ',')
    index1 = df['Pathologie_amyloid'] == 0
    index2 = df['Pathologie_amyloid'] == 1
    volume.to_csv(study_path + '/volume.csv') 
    print(volume)
    print(len(volume))
    print(len(index1))
    for label in volume.columns:
        t, p = sc.ttest_ind(volume[label][index1], volume[label][index2],equal_var=False)
        stat, ps = sc.mannwhitneyu(volume[label][index1], volume[label][index2])
        result = result.append({'Label' : label, 'T_test': t, 'p-value T' : p, 'Significant T' : p < 0.05, 'Mann-Whithney' : stat, 'p-value MW' : ps, 'Significant MW' : ps < 0.05}, ignore_index=True)
   
    result.to_csv(study_path + '/result_volume.csv')
    return 1

def graph_plot(study_path):
    df = pd.read_csv(study_path + "/Patient_data.csv", sep = ',')  
    labels = list(df.columns[13:])
    df['Column_with_Color'] = df['Pathologie_amyloid'].map({0: 'r', 1: 'g'})
    if not os.path.exists(study_path + '/Plots'):
        os.makedirs(study_path + '/Plots')
    for label in labels:
        plot = df.plot.scatter(x = 'Pathologie_amyloid', y = label, c = df['Column_with_Color'], title = label)
        plot.figure.savefig(study_path + '/Plots/' + 'plot' + '_' + label + '.png')
    return 1 

#%%============================================================================
# Main
#==============================================================================

def main(args):
    print(args)
    study_path = args[1]
    number_of_patients = int(args[2])
    patient_list = []
    for i in range(3, 3 + number_of_patients):
        patient_list.append(args[i])
    number_of_atlas = int(args[3 + number_of_patients])
    atlas_list = []
    for i in range(4 + number_of_patients, 4 + number_of_patients + number_of_atlas):
        atlas_list.append(args[i])
    statistic(study_path, patient_list, atlas_list)
    Ttest_region(study_path, 'solo')
    Ttest_region(study_path, 'duo')
    #Ttest_voxel(study_path, atlas_list, patient_list)
    Ttest_volume(study_path, atlas_list, patient_list)
    graph_plot(study_path)

    return 1

if __name__ == "__main__":
    main(sys.argv)
    
#%%============================================================================
# Affichage
#==============================================================================

study_path = 'D:/Only_denoising/'

patient_data = pd.read_csv(study_path + 'Patient_data.csv', sep = ',') #mean and variance of metrics and other parameters for each patients 
result_solo = pd.read_csv(study_path + 'result_solo.csv', sep = ',') # result of ttest from patient_data mean and var and group
result_duo = pd.read_csv(study_path + 'result_duo.csv', sep = ',') #result of ttest from grouped values 
result_volume = pd.read_csv(study_path + 'result_volume.csv', sep = ',') #result of ttest between volume in groups