# Data

Datasets are not committed to Git. All data is stored in Amazon S3 (`us-east-1`), bucket `sagemaker-us-east-1-977845482519`, under the prefix `aai540-turbofan-rul/`.

| Prefix | Contents |
|---|---|
| `raw/FD001/` | NASA C-MAPSS FD001 source files: `train_FD001.txt`, `test_FD001.txt`, `RUL_FD001.txt` |
| `processed/` | Engineered feature files for the train, validation, test and production partitions (CSV, including XGBoost-format files) |
| `athena/fd001_training_features/` | Source data for the Athena table `fd001_training_features` |
| `feature-store/` | SageMaker Feature Store offline store (feature group `aai540-turbofan-features-482519`, 20,631 records) |
| `models/` | XGBoost training output (`model.tar.gz`) |
| `batch-output/test/` | Batch Transform predictions for the test partition |
| `monitoring/` | Model Monitor baseline and current-data reports |
| `evidence/` | `evidence_manifest.json` listing every AWS resource created by the notebook |

**Source:** [NASA Prognostics Center of Excellence data set repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/). The notebook downloads FD001 inside SageMaker and uploads it to `raw/FD001/`.

**Partitions** (split by engine ID): 40% train, 10% validation, 10% test, 40% production (reserved for monitoring and drift checks).

The bucket and account are specific to the team's AWS lab environment; the notebook derives them from the active SageMaker session.
