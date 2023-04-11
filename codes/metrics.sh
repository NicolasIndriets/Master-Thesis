#!/bin/bash
# 
#SBATCH --job-name=metrics
#SBATCH --array=0-64
#SBATCH --time=00:20:00 # hh:mm:ss
#
#SBATCH --ntasks=1
#SBATCH --mem-per-cpu=5000 # megabytes
#SBATCH --partition=cp3,Def,keira,gpu
#
#SBATCH --mail-user=nicolas.indriets@student.uclouvain.be
#SBATCH --mail-type=ALL
#
#SBATCH --output=metrics.out

PATIENTS_PATH="/CECI/trsf/users/i/n/indriets/Subjects/subjects/"

NUM_PATIENTS=1

PATIENTS=("sub-040" "sub-013" "sub-018" "sub-044" "sub-056" "sub-061" "sub-068" "sub-070" "sub-071" "sub-076" "sub-093" "sub-098" "sub-106" "sub-145" "sub-009" "sub-014" "sub-017" "sub-020" "sub-021" "sub-025" "sub-026" "sub-028" "sub-032" "sub-033" "sub-036" "sub-037" "sub-038" "sub-040" "sub-041" "sub-042" "sub-043" "sub-046" "sub-047" "sub-048" "sub-049" "sub-050" "sub-051" "sub-052" "sub-054" "sub-055" "sub-057" "sub-059" "sub-060" "sub-062" "sub-063" "sub-064" "sub-065" "sub-066" "sub-067" "sub-069" "sub-073" "sub-077" "sub-078" "sub-084" "sub-085" "sub-086" "sub-103" "sub-104" "sub-108" "sub-110" "sub-117" "sub-121" "sub-132" "sub-134" "sub-135" "sub-148") 

srun python3 ./Metrics.py $PATIENTS_PATH $NUM_PATIENTS ${PATIENTS[$SLURM_ARRAY_TASK_ID]}
echo "Task ID: $SLURM_ARRAY_TASK_ID"