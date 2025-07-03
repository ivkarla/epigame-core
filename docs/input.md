## `NODES.p`

- Format: Python `dict` with subject ID as key, list of node IDs as value
- Example: `{ 1: [0, 1, 2, ...] }`

## `RESECTION.p`

- Format: Python `dict` with subject ID as key, list of resection node IDs as value
- Must match keys in `NODES.p`
- Example: `{ 1: [4, 10] }`

## `.mat` Files

- Must contain key `sz_data` of shape `(channels, time)` under index [0][0] and node labels under index [0][1]
- Named like: `1-interictal.mat`, `1-preictal.mat` where `1` is an example of subject ID

## `outcomes.xlsx`

- Only necessary in case of using `outcome_prediction.py`
- Must contain columns: `subject_id` (integer IDs as values), `outcome` (1 - good outcome; 0 - poor outcome as values)
