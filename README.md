# Exact Codimension-Two Reaching Thresholds for Binary Completely Reachable Automata

Ryutaro Yonezu — Independent Researcher

This repository contains the frozen preprint and an exhaustive finite verifier for the boundary case used in the exact codimension-two theorem for binary completely reachable automata.

## Main theorem

For every integer `n >= 4`, let `F_BCR(n,n-2)` be the worst-case length of a shortest word reaching an `(n-2)`-subset, maximized over all `n`-state binary completely reachable DFAs and all such target subsets. Then

```text
F_BCR(n,n-2) = 2n                              if n is odd,
               max{2n, 5n/2 - 3}              if n is even.
```

Equivalently, the value is `2n` for odd `n` and for `n = 4,6`, and is `5n/2 - 3` for even `n >= 8`.

The proof isolates the only obstruction to the direct `2n` route: an even-state antipodal missing pair when the duplicated state of the defect-one letter is the unique nonzero element of order two. A two-route detour gives the upper bound `5n/2 - 3`. The lower bounds come from the classical Cerny family, Zhu's even-state construction for even `n >= 10`, and an exhaustive finite certificate for `n = 8`.

## Exhaustive n=8 certificate

Run:

```bash
python verify_n8.py --n 8 --json verification_n8.json
```

Expected exact summary:

```text
normalized defect-one maps        141120
completely reachable              136704
maximum codimension-two threshold 17
extremal automata                 68
```

The verifier uses only the Python standard library and performs direct subset-BFS over all nonempty subsets for every normalized rank-7 map with the cyclic letter fixed.

The first extremal witness reported by the frozen verifier is

```text
a = (5, 2, 3, 6, 4, 4, 7, 1)
target = {0,1,2,4,5,6}
distance = 17
```

## Frozen artifacts

- `Yonezu_2026_Exact_Codim2_BCR.pdf` — six-page preprint.
- `verify_n8.py` — publication verifier for the finite n=8 certificate.
- `verification_n8.json` — frozen verifier output.
- `verify_n8_output.txt` — human-readable verification log.
- `research/exact_bcr_codim2.py` — earlier broader enumeration script retained for provenance.
- `SHA256SUMS.txt` — frozen integrity manifest.

## Claim boundary

The paper claims the exact formula above for the binary completely reachable class. It does not claim the general completely reachable upper bound, the Cerny lower construction, Zhu's lower construction, or the underlying definitions as new. The computational component is used only for the n=8 boundary case; the general upper bound is analytical.

The earlier exploratory status note that still called the formula a conjecture is intentionally excluded from this release because it predates the completed proof.

## References used by the paper

- D. Casas and M. V. Volkov, *Binary Completely Reachable Automata*, LATIN 2022.
- J. Cerny, *Poznamka k homogenym experimentom s konecnymi automatami*, 1964.
- R. Ferens and M. Szykula, *Recognizing Completely Reachable Automata in Quadratic Time*, ACM Transactions on Algorithms 22(2), 2026.
- F. Gonze and R. M. Jungers, *On Completely Reachable Automata and Subset Reachability*, DLT 2018.
- Y. Zhu, *Around Don's Conjecture for Binary Completely Reachable Automata*, DLT 2024.

## Licenses

- Paper: CC BY 4.0.
- Code and repository documentation: MIT.
