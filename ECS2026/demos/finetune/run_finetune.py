#!/usr/bin/env python3
"""Upload training data and create an Azure AI Foundry fine-tuning job for Aino.

Run from the ECS directory (with venv active):
    python demos/finetune/run_finetune.py

After the job completes (~30-60 min), deploy the model and add the deployment name to demos/.env:
    AZURE_OPENAI_DEPLOYMENT_FT=<your-deployment-name>
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from aif_client import get_client

FINETUNE_DIR = Path(__file__).parent
TRAINING_FILE   = FINETUNE_DIR / "training_data.jsonl"
VALIDATION_FILE = FINETUNE_DIR / "validation_data.jsonl"

# Fine-tune on gpt-4o-mini (cheapest / fastest; good for customer support)
BASE_MODEL = "gpt-4o-mini"


def upload_file(client, path: Path, purpose: str) -> str:
    print(f"Uploading {path.name} ...")
    with path.open("rb") as f:
        result = client.files.create(file=f, purpose=purpose)
    print(f"  file_id={result.id}  status={result.status}")
    return result.id


def create_job(client, training_id: str, validation_id: str) -> str:
    print(f"\nCreating fine-tuning job on {BASE_MODEL} ...")
    job = client.fine_tuning.jobs.create(
        training_file=training_id,
        validation_file=validation_id,
        model=BASE_MODEL,
        hyperparameters={"n_epochs": 3},
        suffix="aino",
    )
    print(f"  job_id={job.id}  status={job.status}")
    return job.id


def wait_for_job(client, job_id: str) -> None:
    print(f"\nWaiting for job {job_id} to complete (this takes 30-60 minutes) ...")
    print("Press Ctrl+C to stop watching — the job continues running in Azure.")
    dots = 0
    while True:
        try:
            time.sleep(30)
            job = client.fine_tuning.jobs.retrieve(job_id)
            dots += 1
            print(f"  [{dots * 30}s] status={job.status}", end="")
            if job.status == "succeeded":
                print()
                print(f"\nJob succeeded!")
                print(f"  fine_tuned_model: {job.fine_tuned_model}")
                print()
                print("Next steps:")
                print("  1. In Azure AI Foundry, deploy the model above.")
                print("  2. Copy the deployment name into demos/.env:")
                print(f"       AZURE_OPENAI_DEPLOYMENT_FT=<your-deployment-name>")
                return
            elif job.status in ("failed", "cancelled"):
                print()
                print(f"\nJob {job.status}.")
                if job.error:
                    print(f"  Error: {job.error}")
                return
            else:
                print(" (still running...)")
        except KeyboardInterrupt:
            print(f"\n\nStopped watching. Job {job_id} is still running in Azure.")
            print("Check status: Azure AI Foundry → Fine-tuning → Jobs")
            return


def main() -> int:
    client, _ = get_client()

    training_id   = upload_file(client, TRAINING_FILE,   "fine-tune")
    validation_id = upload_file(client, VALIDATION_FILE, "fine-tune")
    job_id = create_job(client, training_id, validation_id)
    wait_for_job(client, job_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
