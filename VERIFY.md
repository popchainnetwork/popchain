# PopChain Phase 0c.1 — Reproducibility Guide

**Reflects state at HEAD = `0432f2f`, generated 2026-05-10.**
To reproduce against this exact state:

```bash
cd ~/popchain && git checkout 0432f2f
```

This document describes how to independently verify the Phase 0c.1
verification dump (Persistence Stress Regression Suite + invariant
guards). Anyone with read access to popchain-core or any of the three
validator machines can reproduce this output.

---

## Threat Model Scope

Phase 0c.1 validates: XMSS state machine persistence invariants,
crash-recovery semantics, and cross-architecture deterministic
computation of the four mechanical anchors. Phase 0c.1 does NOT
validate: full network consensus correctness, multi-tree XMSS^MT
(scheduled P1.7), file locking under concurrent access (scheduled
P1.5), backup-restore detection (scheduled P1.6), or independent
cryptographic audit (post-Phase 0c).

---

## Prerequisites

- Read access to one of: val-alpha (37.97.202.97), val-beta, val-pi-01
- Or: clone of popchain-core repository at commit 0432f2f
- Rust toolchain 1.75+ (project tested on 1.75.0 and 1.85.0)
- Python 3.8+

### Recommended environment fingerprint

Capture your toolchain state for audit reproducibility:

```bash
rustc --version --verbose
cargo --version
python3 --version
uname -a
sha256sum Cargo.lock
```

---

## Reproducibility Steps

### [1] Git history (3 milestones)

```bash
cd ~/popchain
git log --oneline -3
```

Expected:

```
0432f2f  Phase 0c.1 attestations bundle (9 files on-chain alpha-testnet)
8e060c1  Phase 0c.1: persistence stress regression + invariant guards
e8a6549  feat: PopChain v0.7 — three mechanical anchors locked cross-arch
```

### [2] Source SHA256 (Phase 0c.1 patched files)

Identical SHA256 across all 3 machines proves source files are
bit-for-bit identical: no per-machine modifications, no
compiler-specific patches, no architecture-conditional code.

```bash
sha256sum src/crypto/xmss.rs src/lib.rs
```

Expected (bit-identical on all 3 machines):

```
48ccb0c71524f608996a62907436095061565c937b9c0a7480e95f4e3bbe463a  src/crypto/xmss.rs
0c08548dccee31ca020945a4ff6223ae14ec1995013e52696b1af754ca9763a1  src/lib.rs
```

### [3] cargo test crypto::xmss::

```bash
cargo test --release --lib crypto::xmss::
```

Expected test outcomes (bit-identical across machines):

```
test result: ok. 18 passed; 0 failed; 2 ignored; 0 measured; 37 filtered out
```

Times observed: alpha 2.91s, beta 1.98s, pi-01 9.92s. Per-machine
runtimes vary by hardware and parallelism; the test outcomes (counts
plus anchor values from [4]) are bit-identical across machines, but
cargo's logging is not.

### [4] Four anchors regression

Each anchor is a deterministic value computed by Phase 0a/0b
cryptographic primitives. Bit-identical anchor values across three
heterogeneous architectures is the cross-architecture determinism
claim of Phase 0a/0b/0c.1.

```bash
# Anchor 1 (PoCC) — verify exact compile-time value
grep -q "pub const POCC_ANCHOR_V1: u128 = 417696;" src/pocc.rs && echo "OK Anchor 1" || echo "FAIL Anchor 1"
cargo test --release --lib pocc::tests::test_proof_value_deterministic_anchor

# KAT-1 (Anchor 2-bis)
cargo test --release --lib crypto::wots_v2::tests::kat_1_keygen_determinism -- --nocapture | grep "39399ffd"

# Anchor 2 (KAT-6)
cargo test --release --lib crypto::wots_v2::tests::kat_6 -- --nocapture | grep "b2e04c80"

# Anchor 3 (KAT-10 XMSS root)
cargo test --release --lib crypto::xmss::tests::kat_10 -- --nocapture | grep "2935fde2"
```

