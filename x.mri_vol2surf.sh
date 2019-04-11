#!/bin/bash

# For loading on server. Can remove if software already installed locally
module load FreeSurfer/6.0.0
module load FSL

export SUBJECTS_DIR=/network/lustre/iss01/home/daniel.margulies/data/lsd/freesurfer

subject=${1}
dir=/network/lustre/iss01/home/daniel.margulies/data/lsd/derivatives

for scan in _ses-02_task-rest_acq-AP_run-01 _ses-02_task-rest_acq-AP_run-02 _ses-02_task-rest_acq-PA_run-01 _ses-02_task-rest_acq-PA_run-02
do

#fslmaths ${dir}/${subject}/func/${subject}${scan}_native.nii.gz -Tmean ${dir}/${subject}/func/${subject}${scan}_native_avg.nii.gz
#done
#fslmerge -t ${dir}/${subject}/func/${subject}_example_all.nii.gz ${dir}/${subject}/func/${subject}*_native_avg.nii.gz

#fslmaths ${dir}/${subject}/func/${subject}_example_all.nii.gz -Tmean ${dir}/${subject}/func/${subject}_example.nii.gz

#bbregister \
#  --mov ${dir}/${subject}/func/${subject}${scan}_native_avg.nii.gz \
#  --bold \
#  --s ${subject} \
#  --init-fsl \
#  --reg ${dir}/${subject}/func/${subject}${scan}_example2fs.dat \
#  --o ${dir}/${subject}/func/${subject}${scan}_rs_example2fs.nii.gz

for hemi in lh rh
do

#   --srcsubject ${subject} \
#   --reg ${dir}/${subject}/func/${subject}${scan}_example2fs.dat \
#   --sd $SUBJECTS_DIR  \

# To run from MRI space:
mri_vol2surf --mov ${dir}/${subject}/func/${subject}${scan}_MNI2mm.nii.gz \
  --mni152reg \
  --projfrac-avg 0.2 0.8 0.1 \
  --trgsubject fsaverage5 \
  --interp nearest \
  --hemi ${hemi} \
  --surf-fwhm 6.0 --cortex --noreshape \
  --o ${dir}/${subject}/func/${subject}${scan}.fsa5.${hemi}.mgz

done

done
