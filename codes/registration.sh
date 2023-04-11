#!/bin/bash
# Submission script for Manneback
#SBATCH --job-name=registration
#SBATCH --array=0-65
#SBATCH --time=01:00:00 # hh:mm:ss
#
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=5000 # megabytes
#SBATCH --partition=cp3,Def,keira,gpu
#
#SBATCH --mail-user=nicolas.indriets@student.uclouvain.be
#SBATCH --mail-type=ALL
#
#SBATCH --output=registration.out

PATIENTS_PATH="/CECI/trsf/users/i/n/indriets/Subjects/subjects/"

STATIC_REF_FILE="/CECI/trsf/users/i/n/indriets/Atlas_Maps/Atlas_Maps/"

ATLAS_SUB_FOLD="Desikan_Killiany" # "-" #Harvard #Harvard_cortex #XTRACT #Desikan_Killiany

NUM_FILES=12

FILES=("ctx-rh-entorhinal" "ctx-lh-entorhinal" "ctx-lh-isthmuscingulate" "ctx-rh-isthmuscingulate" "ctx-lh-posteriorcingulate" "ctx-rh-posteriorcingulate" "ctx-lh-parahippocampal" "ctx-rh-parahippocampal" "Left-Amygdala" "Right-Amygdala" "Left-Hippocampus" "Right-Hippocampus") 
#"00Average_Brain" 
#"FSL_HCP1065_FA_1mm" 
#"harvardoxford-subcortical_prob_Left Amygdala" "harvardoxford-subcortical_prob_Right Amygdala" "harvardoxford-subcortical_prob_Left Hippocampus" "harvardoxford-subcortical_prob_Right Hippocampus" 
#"harvardoxford-cortical_prob_Parahippocampal_Gyrus_anterior" "harvardoxford-cortical_prob_Parahippocampal_Gyrus_posterior" "harvardoxford-cortical_prob_Cingulate_Gyrus_anterior" "harvardoxford-cortical_prob_Cingulate_Gyrus_posterior" 
#"xtract_prob_Cingulum_subsection_Dorsal_L" "xtract_prob_Cingulum_subsection_Dorsal_R" "xtract_prob_Cingulum_subsection_Peri-genual_L" "xtract_prob_Cingulum_subsection_Peri-genual_R" "xtract_prob_Cingulum_subsection_Temporal_L" "xtract_prob_Cingulum_subsection_Temporal_R"

#"MNI152_T1_1mm_brain_float"
#"ctx-rh-entorhinal" "ctx-lh-entorhinal" "ctx-lh-isthmuscingulate" "ctx-rh-isthmuscingulate" "ctx-lh-posteriorcingulate" "ctx-rh-posteriorcingulate" "ctx-lh-parahippocampal" "ctx-rh-parahippocampal" "Left-Amygdala" "Right-Amygdala" "Left-Hippocampus" "Right-Hippocampus"

NUM_PATIENTS=1
#["sub-009","sub-013","sub-014","sub-017","sub-018","sub-020","sub-021","sub-025","sub-026","sub-028","sub-032","sub-033","sub-036","sub-037","sub-038","sub-040","sub-041","sub-042","sub-043","sub-044","sub-046","sub-047","sub-048","sub-049","sub-050","sub-051","sub-052","sub-054","sub-055","sub-056","sub-057","sub-059","sub-060","sub-061","sub-062","sub-063","sub-064","sub-065","sub-066","sub-067","sub-068","sub-069","sub-070","sub-071","sub-073","sub-076","sub-077","sub-078","sub-084","sub-085","sub-086","sub-093","sub-098","sub-103","sub-104","sub-106","sub-108","sub-110","sub-117","sub-121","sub-132","sub-134","sub-135","sub-145","sub-148"]
#["sub-013","sub-018","sub-044","sub-056","sub-061","sub-068","sub-070","sub-071","sub-076","sub-093","sub-098","sub-106","sub-145"]

PATIENTS=("sub-013" "sub-018" "sub-044" "sub-056" "sub-061" "sub-068" "sub-070" "sub-071" "sub-076" "sub-093" "sub-098" "sub-106" "sub-145" "sub-009" "sub-014" "sub-017" "sub-020" "sub-021" "sub-025" "sub-026" "sub-028" "sub-032" "sub-033" "sub-036" "sub-037" "sub-038" "sub-040" "sub-041" "sub-042" "sub-043" "sub-046" "sub-047" "sub-048" "sub-049" "sub-050" "sub-051" "sub-052" "sub-054" "sub-055" "sub-057" "sub-059" "sub-060" "sub-062" "sub-063" "sub-064" "sub-065" "sub-066" "sub-067" "sub-069" "sub-073" "sub-077" "sub-078" "sub-084" "sub-085" "sub-086" "sub-103" "sub-104" "sub-108" "sub-110" "sub-117" "sub-121" "sub-132" "sub-134" "sub-135" "sub-148") 

FA=0

GETMAP=0

srun python3 ./registration_fixedPatient.py $PATIENTS_PATH $STATIC_REF_FILE $ATLAS_SUB_FOLD $NUM_FILES ${FILES[@]} $NUM_PATIENTS ${PATIENTS[$SLURM_ARRAY_TASK_ID]} $FA $GETMAP
echo "Task ID: $SLURM_ARRAY_TASK_ID"