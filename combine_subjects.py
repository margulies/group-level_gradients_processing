import nibabel as nib
import numpy as np
import os, glob

def run_realign(emb, tar, firstpass = False):
    realign = []
    if firstpass:
        realign.append(tar)
    for i, embedding in enumerate(emb):
        u, s, v = np.linalg.svd(tar.T.dot(embedding), full_matrices=False)
        xfm = v.T.dot(u.T)
        realign.append(embedding.dot(xfm))
    return realign

embeddings = []
subs = []
import pandas as pd
df = pd.read_csv('/network/lustre/iss01/home/daniel.margulies/data/lsd/subjects.txt')
sublist = np.asarray(df).flatten()
for s in sublist:
    try:
        subs.append(s)
        embeddings.append(np.load('/network/lustre/iss01/home/daniel.margulies/data/lsd/embedding/embedding_dense_emb.%s.npy' % s))
    except:
        print(s)

realigned = run_realign(embeddings[1:], embeddings[0], firstpass=True)
for i in range(5):
    realigned = run_realign(realigned, np.asarray(np.mean(realigned, axis=0).squeeze()))

from scipy.io import savemat
savemat('/network/lustre/iss01/home/daniel.margulies/data/lsd/group_embedding.mat', mdict={'emb': realigned, 'subs': subs})
