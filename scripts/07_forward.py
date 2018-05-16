"""
Create a source space by morphing the fsaverage brain to the current subject.
Then, compute forward solution based on this source space.

Author: Marijn van Vliet <w.m.vanvliet@gmail.com>
"""
from __future__ import print_function
import argparse
import mne

from config import fname, min_skull_dist, n_jobs

# Be verbose
mne.set_log_level('INFO')

# Handle command line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('subject', metavar='sub###', help='The subject to process')
args = parser.parse_args()
subject = args.subject
print('Processing subject:', subject)

fsaverage = mne.read_source_spaces(fname.fsaverage_src)

# Morph the source space to the current subject
subject_src = mne.morph_source_spaces(fsaverage, subject,
                                      subjects_dir=fname.subjects_dir)

# Save the source space
mne.write_source_spaces(fname.src(subject=subject), subject_src,
                        overwrite=True)

# Create the forward model. We use a single layer BEM model for this.
bem_model = mne.make_bem_model(subject, ico=4, subjects_dir=fname.subjects_dir,
                               conductivity=(0.3,))
bem = mne.make_bem_solution(bem_model)
info = mne.io.read_info(fname.epo(subject=subject))
fwd = mne.make_forward_solution(
    info,
    trans=fname.trans(subject=subject),
    src=subject_src,
    bem=bem,
    meg=True,
    eeg=False,
    mindist=min_skull_dist,
    n_jobs=n_jobs
)

mne.write_forward_solution(fname.fwd(subject=subject), fwd,
                           overwrite=True)
