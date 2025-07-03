import os
from epigame.cross_validation import run_classification_pipeline
from aggregate_scores import aggregate_cv_scores
from epigame.connectivity import REc


def test_run_cross_validation():

    output_folder = "data/output"
    connectivity_dir = os.path.join(output_folder, "connectivity")

    subject_id = 1
    measure = "PAC"
    bands = None

    cm_suffix = "" if bands is None else f"-{bands[0]}-{bands[1]}"
    ext = f"{subject_id}-{bands[0]}-{bands[1]}" if bands else f"{subject_id}"
    file = os.path.join(connectivity_dir, f"{subject_id}-{measure}{cm_suffix}.prep")

    cm_struct = REc.load(file).data
    run_classification_pipeline(
        cm_struct=cm_struct,
        subject_id=subject_id,
        measure=measure,
        bands=bands,
        output_dir=output_folder
    )

    #Step 3: Aggregate CVS scores
    cvs_csv = os.path.join(output_folder, "cvs_pairs_test.csv")
    aggregate_cv_scores(
        result_dir=output_folder,
        subject_ids=[subject_id],
        output_csv=cvs_csv
    )