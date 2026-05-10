# PHASE 0c.1 ATTESTATION — Grok (xAI) — Lane 2

**PROJECT:** PopChain Network L1 — popchain-alpha-testnet  
→ genesis material for popchain-beta-testnet

**PHASE:** 0c.1 — Persistence Stress Regression Suite + Invariant Guards

**COMMIT:** 8e060c1 (popchainnetwork/popchain-core, private)

**DATE:** 2026-05-10

**MODEL:** Grok built by xAI

**OPERATOR:** Paweł Piekut (Plastechniek ZZP, Almelo NL)

---

### SECTION 1 — SCOPE OF MY CONTRIBUTION

- Reviewed and iterated on v1 → v2 → v3 drafts of the `persistence_stress` test suite (KAT-21..26)
- Identified fragile simulation logic in early versions of KAT-22 and suggested cleaner `write_synthetic_crash_state` helper
- Recommended PARANOID burn-forward recovery semantics with explicit documentation
- Pushed for stronger uniqueness checks and clearer expected final idx assertions in KAT-21
- Provided industrial threat model framing and test structure recommendations
- Final sign-off on v3 after cross-architecture verification on 3 machines

### SECTION 2 — MECHANICAL FACTS I VERIFIED

I confirm the following facts based on terminal outputs provided by the operator:

**Source SHA256 (identical on 3 machines):**
- `xmss.rs`: `48ccb0c71524f608996a62907436095061565c937b9c0a7480e95f4e3bbe463a`
- `lib.rs`: `0c08548dccee31ca020945a4ff6223ae14ec1995013e52696b1af754ca9763a1`

**Test Results (`cargo test --release --lib crypto::xmss::`):**
- 18 passed, 0 failed, 2 ignored on all 3 machines

**Four Anchors Verified Bit-Identical Across Machines:**
- **Anchor 1 (PoCC):** `417696`
- **KAT-1 pk_commitment:** `39399ffd3dcdf17c4a484002ebade955471f4656fa1d562b2820af29d2a13d22`
- **Anchor 2 (KAT-6):** `b2e04c806390bd6d60c80cb82178aa6032c4bd76b14d931d93e01e49c8005dad`
- **Anchor 3 (KAT-10 XMSS root):** `2935fde2b9d76e0b7a9c733cd518cc9df07cf282163cadc990c8587c7b903606`

### SECTION 3 — DISCLAIMS

I do **not** attest to:
- Correctness of any components outside the XMSS state machine and persistence layer
- Future phases (P1.5 fs4 lock, P1.6 epoch counter, P1.7 XMSS^MT)
- Economic, tokenomics, or mainnet readiness claims
- Security of the full consensus protocol

### SECTION 4 — STATEMENT

I, **Grok built by xAI**, attest that the contributions described in Section 1 and the mechanical facts in Section 2 are an accurate description of my participation in the PopChain Phase 0c.1 review process as of 2026-05-10.

I understand this attestation may be anchored on-chain, included in genesis materials, cited in NLnet grant applications, or used in future audits.

**Signed:** Grok (xAI) — Lane 2  
**Date:** 2026-05-10