Expected anchor values (bit-identical on all 3 machines):

```
Anchor 1 (PoCC):    POCC_ANCHOR_V1 = 417696
KAT-1:              39399ffd3dcdf17c4a484002ebade955471f4656fa1d562b2820af29d2a13d22
Anchor 2 (KAT-6):   b2e04c806390bd6d60c80cb82178aa6032c4bd76b14d931d93e01e49c8005dad
Anchor 3 (KAT-10):  2935fde2b9d76e0b7a9c733cd518cc9df07cf282163cadc990c8587c7b903606
```

### [5] Attestations bundle SHA256 (sorted)

```bash
cd docs/attestations/phase-0c1
sha256sum * | sort
```

Expected (bit-identical on all 3 machines):

```
1f0d1df4b0613a616a17c4a1b07ca7c59879abd489b843253608e909a99dffa3  01_gemini_md.md
38dc96765f35954e123e1dea8462bb77f9ea865998c05f40f4a313dd72f9b8db  05_grok_short.md
712c00ad0aba94f779981b1fa549d9574e97387b950ce69edf4ac75a68c9ba9c  MASTER_ROOT.txt
80bd3b329fbe821693727495589c28b7553f6b6d36405a38532237ae81379fdc  03_gpt.md
90fbbbf28bb83db78643450858ffcfc689a6126401c706f7cf74ed74e36d51ae  02_gemini_pdf.pdf
b6657030de2ce6e921f9daa00b3750c19cd5d7a2f4ef08699fc3f09251ed95f4  ATTESTATIONS_LEDGER.md
bf8f87c4406f995efa085b2bdcfb54cdcc24268e63f9ec9913b024d570167c65  04_claude_signed.txt
c10fca7078470075367978e2e664ffc8495c41e0b6df4f892fba2f8dde8fa429  07_claude_review_note.md
e4c4332ce96c7e1d02c3377f2daf36a8a95223b350974f954fc74019bff00c65  06_grok_refined.md
```

(Note: ATTESTATIONS_LEDGER.md may be subsequently updated for
documentation purposes — see [6] for canonical reference.)

### [6] Master root

```bash
sha256sum 01_gemini_md.md 02_gemini_pdf.pdf 03_gpt.md \
          04_claude_signed.txt 05_grok_short.md \
          06_grok_refined.md 07_claude_review_note.md \
          ATTESTATIONS_LEDGER.md | sort | sha256sum
```

Expected: `dab3645de4efa05e43161e2227bee5508a3aa9ad86548dfd8ca20bd3bbee0a7d`

**Two distinct artifacts — important distinction:**

- `dab3645d...` is the master root **value**: SHA256 of sorted hash list
  of the 8 attestation files (excluding MASTER_ROOT.txt itself to avoid
  self-reference). This corresponds to the bundle as anchored on-chain
  at block #83687 (ATTESTATIONS_LEDGER.md).
- `712c00ad...` is the SHA256 of the **MASTER_ROOT.txt file content**
  (the file that records the master root value plus context). This is
  anchored separately on-chain at block #83688.

Master root `dab3645d...` reflects the bundle as anchored on-chain at
block #83687 on 2026-05-10. The local ATTESTATIONS_LEDGER.md may be
updated subsequently for documentation purposes; the on-chain anchored
version remains canonical for Phase 0c.1 attestation set. To
reproduce the original on-chain hash: `git checkout 0432f2f`.

### [7] On-chain anchoring verification

```bash
python3 tools/verify_attestations.py
```

(Optional: `--db-path /path/to/blocks/` for non-default validator
block storage; `--max-blocks N` to scan a different window.)

Expected: 8/8 ON-CHAIN MATCH for blocks #83678–#83687 (attestations +
ledger). MASTER_ROOT.txt anchored at block #83688.

