"""SageMaker Pipeline processing step: evaluate the trained XGBoost model.

Loads the model artifact produced by the pipeline's training step and the
held-out validation CSV, scores it, and writes evaluation.json in the schema
SageMaker Pipelines' ConditionStep / JsonGet expects
(regression_metrics.<metric>.value), so the pipeline can branch on RMSE.
"""

import json
import os
import tarfile

import pandas as pd
import xgboost as xgb

MODEL_DIR = "/opt/ml/processing/model"
VALIDATION_DIR = "/opt/ml/processing/validation"
OUTPUT_DIR = "/opt/ml/processing/evaluation"


def main():
    model_archive = os.path.join(MODEL_DIR, "model.tar.gz")
    with tarfile.open(model_archive) as archive:
        archive.extractall(MODEL_DIR)

    booster = xgb.Booster()
    model_file = next(
        name for name in os.listdir(MODEL_DIR) if name.startswith("xgboost-model") or name.endswith(".bin")
    )
    booster.load_model(os.path.join(MODEL_DIR, model_file))

    validation_path = next(
        os.path.join(VALIDATION_DIR, name)
        for name in os.listdir(VALIDATION_DIR)
        if name.endswith(".csv")
    )
    validation_frame = pd.read_csv(validation_path, header=None)
    labels = validation_frame.iloc[:, 0].to_numpy()
    features = validation_frame.iloc[:, 1:]

    predictions = booster.predict(xgb.DMatrix(features))

    rmse = float(((predictions - labels) ** 2).mean() ** 0.5)
    mae = float(abs(predictions - labels).mean())

    report = {
        "regression_metrics": {
            "rmse": {"value": rmse, "standard_deviation": "NaN"},
            "mae": {"value": mae, "standard_deviation": "NaN"},
        }
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "evaluation.json"), "w") as handle:
        json.dump(report, handle, indent=2)

    print(f"Evaluation RMSE: {rmse:.3f}")
    print(f"Evaluation MAE:  {mae:.3f}")


if __name__ == "__main__":
    main()
