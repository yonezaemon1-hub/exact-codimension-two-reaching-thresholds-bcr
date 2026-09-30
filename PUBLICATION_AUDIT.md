# Publication audit

Date: 2026-09-30
Author: Ryutaro Yonezu

## Frozen theorem

For every n >= 4,

- odd n: F_BCR(n,n-2) = 2n;
- even n: F_BCR(n,n-2) = max{2n, 5n/2 - 3}.

## Finite certificate used by the proof

The only finite boundary case needed beyond the cited infinite lower-bound families is n=8.
The publication verifier recomputes from scratch:

- normalized defect-one maps: 141,120;
- completely reachable automata: 136,704;
- exact maximum: 17;
- extremal automata: 68.

The verifier was run on the frozen package before release and returned PASS_N8_EXACT_CERTIFICATE.

## PDF visual preflight

The six-page PDF was rendered at 150 dpi before publication. The title page and final reproducibility/reference page were visually inspected; no clipping, overlap, missing glyph blocks, or broken page geometry was observed.

## Claim boundary

Previously known definitions, Cerny-family lower bounds, Zhu's even-state lower construction, and general completely-reachable upper-bound results are cited rather than claimed as new. The new claim is the exact binary codimension-two formula and its proof, with computation confined to n=8.

An earlier exploratory status note that described the formula as a conjecture is superseded and intentionally omitted from the release package.
