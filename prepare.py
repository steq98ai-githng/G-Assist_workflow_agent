# Immutable Evaluator
# DO NOT MODIFY THIS FILE.
# This file serves as the objective evaluator for AI experiments.

import os

def evaluate() -> None:
    target = 0.9979
    val_bpb = float('inf')

    if os.path.exists("results.tsv"):
        with open("results.tsv", "r") as f:
            lines = f.readlines()
            if len(lines) > 1:
                last_line = lines[-1].strip()
                parts = last_line.split("\t")
                if len(parts) >= 2:
                    try:
                        val_bpb = float(parts[1])
                    except ValueError:
                        pass

    status = "PASS" if val_bpb < target else "FAIL"
    print(f"EVAL: val_bpb={val_bpb} | target={target} | status={status}")

if __name__ == "__main__":
    evaluate()
