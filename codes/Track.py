# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 12:35:31 2022

@author: Nicolas Indriets
"""

from dipy.core.gradients import gradient_table
from dipy.data import get_fnames
from dipy.io.gradients import read_bvals_bvecs
from dipy.io.image import load_nifti, load_nifti_data
from dipy.reconst.csdeconv import (ConstrainedSphericalDeconvModel,
                                   auto_response_ssst)
from dipy.tracking import utils
from dipy.tracking.local_tracking import LocalTracking
from dipy.tracking.streamline import Streamlines
from dipy.tracking.stopping_criterion import ThresholdStoppingCriterion
from dipy.reconst.shm import CsaOdfModel
from dipy.direction import ProbabilisticDirectionGetter
from dipy.data import small_sphere
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.streamline import save_trk
from dipy.data import default_sphere
import sys
import os

#%%============================================================================
# Tracking
#==============================================================================


def tracking(study_path, patient_list,atlas_list, atlas_bool):
  
  for patient in patient_list : 
      data_path = study_path + patient + '/dMRI/preproc/' + patient + '_dmri_preproc.nii.gz'
      bval_path = study_path + patient + '/dMRI/preproc/' + patient + '_dmri_preproc.bval'
      bvec_path = study_path + patient + '/dMRI/preproc/' + patient + '_dmri_preproc.bvec'
      
        
      data, affine, img = load_nifti(data_path, return_img=True)
      bvals, bvecs = read_bvals_bvecs(bval_path, bvec_path)
      gtab = gradient_table(bvals, bvecs)
      
      if atlas_bool == 1 : 
        for atlas in atlas_list:
            brain_path = study_path + patient + '/transformed/' + patient + '_' + atlas +'.nii.gz'
            seed_mask, _ , _ = load_nifti(brain_path, return_img=True)
            mask, _ , _ = load_nifti(brain_path, return_img=True)
            seeds = utils.seeds_from_mask(seed_mask, affine, density=1)
            
            response, ratio = auto_response_ssst(gtab, data, roi_radii=10, fa_thr=0.7)
            csd_model = ConstrainedSphericalDeconvModel(gtab, response, sh_order=6)
            csd_fit = csd_model.fit(data, mask=mask)
            
            csa_model = CsaOdfModel(gtab, sh_order=6)
            gfa = csa_model.fit(data, mask=mask).gfa
            stopping_criterion = ThresholdStoppingCriterion(gfa, .25)
            
            prob_dg = ProbabilisticDirectionGetter.from_shcoeff(csd_fit.shm_coeff,
                                                                max_angle=30.,
                                                                sphere=default_sphere)
            streamline_generator = LocalTracking(prob_dg, stopping_criterion, seeds,
                                                 affine, step_size=.5)
            streamlines = Streamlines(streamline_generator)
            sft = StatefulTractogram(streamlines, img, Space.RASMM)
            if not os.path.exists( study_path + patient + '/tracking/'):
              os.makedirs( study_path + patient + '/tracking/')
            save_trk(sft, study_path + patient + '/tracking/' + patient + '_' + atlas + '_track.trk')
            
      else : 
        brain_path = study_path + patient + '/masks/' + patient + '_wm_mask_AP.nii.gz'
        seed_mask, _ , _ = load_nifti(brain_path, return_img=True)
        mask, _ , _ = load_nifti(brain_path, return_img=True)
        seeds = utils.seeds_from_mask(seed_mask, affine, density=1)
        
        response, ratio = auto_response_ssst(gtab, data, roi_radii=10, fa_thr=0.7)
        csd_model = ConstrainedSphericalDeconvModel(gtab, response, sh_order=6)
        csd_fit = csd_model.fit(data, mask=mask)
        
        csa_model = CsaOdfModel(gtab, sh_order=6)
        gfa = csa_model.fit(data, mask=mask).gfa
        stopping_criterion = ThresholdStoppingCriterion(gfa, .25)
         
        
        prob_dg = ProbabilisticDirectionGetter.from_shcoeff(csd_fit.shm_coeff,
                                                            max_angle=30.,
                                                            sphere=default_sphere)
        streamline_generator = LocalTracking(prob_dg, stopping_criterion, seeds,
                                             affine, step_size=.5)
        streamlines = Streamlines(streamline_generator)
        sft = StatefulTractogram(streamlines, img, Space.RASMM)
        if not os.path.exists( study_path + patient + '/tracking/'):
          os.makedirs( study_path + patient + '/tracking/')
        save_trk(sft, study_path + patient + '/tracking/' + patient + '_wm_track.trk')
    
  return 1
        

#%%============================================================================
# Main
#==============================================================================        
        
def main(args):
    print(args)
    study_path = args[1]
    atlas_bool = int(args[2])
    number_of_atlas = int(args[3])
    atlas_list = []
    for i in range(4, 4+number_of_atlas):
      atlas_list.append(args[i])
    number_of_patients = int(args[4 + number_of_atlas])
    patient_list = []
    for i in range(5 + number_of_atlas , 5 + number_of_atlas + number_of_patients):
        patient_list.append(args[i])
    
    track = tracking(study_path, patient_list, atlas_list, atlas_bool) 
    return 1

if __name__ == "__main__":
    main(sys.argv)
