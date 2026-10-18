"""SageMaker Pipeline processing step: validate the training CSV before training.

Reads the headerless SageMaker-XGBoost-format CSV (label in column 0, followed
by FEATURE_COLUMNS) from /opt/ml/processing/input, checks schema and basic
data-quality invariants, and either copies the file through to
/opt/ml/processing/output/train (success) or exits non-zero (failure), which
SageMaker Pipelines surfaces as a failed step / failed pipeline execution.
"""

import argparse
import glob
import os
import shutil
import sys

import pandas as pd

INPUT_DIR = "/opt/ml/processing/input"
OUTPUT_DIR = "/opt/ml/processing/output/train"


def fail(message):
    print(f"VALIDATION FAILED: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-columns", type=int, required=True)
    parser.add_argument("--rul-cap", type=float, required=True)
    parser.add_argument("--min-rows", type=int, default=50)
    args = parser.parse_args()

    candidates = sorted(glob.glob(os.path.join(INPUT_DIR, "*.csv")))
    if not candidates:
        fail(f"No CSV file found under {INPUT_DIR}.")
    input_path = candidates[0]

    try:
        frame = pd.read_csv(input_path, header=None)
    except Exception as error:  # noqa: BLE001 - surface any parse failure as a validation failure
        fail(f"Could not parse {input_path} as CSV: {error}")

    if frame.shape[1] != args.expected_columns:
        fail(
            f"Expected {args.expected_columns} columns, found {frame.shape[1]} "
            f"in {input_path}."
        )

    if len(frame) < args.min_rows:
        fail(f"Expected at least {args.min_rows} rows, found {len(frame)}.")

    fully_null_columns = [col for col in frame.columns if frame[col].isna().all()]
    if fully_null_columns:
        fail(f"Columns entirely null: {fully_null_columns}")

    if frame.isna().any().any():
        fail("Input contains missing values outside of fully-null columns.")

    label = frame[0]
    if label.nunique() <= 1:
        fail("Label column (RUL) has no variance; refusing to train on a constant target.")

    if (label < 0).any() or (label > args.rul_cap).any():
        fail(f"Label column (RUL) contains values outside [0, {args.rul_cap}].")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, os.path.basename(input_path))
    shutil.copyfile(input_path, output_path)

    print(f"Validation passed: {len(frame)} rows, {frame.shape[1]} columns.")
    print(f"Copied validated data to {output_path}")


if __name__ == "__main__":
    main()
