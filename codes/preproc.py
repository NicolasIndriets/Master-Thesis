# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 14:58:36 2022

@author: Nicolas Indriets inspired from Manon Dausort 
"""

import elikopy
import elikopy.utils
from elikopy.individual_subject_processing import report_solo

f_path = "/home/users/i/n/indriets/sub-009/ses-01/"

patient_list = ["sub-009"]
study = elikopy.core.Elikopy(f_path, slurm = True, slurm_email = 'nicolas.indriets@student.uclouvain.be', cuda = False)

# =============================================================================
# Patient list
# =============================================================================
study.patient_list()


# =============================================================================
# Preprocessing
# =============================================================================
study.preproc(eddy=True,topup=True,denoising=True, reslice=False, gibbs=False, biasfield=False,patient_list_m=patient_list, qc_reg=False, starting_state=None, report=True)

# =============================================================================
# Mask de matière blanche
# =============================================================================
#study.white_mask("wm_mask_AP",patient_list_m=patient_list, corr_gibbs=True, cpus=2, debug=False) # Done wm_mask_FSL_T1, maskType in ["wm_mask_AP", "wm_mask_FSL_T1"]
   
# =============================================================================
# Modèles microstructuraux
# =============================================================================
#study.dti(patient_list_m=patient_list) # Done
#study.odf_msmtcsd(num_peaks=2, peaks_threshold=0.25, patient_list_m=patient_list) # Done
#study.noddi(patient_list_m=patient_list, cpus=4) # Done
#study.diamond(patient_list_m=patient_list,slurm_timeout="30:00:00",cpus=8)



# =============================================================================
# Statistiques
# =============================================================================
# grp1=[1]
# grp2=[2]



# study.regall_FA(grp1=grp1,grp2=grp2, registration_type="-T", postreg_type="-S", prestats_treshold=0.2, cpus=8)



# metrics={'_noddi_odi':'noddi','_mf_fvf_tot':'mf'}
# study.regall(grp1=grp1,grp2=grp2, metrics_dic=metrics)
# study.randomise_all(randomise_numberofpermutation=0,skeletonised=True,metrics_dic=metrics,regionWiseMean=True,cpus=1,slurm_timeout="1:00:00")


# =============================================================================
# Export
# =============================================================================
study.export(tractography=False, raw=False, preprocessing=True, dti=False, noddi=False, diamond=False, mf=False, wm_mask=False, report=False, preprocessed_first_b0=False, patient_list_m=None)
elikopy.utils.merge_all_reports(f_path)



