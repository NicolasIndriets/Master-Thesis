# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 17:46:56 2023

@author: Nicolas Indriets
"""

import os 
import numpy as np
import pandas as pd
import sys
from dipy.io.image import load_nifti, save_nifti
import nibabel as nib
from os.path import join as pjoin
from dipy.viz import regtools
from dipy.io.image import load_nifti, save_nifti
from dipy.align.imaffine import AffineMap

#%% ===========================================================================
# Create atlas from csv files and nifti files with labels
#==============================================================================


data = pd.read_csv("D:/Atlas_Maps/Atlas_Maps/atlas_desikan_killiany.csv")
data_nifti, affine, img = load_nifti("D:/Atlas_Maps/Atlas_Maps/atlas_desikan_killiany_resampled.nii.gz", return_img=True)
data.info()
for i in range(len(data["index"])): 
    atlas = np.zeros(data_nifti.shape)
    atlas[data_nifti == data["index"][i]] = 1
    save_nifti("D:/Atlas_Maps/Atlas_Maps/Desikan_Killiany/" + data["name"][i] +".nii.gz", atlas.astype(np.float32),affine)

#%% ===========================================================================
# Resampled Atlas nifti into T1 dimensions
#==============================================================================

folder = "D:/Atlas_Maps/Atlas_Maps"
static_data, static_affine, static_img = load_nifti(
                                            pjoin(folder, 'MNI152_T1_1mm_brain.nii.gz'),
                                            return_img=True)
static = static_data
static_grid2world = static_affine

moving_data, moving_affine, moving_img = load_nifti(
                                            pjoin(folder, 'atlas_desikan_killiany.nii.gz'),
                                            return_img=True)
moving = moving_data
moving_grid2world = moving_affine

identity = np.eye(4)
affine_map = AffineMap(identity,
                       static.shape, static_grid2world,
                       moving.shape, moving_grid2world)
print(affine_map.affine)
resampled = affine_map.transform(moving)
regtools.overlay_slices(static, resampled, None, 0,
                        "Static", "Moving", "resampled_0.png")
regtools.overlay_slices(static, resampled, None, 1,
                        "Static", "Moving", "resampled_1.png")
regtools.overlay_slices(static, resampled, None, 2,
                        "Static", "Moving", "resampled_2.png")

save_nifti("D:/Atlas_Maps/Atlas_Maps/atlas_desikan_killiany_resampled.nii.gz", resampled.astype(np.float32),static_affine)
