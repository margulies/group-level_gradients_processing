

def load_fs(subject):

    import nibabel as nib
    import numpy as np

    dir1 = '/network/lustre/iss01/home/daniel.margulies/data/lsd'
    data_all = [] 
    for d in ['AP', 'PA']:
        for s in [1,2]:

            h = 'lh'
            data_lh = nib.load('%s/derivatives/%s/func/%s_ses-02_task-rest_acq-%s_run-0%i.fsa5.%s.mgz' % (dir1,subject,subject,d,s,h)).get_data().squeeze()
            lab_lh = nib.freesurfer.read_label('%s/freesurfer/fsaverage5/label/%s.cortex.label' % (dir1,h))

            h = 'rh'
            data_rh = nib.load('%s/derivatives/%s/func/%s_ses-02_task-rest_acq-%s_run-0%i.fsa5.%s.mgz' % (dir1,subject,subject,d,s,h)).get_data().squeeze()
            lab_rh = nib.freesurfer.read_label('%s/freesurfer/fsaverage5/label/%s.cortex.label' % (dir1,h))


            data = np.vstack((data_lh[lab_lh,:],data_rh[lab_rh,:]))
            data = (data.T - np.nanmean(data, axis = 1)).T
            data = (data.T / np.nanstd(data, axis = 1)).T
            if len(data_all) == 0:
                data_all = data.copy()
            else:
                data_all = np.hstack((data_all, data))
            del data

    return data_all

