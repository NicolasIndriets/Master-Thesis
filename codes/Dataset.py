# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 16:07:19 2023

@author: Nicolas Indriets
"""
import os 
import numpy as np
import pandas as pd
import sys
from dipy.io.image import load_nifti, save_nifti
import nibabel as nib

#%%============================================================================
# Creating .csv files with data
#==============================================================================

data_pet_tau = pd.read_csv("D:/data_extraction_F6.0.0_petsurfer_tau_pvc_fdg_nopvc_pvc.tsv",sep="\t")
data_pet_tau = data_pet_tau.shift(periods=1, axis=1)
data_pet_tau["subjectname1"] = data_pet_tau["subjectname2"]

data_DG_neuro = pd.read_excel("D:/TAU_Dg neuro complet_FINAL_July_2022.xlsx")
data_subject = pd.read_excel("D:/patient_DATA.xlsx")

preproc_complete = []
for i in range(len(data_subject["Patient ID"])): 
    if data_subject["Patient ID"][i] in [13,18,44,56,61,68,70,71,76,93,98,106,145]:
        preproc_complete.append("no")
    else : 
        preproc_complete.append("yes")
df = data_subject.assign(Preproc_complete=preproc_complete)

index = []
for i in range(len(data_subject["Patient ID"])): 
    for j in range(len(data_DG_neuro)):
        if data_subject["Patient ID"][i] == data_DG_neuro["ID"][j]:
            index.append(j)
age = np.array(data_DG_neuro["AGE_cog_assessment"][index])
df = df.assign(Age=age)

gender = np.array(data_DG_neuro["Gender"][index])
df = df.assign(Gender=gender)

education = np.array(data_DG_neuro["Education_NSC"][index])
df = df.assign(Education=education)

mmse = np.array(data_DG_neuro["MMSE"][index])
df = df.assign(MMSE=mmse)

amyloid = np.array(data_DG_neuro["Beta-amyloïde 1-42 (pg/mL) Seuil = 437"][index])
df = df.assign(Beta_amyloïd=amyloid)

centiloid = np.array(data_DG_neuro["PET Flutemetamol centiloid"][index])
df = df.assign(Centiloid = centiloid)

path_amyloid = np.zeros(amyloid.shape) 
for i in range(len(amyloid)): 
    if(amyloid[i] == "/"):
        if(float(centiloid[i] > 26)): 
            path_amyloid[i] = 1 
    else :
        if(float(amyloid[i])<437): 
            path_amyloid[i] = 1
df = df.assign(Pathologie_amyloid=path_amyloid)

fdg = []
assign = False
for i in range(len(data_subject["Patient ID"])): 
    for j in data_pet_tau["subjectname1"]:
        if data_subject["Patient ID"][i] == j:
            fdg.append("yes")
            assign = True
            break
    if assign != True:
        fdg.append("no")
    else : 
        assign = False
df = df.assign(FDG_data_available=fdg)


df.to_csv("D:/Patient_data.csv")

#%% ===========================================================================
# Adding metrics 
#==============================================================================




