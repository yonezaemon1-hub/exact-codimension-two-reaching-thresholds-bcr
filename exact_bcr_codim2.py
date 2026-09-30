from collections import deque
from itertools import combinations, permutations
import sys


def rank_n_minus_one_maps(n, canonical_rotation=False):
    q = range(n)
    # With b=(0 1 ... n-1), conjugation by a power of b preserves all
    # reaching distances.  Every rank-(n-1) map has a unique excluded state,
    # so fixing it to 0 gives one representative from every rotation orbit.
    excluded_states = (0,) if canonical_rotation else q
    for excluded in excluded_states:
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


def audit(n, canonical_rotation=False):
    b = tuple((i + 1) % n for i in range(n))
    bt = image_table(n, b)
    full = (1 << n) - 1
    target_size = n - 2
    total = cr = 0
    best = -1
    best_data = None
    histogram = {}
    seen_maps = set()
    for a in rank_n_minus_one_maps(n, canonical_rotation):
        if a in seen_maps:
            continue
        seen_maps.add(a)
        total += 1
        at = image_table(n, a)
        dist = [-1] * (1 << n)
        dist[full] = 0
        todo = deque([full])
        while todo:
            s = todo.popleft()
            for t in (at[s], bt[s]):
                if dist[t] < 0:
                    dist[t] = dist[s] + 1
                    todo.append(t)
        if any(dist[s] < 0 for s in range(1, 1 << n)):
            continue
        cr += 1
        threshold = max(dist[s] for s in range(1, 1 << n)
                        if s.bit_count() == target_size)
        histogram[threshold] = histogram.get(threshold, 0) + 1
        if threshold > best:
            best = threshold
            target = max((s for s in range(1, 1 << n)
                          if s.bit_count() == target_size), key=dist.__getitem__)
            best_data = (a, target, dist[target])
    print({"n": n, "rank_n_minus_one_maps": total,
           "canonical_rotation": canonical_rotation,
           "completely_reachable": cr, "best": best,
           "histogram": histogram, "witness": best_data})


if __name__ == "__main__":
    args = sys.argv[1:]
    canonical = "--canonical-rotation" in args
    values = [int(x) for x in args if not x.startswith("--")] or [4, 5, 6, 7]
    for n in values:
        audit(n, canonical)
