spaCys coref model is intriguing -- although it is largely based on WL-coref <https://github.com/vdobrovolskii/wl-coref>. Working with a large number of datasets, I needed to alter the custom spacydoc object that is serialized in the preprocessing pipeline: <https://github.com/explosion/projects/blob/v3/experimental/coref/scripts/preprocess.py>. 

By merely outputting interesting fields from the preprocessing step, their clustermap and according functionality is just based on the common jsonl-format of coreference clusters:
```json
    "clustermap": {
        "18": [
            [
                32,
                38
            ],
            [
                28,
                29
            ]
        ],
        "12": [
            [
                494,
                498
            ], ...
```
(loaded using Ontonotes v5)

Where each cluster ID (e.g. "18" above), is then processed as text spans, so we move from "ID": [(start,end), (...)] to "coref_clusters_LENGTH_OF_ID-CLUSTERS": [token span text, ...], along with "coref_head_clusters_ID": [head text, ...]

so this is fairly easy to gather from any conll- or json formatted file. Neat.
