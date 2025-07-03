import os
import tempfile
from random import sample
from pickle import load
from scipy.io import loadmat
from epigame.game import run_game

def test_run_game_smoke():
    input_folder = "data/input"
    # Setup temporary directories and fake data
    temp_dir = tempfile.mkdtemp()
    output_dir = os.path.join(temp_dir, "game_scores")
    os.makedirs(output_dir, exist_ok=True)
    
    subject_id = 1
    interictal_path = os.path.join(input_folder, f"{subject_id}_interictal.mat")
    interictal_raw = loadmat(interictal_path)['sz_data'][0]

    NODES = {subject_id : [id for id in range(len(interictal_raw[1]))]}
    RESECTION = {subject_id : sample(NODES[subject_id], 10)}  # Dummy resection data

    # Run the game pipeline
    run_game(
        subject_id=subject_id,
        main_folder=input_folder,
        output_dir=output_dir,
        RESECTION=RESECTION,
        NODES=NODES,
        rounds=2,
        turns=2,
        cards_in_hand=2,
        max_sigma=1
    )

    # Check output
    out_file = os.path.join(output_dir, f"scores_sub{subject_id}.p")
    assert os.path.exists(out_file), "Output .p file not created"

