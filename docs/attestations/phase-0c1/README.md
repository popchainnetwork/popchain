# Phase 0c.1 Attestations Bundle

**Project:** PopChain Network L1 — popchain-alpha-testnet
**Phase:**   0c.1 — Persistence Stress Regression Suite
**Date:**    2026-05-10

## What This Directory Contains

Nine files documenting multi-vendor AI review of PopChain Phase 0c.1:

- 7 attestation files (01-07) from 4 AI vendors (Gemini, OpenAI, Anthropic, xAI)
- 1 ledger (ATTESTATIONS_LEDGER.md) describing the bundle
- 1 master root file (MASTER_ROOT.txt) recording bundle integrity hash

All files SHA256-hashed identically across three validator machines
(alpha x86_64 cloud, beta x86_64 AMD, pi-01 ARM64 Pi 5) and anchored
on-chain at popchain-alpha-testnet (blocks #83678–#83688).

## How to Verify

The verification process exercises the same cross-architecture SHA256
identity check that PopChain applies to industrial proofs.

### 1. SHA256 each file (any of 3 machines)

```bash
cd docs/attestations/phase-0c1
sha256sum *
```

### 2. Master root (excludes MASTER_ROOT.txt itself to avoid self-reference)

```bash
sha256sum 01_gemini_md.md 02_gemini_pdf.pdf 03_gpt.md \
          04_claude_signed.txt 05_grok_short.md \
          06_grok_refined.md 07_claude_review_note.md \
          ATTESTATIONS_LEDGER.md | sort | sha256sum
```

Expected master root: `dab3645de4efa05e43161e2227bee5508a3aa9ad86548dfd8ca20bd3bbee0a7d`

(Note: ATTESTATIONS_LEDGER.md may have been updated post-bundle. Original
ledger hash `b6657030de2ce6e921f9daa00b3750c19cd5d7a2f4ef08699fc3f09251ed95f4`
is on-chain at block #83687.)

### 3. Verify on-chain anchoring

```bash
ssh uncrfactory@37.97.202.97
python3 /tmp/verify_attestations.py
```

Expected: 8/8 ON-CHAIN MATCH on alpha-testnet blocks #83678–#83687.

## Note on Two Claude Attestations

Two separate Claude (Anthropic) instances participated in review, in
different sessions, and reached different conclusions about the
standard ATTESTATION template:

- `04_claude_signed.txt` (block #83682) — Signed standard template
  with extensive Section 3 disclaims
- `07_claude_review_note.md` (block #83685) — Declined template, signed
  alternative "Technical Review Note" form

Both are on-chain. The dissent is documented, not hidden. See
ATTESTATIONS_LEDGER.md "Important Note on Two Claude Attestations"
section for full context.

## What This Bundle Demonstrates

PopChain's anchoring infrastructure: cross-architecture SHA256 identity
check, on-chain proof submission, and master root construction applied
to AI review documents.

The bundle is a record of review activity. The mechanical truth is
the SHA256 identity across machines and the on-chain block heights.
Score and grade values are produced by PopChain's PoCC formula on the
chain itself; they describe internal chain accounting, not external
validation of attestation quality.

## Roadmap

Phase 0c continues with:
- P1.5 + P1.6 + P5 (parallel small wins)
- P1.7 XMSS^MT (beta blocker)
- P3 Python cross-implementation
- P2 cosignatures protocol
- P4 POP-1, POP-2 specifications
- P6 demo video
- P7 tokenomics framework

— Paweł Piekut, 2026-05-10
