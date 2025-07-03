import os, shutil
import tempfile

from epigame.connectivity import run_connectivity_matrices, preprocess_from_mat
from epigame.connectivity import REc, struct

# Test for the connectivity module in the epigame package
# Ensure that the necessary directories and files exist
def test_run_connectivity():

    input_folder = "data/input"
    output_folder = "data/output"
    connectivity_dir = os.path.join(output_folder, "connectivity")

    # temp_dir = tempfile.mkdtemp()
    # connectivity_dir = os.path.join(temp_dir, "connectivity")

    os.makedirs(connectivity_dir, exist_ok=True)
    subject_id = 1

    interictal_path = os.path.join(input_folder, f"{subject_id}_interictal.mat")
    preictal_path = os.path.join(input_folder, f"{subject_id}_preictal.mat")

    prep = preprocess_from_mat(interictal_path, preictal_path, fs=500, band=None)
    run_connectivity_matrices(prep, subject_id, bands=None, output_dir=connectivity_dir)

    # Clean up
    # shutil.rmtree(temp_dir)