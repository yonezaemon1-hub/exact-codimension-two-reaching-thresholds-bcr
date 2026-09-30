#!/usr/bin/env python3
import argparse
import json
from collections import deque
from itertools import combinations, permutations
from pathlib import Path

EXPECTED = {
    "n": 8,
    "normalized_defect_one_maps": 141120,
    "completely_reachable": 136704,
    "maximum_codimension_two_threshold": 17,
    "extremal_automata": 68,
}


def rank_n_minus_one_maps(n):
    q = range(n)
    excluded = 0
    image = [x for x in q if x != excluded]
    for p, r in combinations(q, 2):
        other_sources = [x for x in q if x not in (p, r)]
        for duplicate in image:
            other_images = [x for x in image if x != duplicate]
            for perm in permutations(other_images):
                a = [None] * n
                a[p] = a[r] = duplicate
                for x, y in zip(other_sources, perm):
                    a[x] = y
                yield tuple(a)


def image_table(n, trans):
    size = 1 << n
    out = [0] * size
    for mask in range(1, size):
        low = mask & -mask
        i = low.bit_length() - 1
        out[mask] = out[mask ^ low] | (1 << trans[i])
    return out


def mask_to_states(mask, n):
    return [i for i in range(n) if mask >> i & 1]


def audit(n=8):
    if n != 8:
        raise ValueError("This frozen publication verifier certifies only n=8.")
    b = tuple((i + 1) % n for i in range(n))
    bt = image_table(n, b)
    full = (1 << n) - 1
    target_size = n - 2
    total = 0
    cr = 0
    best = -1
    extremal = 0
    witness = None
    histogram = {}

    for a in rank_n_minus_one_maps(n):
        total += 1
        at = image_table(n, a)
        dist = [-1] * (1 << n)
        dist[full] = 0
        todo = deque([full])
        while todo:
            s = todo.popleft()
            ds = dist[s] + 1
            ta = at[s]
            if dist[ta] < 0:
                dist[ta] = ds
                todo.append(ta)
            tb = bt[s]
            if dist[tb] < 0:
                dist[tb] = ds
                todo.append(tb)

        if any(dist[s] < 0 for s in range(1, 1 << n)):
            continue

        cr += 1
        targets = [s for s in range(1, 1 << n) if s.bit_count() == target_size]
        threshold = max(dist[s] for s in targets)
        histogram[threshold] = histogram.get(threshold, 0) + 1

        if threshold > best:
            best = threshold
            extremal = 1
            target = max(targets, key=dist.__getitem__)
            witness = {
                "a": list(a),
                "target_mask": target,
                "target_states": mask_to_states(target, n),
                "distance": dist[target],
            }
        elif threshold == best:
            extremal += 1

    result = {
        "n": n,
        "normalized_defect_one_maps": total,
        "completely_reachable": cr,
        "maximum_codimension_two_threshold": best,
        "extremal_automata": extremal,
        "histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "first_extremal_witness": witness,
    }

    for key, value in EXPECTED.items():
        if result[key] != value:
            raise AssertionError(f"{key}: expected {value}, got {result[key]}")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()
    result = audit(args.n)
    if args.json:
        args.json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS_N8_EXACT_CERTIFICATE")


if __name__ == "__main__":
    main()
