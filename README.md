# To run:

## Requirements:

FreeSurfer/6.0.0
python/3.6+

### Python packages:
nibabel
numpy
numba
scipy
https://www.github.com/satra/mapalign

## Processing steps:

### 1. Project volume to surface using FreeSurfer:

Currently set to project from MNI space, but could also be modified for
native spaces. 

    #!/bin/bash

    while read subject;
    do
      ./x.mri_vol2surf.sh ${subject}
    done <subject_list.txt

### 2. Correlate RS data across sessions and embed

This command will call `load_fs.py` to read in the data.
This is the most time consuming step, but the script has some fancy numpy
optimizations to speed it up dramatically.

    #!/bin/bash

    while read subject;
    do
      python pipeline.py ${subject}
    done <subject_list.txt

### 3. Rotate embeddings across individuals to match

Need to set the path to the `subject_list.txt` file.

    python combine_subjects.py

A single file with all individual embeddings is created that can be read into
another software for group-level analyses.
