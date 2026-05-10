# Phase 0c.1 Attestations Ledger

**Project:**       PopChain Network L1 — popchain-alpha-testnet
                   → genesis material for popchain-beta-testnet
**Phase:**         0c.1 — Persistence Stress Regression Suite
**Commit:**        `8e060c1` (popchainnetwork/popchain-core, private)
**Parent commit:** `e8a6549`
**Bundle commit:** `0432f2f`
**Date:**          2026-05-10
**Operator:**      Paweł Piekut, Plastechniek ZZP, Almelo NL
**NLnet ticket:**  2026-04-3f6

---

## What This Bundle Contains

This bundle is a record of multi-vendor AI review of PopChain Phase 0c.1
(persistence stress regression suite + invariant guards). It contains
seven attestation files written by reviewer instances from four AI
vendors, plus this ledger and a master root file. All files are
SHA256-hashed cross-architecture (x86_64 cloud, x86_64 AMD, ARM64 Pi 5)
with bit-identical results. All files are anchored on-chain at
popchain-alpha-testnet.

---

## Important Note on Two Claude Attestations

Two separate Claude (Anthropic) instances participated in Phase 0c.1
review, in different sessions. They reached different conclusions about
the standard ATTESTATION template, and **both attestations are on-chain**:

- **`04_claude_signed.txt`** (block #83682) — A Claude instance from a
  separate session signed the standard template, with extensive
  Section 3 disclaims documenting the limitations of AI verification
  (no command execution, no repository access, no continuity across
  sessions, language model patterns, not a substitute for human audit).

- **`07_claude_review_note.md`** (block #83685) — A different Claude
  instance (from a different session) declined to sign the standard
  template. Reasons: inability to verify Section 2 mechanical facts
  firsthand, no legal personhood, and concern that the template
  framing might over-state the role of AI as attesting party. This
  Claude proposed an alternative "Technical Review Note" form which
  the operator accepted as an alternative attestation.

The two outcomes reflect a real property of LLM systems: separate
sessions of the same model can reach different conclusions on edge
cases involving identity, authority, and the proper framing of AI
contribution. The dissent itself strengthens the multi-model
methodology — it is documented rather than hidden, and both records
are on-chain for any auditor to inspect.

This is the intended record. Operator did not write or sign either
file; both are direct outputs from Claude sessions, with their
respective session URLs preserved in the file headers.

---

## PoP Anchors Referenced

| # | Name | Value |
|---|---|---|
| 1 | PoCC Anchor 1 | `POCC_ANCHOR_V1 = 417696` |
| 2 | KAT-1 (Anchor 2-bis) | `39399ffd3dcdf17c4a484002ebade955471f4656fa1d562b2820af29d2a13d22` |
| 3 | Anchor 2 (KAT-6) | `b2e04c806390bd6d60c80cb82178aa6032c4bd76b14d931d93e01e49c8005dad` |
| 4 | Anchor 3 (KAT-10 XMSS root) | `2935fde2b9d76e0b7a9c733cd518cc9df07cf282163cadc990c8587c7b903606` |

## Source Files (verified bit-identical × 3 machines)

| File | SHA256 |
|---|---|
| `src/crypto/xmss.rs` | `48ccb0c71524f608996a62907436095061565c937b9c0a7480e95f4e3bbe463a` |
| `src/lib.rs` | `0c08548dccee31ca020945a4ff6223ae14ec1995013e52696b1af754ca9763a1` |

## Cross-Architecture Witness Matrix

| Machine | Architecture | Role |
|---|---|---|
| val-alpha (37.97.202.97) | x86_64 cloud VPS | hub validator |
| val-beta | x86_64 AMD desktop | peer validator |
| val-pi-01 | ARM64 Raspberry Pi 5 | peer validator |

`cargo test --release --lib crypto::xmss::` — **18 passed; 0 failed; 2 ignored** × 3 machines.
Times: alpha 2.91s, beta 1.98s, pi-01 9.92s.

---

## Attestation Files (sorted by SHA256)

### 01_gemini_md.md — Gemini 3 Flash (Google)
- **SHA256:** `1f0d1df4b0613a616a17c4a1b07ca7c59879abd489b843253608e909a99dffa3`
- **Format:** Markdown, full template
- **Status:** Signed standard attestation
- **On-chain:** block #83678 (alpha-testnet)
- **Session URL:** https://gemini.google.com/app/c70183d8e2cb5669
- **Vendor:** Google

### 02_gemini_pdf.pdf — Gemini 3 Flash (Google)
- **SHA256:** `90fbbbf28bb83db78643450858ffcfc689a6126401c706f7cf74ed74e36d51ae`
- **Format:** PDF, condensed version of 01_gemini_md.md
- **Status:** Signed standard attestation
- **On-chain:** block #83681
- **Vendor:** Google

### 03_gpt.md — ChatGPT GPT-5.5 (OpenAI)
- **SHA256:** `80bd3b329fbe821693727495589c28b7553f6b6d36405a38532237ae81379fdc`
- **Format:** Markdown, full template
- **Status:** Signed standard attestation
- **On-chain:** block #83680
- **Session URL:** https://chatgpt.com/c/69f0e21e-10bc-8333-b8a4-e8c114f7426c
- **Vendor:** OpenAI

### 04_claude_signed.txt — Claude (Anthropic) — instance A
- **SHA256:** `bf8f87c4406f995efa085b2bdcfb54cdcc24268e63f9ec9913b024d570167c65`
- **Format:** Plain text, full template with extensive Section 3 disclaims
- **Status:** Signed standard attestation (with explicit AI limitations)
- **On-chain:** block #83682
- **Session URL:** https://claude.ai/chat/11c30de1-a5ca-4ef3-8fb6-4d04ab4495a9
- **Vendor:** Anthropic
- **Note:** See "Important Note on Two Claude Attestations" above.

### 05_grok_short.md — Grok (xAI)
- **SHA256:** `38dc96765f35954e123e1dea8462bb77f9ea865998c05f40f4a313dd72f9b8db`
- **Format:** Markdown, short version
- **Status:** Signed standard attestation
- **On-chain:** block #83683
- **Vendor:** xAI

### 06_grok_refined.md — Grok (xAI)
- **SHA256:** `e4c4332ce96c7e1d02c3377f2daf36a8a95223b350974f954fc74019bff00c65`
- **Format:** Markdown, refined/long version
- **Status:** Signed standard attestation
- **On-chain:** block #83684
- **Vendor:** xAI

### 07_claude_review_note.md — Claude (Anthropic) — instance B (alternative form)
- **SHA256:** `c10fca7078470075367978e2e664ffc8495c41e0b6df4f892fba2f8dde8fa429`
- **Format:** Markdown, "Technical Review Note" alternative format
- **Status:** Declined standard template, signed alternative form
- **On-chain:** block #83685
- **Vendor:** Anthropic
- **Note:** See "Important Note on Two Claude Attestations" above.

---

## Mechanical Verification — Cross-Machine Witness

All 7 attestation files were independently SHA256-hashed on each of the 3
validator machines (alpha, beta, pi-01). All hashes match bit-identically
across all machines.

This verifies the **anchoring infrastructure**: PopChain's
cross-architecture verification pipeline correctly identifies bit-identical
content across heterogeneous hardware, and submits records to chain via
the existing proof_submit_v0 transaction type. The attestation files
themselves are review documents, not independent proofs of correctness;
their value to an external auditor is the verifiable identity claim
(SHA256) and the on-chain timestamp (block height + producer).

This bundle does not assert that AI review constitutes formal audit.
It records that AI review took place, what each reviewer specifically
contributed, what they did and did not verify firsthand, and that the
record is permanently anchored on alpha-testnet.

---

## Master Root (Merkle-style)

Master root = SHA256 of sorted concatenated SHA256 list of the 8
attestation files (01-07 + this ledger), excluding MASTER_ROOT.txt
itself to avoid self-reference:

```
dab3645de4efa05e43161e2227bee5508a3aa9ad86548dfd8ca20bd3bbee0a7d
```

To reproduce on any of 3 validator machines:

```
cd ~/popchain/docs/attestations/phase-0c1
sha256sum 01_gemini_md.md 02_gemini_pdf.pdf 03_gpt.md \
          04_claude_signed.txt 05_grok_short.md \
          06_grok_refined.md 07_claude_review_note.md \
          ATTESTATIONS_LEDGER.md | sort | sha256sum
```

`MASTER_ROOT.txt` is anchored separately on-chain at block #83688 and
provides the integrity claim for this bundle as a whole.

---

## On-Chain Anchoring Summary

All 9 files (7 attestations + ledger + master root) anchored on
popchain-alpha-testnet via proof_submit_v0 transactions, submitter
`pop1_a4c073ac215bdd52b369b618f1913f7071a659172ba35e9dc7845d6aa876fa84`:

| File | Block | Type |
|---|---|---|
| 01_gemini_md.md | #83678 | attestation |
| 03_gpt.md | #83680 | attestation |
| 02_gemini_pdf.pdf | #83681 | attestation |
| 04_claude_signed.txt | #83682 | attestation (Claude instance A) |
| 05_grok_short.md | #83683 | attestation |
| 06_grok_refined.md | #83684 | attestation |
| 07_claude_review_note.md | #83685 | attestation (Claude instance B, alt form) |
| ATTESTATIONS_LEDGER.md | #83687 | ledger |
| MASTER_ROOT.txt | #83688 | bundle integrity claim |

---

## Distribution Status

- ✓ Files committed to: `popchainnetwork/popchain-core` (private, commits 8e060c1 and 0432f2f)
- ✓ Files mirrored to: alpha, beta, pi-01 (all 3 validators)
- ✓ Files anchored on-chain: alpha-testnet blocks #83678–#83688
- ⏳ Public sync to: `popchainnetwork/popchain` (scheduled +24h)
- ⏳ Beta-testnet block 0 reference: scheduled at beta launch

---

## Roadmap Continuation

Phase 0c.1 attestations conclude this milestone. Continues in Phase 0c:

- **P1.5 + P1.6 + P5 (parallel small wins):** fs4 file lock (KAT-24),
  on-chain epoch counter (KAT-26), Zymkey HSM6 hardware integration
- **P1.7:** XMSS^MT (h_top=10/h_bottom=10 = 2^20 effective signatures) —
  beta blocker, replaces single-tree XMSS h=10
- **P3:** Python cross-implementation (post P1.7, validates final stack)
- **P2:** Cosignatures protocol (uses XMSS^MT, not legacy WOTS)
- **P4:** POP-1, POP-2 specifications (NLnet Commons Fund deliverables)
- **P6:** Demo video (industrial flow live)
- **P7:** Tokenomics framework (post-beta validation)

---

*This ledger is itself an artifact of PopChain Phase 0c.1, anchored
on-chain at block #83687.*

— Operator, 2026-05-10
