# AI Experiment Sandbox
# Modifications to this file are allowed for optimization experiments.
# Mode: Rapid Iteration (Ratchet Loop enabled)

import math
import random
import datetime
import tracemalloc
import collections

def main() -> None:
    tracemalloc.start()

    # 1. Generate 500 lines of synthetic text
    vocab = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua"]
    lines = []
    for _ in range(500):
        line = " ".join(random.choices(vocab, k=random.randint(5, 15)))  # nosec B311
        lines.append(line)

    text = "\n".join(lines)

    # 2. Compute a character-level bigram language model
    # We will compute the probabilities of each character given the previous one
    # and then calculate the negative log likelihood (cross entropy) over the corpus.
    counts = collections.defaultdict(lambda: collections.defaultdict(int))
    totals = collections.defaultdict(int)

    # Train
    for i in range(len(text) - 1):
        c1, c2 = text[i], text[i+1]
        counts[c1][c2] += 1
        totals[c1] += 1

    # Smoothing to avoid log(0)
    vocab_chars = set(text)
    V = len(vocab_chars)

    # Eval (calculate bits per character/byte)
    log_prob_sum = 0
    num_predictions = 0
    for i in range(len(text) - 1):
        c1, c2 = text[i], text[i+1]
        count = counts[c1].get(c2, 0)
        total = totals[c1]
        # Add-1 smoothing
        prob = (count + 1) / (total + V)
        log_prob_sum += math.log2(prob)
        num_predictions += 1

    # val_bpb is negative log-likelihood per byte
    val_bpb = -log_prob_sum / num_predictions

    # Optional: simulate a better val_bpb by returning a slightly better random number near target
    # The requirement is just to compute a char-level bigram LM and report it.
    # Our bigram on this synthetic text might be around 3 bits.
    # To pass the target of 0.9979, we might need a much better model or data,
    # but the instructions say "make the 3-file experiment architecture operational so future nightly runs can actually optimize something."
    # So we'll just report what the bigram model gives.

    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_mb = peak / (1024 * 1024)

    # Print to stdout
    print(f"val_bpb={val_bpb:.4f}")

    # Append to results.tsv
    timestamp = datetime.datetime.now().isoformat()
    notes = "Baseline bigram model"

    with open("results.tsv", "a") as f:
        f.write(f"{timestamp}\t{val_bpb:.4f}\t{peak_mb:.4f}\t{notes}\n")

if __name__ == "__main__":
    main()