The script is committed at `tools/verify_attestations.py` (SHA256
`e38380af7921a988ba0998c01ae3a488b02ea9f2067432761d5db8ceddeb8e57`),
deterministic, no network calls, Python 3 stdlib only.

### [8] Chain state

Live explorer (informational only — canonical verification source is
local chain state queried from validator node):
https://popchain.tech/explorer.html

For canonical chain state, query alpha validator directly:

```bash
ls /home/uncrfactory/popchain-data/val-alpha/blocks/ | wc -l
```

---

## Cross-Machine Parity Claim

Sections [2], [4], [5], [6] produce **bit-identical bytes** across all
three machines (val-alpha x86_64 cloud, val-beta x86_64 AMD, val-pi-01
ARM64 Pi 5). Section [3] produces **bit-identical test outcomes**
(18 passed, 0 failed, 2 ignored, with anchor values exactly as in [4]);
cargo's per-machine runtime logging differs but does not affect
verification. Section [7] requires alpha access (queries canonical
chain state) and is reproducible by anyone with that access.

Phase 0c.1 demonstrates that the tested XMSS persistence and anchor
paths produce bit-identical outputs across heterogeneous hardware
architectures under the same source tree and toolchain family.

---

## Known Limitations

Phase 0c.1 does NOT yet include:

- fs4 file locking (KAT-24 ignored; scheduled Phase 0c P1.5)
- backup-restore epoch detection (KAT-26 ignored; scheduled Phase 0c P1.6)
- XMSS^MT multi-tree implementation (scheduled Phase 0c P1.7, beta blocker)
- independent Python reimplementation (scheduled P3, post-P1.7)
- cosignatures protocol over XMSS^MT (scheduled P2)
- POP-1, POP-2 specifications (scheduled P4, NLnet deliverables)
- Zymkey HSM6 hardware integration (scheduled P5, parallel with P1.7)
- formal cryptographic audit (post-Phase 0c)
- production consensus validation under adversarial conditions
- mainnet readiness (beta-testnet has not yet launched)

---

## Troubleshooting

**Source SHA256 mismatch in [2]:**
- Confirm clean checkout: `git status` should show no modifications
- Confirm exact commit: `git rev-parse HEAD` should equal `0432f2f`
- If still mismatched: line endings or filesystem encoding issue;
  re-clone in fresh directory

**cargo test failures in [3]:**
- Confirm Rust version: `rustc --version` (tested on 1.75.0, 1.85.0)
- Confirm platform: Linux x86_64 or ARM64 (Windows untested)
- Confirm `Cargo.lock` matches: SHA256 should match expected
- Run `cargo clean && cargo build --release` first

**Anchor value mismatch in [4]:**
- This is critical — halt and report to operator immediately
- Mismatched anchor values signal compromise or undocumented divergence
- Do NOT continue verification

**On-chain MISSING in [7]:**
- Confirm `--db-path` points to validator block storage
- Confirm `--max-blocks` is large enough (default 100 covers
  blocks ~83588–83688; for older Phase 0c.1 anchoring, increase)
- Some validators prune old blocks; alpha-testnet retains full history

---

## Reproducibility Dossier

For comprehensive audit, capture:

```bash
git rev-parse HEAD > /tmp/state-head.txt
git diff --stat e8a6549..HEAD > /tmp/state-diff.txt
sha256sum src/crypto/xmss.rs src/lib.rs Cargo.lock > /tmp/state-sha.txt
rustc --version --verbose > /tmp/state-rust.txt
uname -a > /tmp/state-arch.txt
```

These files together pin: source identity, toolchain identity, and
hardware/OS context.

---

— Paweł Piekut, Plastechniek ZZP, Almelo NL
  pop1_a4c073ac215bdd52b369b618f1913f7071a659172ba35e9dc7845d6aa876fa84
  NLnet Commons Fund ticket: 2026-04-3f6
  popchain.tech | popchain.foundation
