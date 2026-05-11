# Cosmic Forge Experiments - May 2026

**Status:** Research probe series, not protocol attestations.  
**Date:** 2026-05-10 to 2026-05-11  
**Hardware:** NVIDIA GeForce RTX 3060 (12 GB VRAM) on PopChain validator val-beta.  
**Scope:** Empirical investigation of GPU compute proof determinism and emergent multi-physics dynamics, conducted to inform PCIP-0010 (POP-2-COMPUTE Active Compute Profile) and PCIP-0011 (Validator Tier Registry).

---

## Why these experiments exist

PopChain plans validator tier admission (PCIP-0011) gated on demonstrated compute capability. POP-2-COMPUTE (PCIP-0010) defines workload proof objects whose canonical correctness requires bit-identical output across GPU backends and across runs.

Before locking the canonical compute proof kernel architecture for protocol version 1, the project conducted an empirical investigation to answer four operational questions:

1. **Is GPU compute deterministic enough to serve as authoritative compute proof?**
2. **What kernel design patterns preserve determinism, and which break it?**
3. **What throughput can a consumer-grade GPU realistically deliver?**
4. **Does multi-stream physics composition scale, and can per-stream witnessing work?**

The answers are documented in `EMPIRICAL-FINDINGS.md`. The methodology is in `METHODOLOGY.md`. Reproducibility guidance is in `REPRODUCIBILITY.md`. The architectural rule derived from the findings is in `DETERMINISM-RULE.md`.

---

## Experiment list

Six experiments were conducted in sequence, each building on the previous.

| # | Date | Name | Scale | Result | Envelope |
|---|------|------|-------|--------|----------|
| 001 | 2026-05-10 | r-process-toy v0 | 10k particles × 1k steps | DETERMINISTIC (PASS × 3 runs) | [link](./results/eksperyment-001-envelope.json) |
| 002 | 2026-05-11 | r-process-v1-MEGA | 1M particles × 10k steps | DETERMINISTIC (PASS × 3 runs) | [link](./results/eksperyment-002-envelope.json) |
| 003 | 2026-05-11 | hypermassive-multiphysics-collider-v0 | 10M particles × 1k steps, 6 streams, float atomics | NON-DETERMINISTIC (FAIL - investigated) | [link](./results/eksperyment-003-envelope.json) |
| 004 | 2026-05-11 | hypermassive-multiphysics-collider-v3 | 10M particles × 1k steps, 6 streams, int64 atomics | DETERMINISTIC (PASS × 3 runs) | [link](./results/eksperyment-004-envelope.json) |
| 005 | 2026-05-11 | multiverse-collider-v4 | 4 universes × 2.5M × 500 steps, 12 streams | DETERMINISTIC (PASS × 3 runs) | [link](./results/eksperyment-005-envelope.json) |
| 006 | 2026-05-11 | maximum-chaos-generator-v0 | 6 universes × 2.5M × 500 steps, chaos amplifiers | Emergent universality (see findings) | [link](./results/eksperyment-006-envelope.json) |

---

## Summary of operational findings

1. **GPU compute proofs CAN be deterministic** at scale (15+ billion particle-step operations per run, bit-identical across re-runs) when correctly designed.

2. **The single decisive design rule** that determines determinism: integer atomic operations are permitted; floating-point atomic operations are not. This rule is proposed for inclusion in PCIP-0010 as §6.4.1 - see `DETERMINISM-RULE.md`.

3. **Consumer hardware suffices.** RTX 3060 (12 GB VRAM, 170 W TDP, ~58°C peak under sustained 100% load) delivered 79.2M to 157.6M particle-steps per second in a 6-12 physics-stream simulation. This exceeds the PCIP-0011 §7.1.1 threshold of 100M operations per second for T2 admission by a factor of 1.5× to 3×.

4. **Per-stream Merkle witnessing scales.** A multi-physics proof can be decomposed into per-stream Merkle roots (one per physics stream), enabling tier-aware partial verification: T2 validators can witness 1–2 streams; T3+ can witness all streams; T4 clusters can witness across parallel universes.

---

## Summary of scientific observations

Experiment 006 (chaos generator) produced unexpected emergent statistics, observed independently across 6 universes with different canonical PopChain anchor seeds:

- **Power-law cluster size distribution** with goodness of fit R² between 0.96 and 0.995 across all universes.
- **Power-law mass-number distribution** with exponent α between 2.02 and 2.12 (mean ≈ 2.05) across all universes.
- **Fractal dimension of spatial density** between 2.662 and 2.669 (mean ≈ 2.665) across all universes - variance below 0.3%.
- **Shannon entropy of mass-number distribution** between 5.934 and 5.939 bits across all universes - variance below 0.1%.
- **Cross-universe KL divergence** of final mass-number distributions: 0.000 to 0.001 (statistical equivalence).

These convergences across distinct seeds suggest the chaotic multi-physics system possesses an **emergent macroscopic universality class**: microscopic state varies per seed, but macroscopic statistical observables converge. See `EMPIRICAL-FINDINGS.md` for full discussion.

---

## Status

- **PUBLIC:** This document, `EMPIRICAL-FINDINGS.md`, `METHODOLOGY.md`, `DETERMINISM-RULE.md`, `REPRODUCIBILITY.md`, and result envelopes (numerical hash outputs).
- **PRIVATE:** Source code of experiment scripts (PopChain Foundation property, available under future open-source release per `PCIP-0020 §10.3`).

Third parties may reproduce results by implementing their own compute kernels following the specifications in `METHODOLOGY.md` and `REPRODUCIBILITY.md`. Reproducibility verification anchors are listed in `results/ANCHOR-HASHES.md`.

---

## License

Documents in this directory are released under Apache-2.0 license, consistent with the rest of the `popchain` public repository.

---

## Funding acknowledgment

The Cosmic Forge experiment series was conducted as part of work supported by NLnet Foundation under Commons Fund grant ticket 2026-04-3f6.
