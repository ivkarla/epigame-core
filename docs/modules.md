# Modules Overview

### `connectivity.py`
Preprocessing of timeseries: notch, bandpass filtering and separating 1-s epochs.
Connectivity analysis (PAC, PLV, etc.), parallelized across epochs.
Outputs connectivity matrices as `.prep`files to `data/output/connectivity` folder.

### `cross_validation.py`
Performs k-fold classification of connectivity sub-matrices (for each node pair), between interictal and preictal states.
Outputs `.res` files for each connectivity measure to `data/output` folder.

### `aggregate_scores.py`
Creates a table of cross-validation scores across all node pairs and connectivity measures.
Outputs `cvs_pairs.csv` to the `data/input` folder.

### `game.py`
Simulates a competitive card-based game to identify relevant node groups.
Outputs `scores_sub{subject_id}.p` to `data/output/game_scores`

### `main.py`
Entry point for running the entire pipeline.

### `utils.py`
Structures for data wrangling and storage.