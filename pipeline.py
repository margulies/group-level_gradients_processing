#!/bin/python

import sys, os
sys.path.append("/network/lustre/iss01/home/daniel.margulies/data/lsd/")
from load_fs import load_fs
import numpy as np
import nibabel as nib
from mapalign import embed
from numba import jit
from scipy.sparse.linalg import eigsh
from scipy import sparse

@jit(parallel=True)
def run_perc(data, thresh):
    perc_all = np.zeros(data.shape[0])
    for n,i in enumerate(data):
        data[n, i < np.percentile(i, thresh)] = 0.
    for n,i in enumerate(data):
        data[n, i < 0.] = 0.
    return data

def main(s):

    import os.path

    if os.path.isfile('/network/lustre/iss01/home/daniel.margulies/data/lsd/embedding/embedding_dense_emb.%s.npy' % s):

        emb = np.load('/network/lustre/iss01/home/daniel.margulies/data/lsd/embedding/embedding_dense_emb.%s.npy' % s)

    else:

        K = load_fs(s)
        K[np.isnan(K)] = 0.0

        A_mA = K - K.mean(1)[:,None]
        ssA = (A_mA**2).sum(1)
        Asq = np.sqrt(np.dot(ssA[:,None],ssA[None]))
        Adot = A_mA.dot(A_mA.T)

        K = Adot/Asq
        del A_mA, ssA, Asq, Adot
        K = run_perc(K, 90)

        norm = (K * K).sum(0, keepdims=True) ** .5
        K = K.T @ K
        aff = K / norm / norm.T
        del norm, K
        #aff = sparse.csr_matrix(aff)

        emb, res = embed.compute_diffusion_map(aff, alpha = 0.5, n_components=5, skip_checks=True, overwrite=True, eigen_solver=eigsh, return_result=True)
        del aff

        np.save('/network/lustre/iss01/home/daniel.margulies/data/lsd/embedding/embedding_dense_emb.%s.npy' % s, emb)
        np.save('/network/lustre/iss01/home/daniel.margulies/data/lsd/embedding/embedding_dense_res.%s.npy' % s, res)

if __name__ == "__main__":
    main(sys.argv[1])
