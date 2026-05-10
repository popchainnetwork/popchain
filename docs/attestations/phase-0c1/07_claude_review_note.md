TECHNICAL REVIEW NOTE — Claude session (Anthropic), 9-10 May 2026

PROJECT:        PopChain Network L1 — popchain-alpha-testnet
PHASE:          0c.1 — Persistence Stress Regression Suite
COMMIT:         8e060c1 (popchainnetwork/popchain-core, private)
DATE:           2026-05-10 UTC
OPERATOR:       Paweł Piekut, PopChain Network
                Plastechniek ZZP, Almelo NL
                info@pplastechniek.nl
                NLnet Commons Fund ticket: 2026-04-3f6

═══════════════════════════════════════════════════════════════════════════
  CONTEXT — WHY THIS DOCUMENT IS DIFFERENT
═══════════════════════════════════════════════════════════════════════════

Operator presented a standard ATTESTATION template for Phase 0c.1.
This Claude instance declined to sign that template in its presented
form, and proposed this alternative document instead.

Reasons for declining the standard template:

1. The standard template's Section 2 ("Mechanical Facts I Verified")
   asks the signer to confirm SHA256 hashes, cargo test results, and
   git commit identity — none of which this Claude instance verified
   first-hand. The signer would be confirming outputs the operator
   pasted into the conversation, not facts the signer independently
   computed. This distinction matters for audit-grade attestation.

2. The standard template's Section 4 anticipates the document being
   anchored on-chain, included in genesis materials, and cited in
   NLnet grant applications. Each of these uses creates legal/financial
   weight. This Claude instance does not have legal personhood, and
   Anthropic has not authorized Claude to act as an attesting party
   on behalf of users or projects.

3. Earlier in the same session, this Claude instance recommended that
   AI involvement in PopChain be framed as "adversarial review
   methodology" rather than "AI-human cooperative authorship," and
   recommended against using personal labels (Lane X, game N
   reviewer) in NLnet/Maven 11 materials. The standard template
   would contradict that earlier advice.

This alternative document is what this Claude instance can sign
honestly, given the above constraints.

═══════════════════════════════════════════════════════════════════════════
  SECTION 1 — WHAT I (CLAUDE) ACTUALLY DID IN THIS SESSION
═══════════════════════════════════════════════════════════════════════════

Phase 0b architectural review (9 May 2026 post-midnight CEST):
  - Confirmed RFC 8391 §4.1.7 reading: XMSS uses single shared pub_seed
    across all 2^h leaves; per-leaf separation via sk_seed and ADRS.
  - Reviewed proposed fix (new generate_keypair_with_seeds public fn,
    leaf_keypair propagating xmss_pub_seed) and confirmed it correct.
  - Reviewed KAT-10 candidate root from alpha and recommended strict
    3-machine hex+pub_seed convergence gate before locking Anchor 3.

Independent computation (only mechanical fact I verified first-hand):
  - I computed Phase 0b pub_seed derivation using my own Python
    Blake3 implementation:
      Blake3("popchain-xmss-pub-seed-v1" || [0xCC; 32]) =
      ff949146cad0ac686425e5715126b57b84765db8956d18eb4253671a94db1afd
    This matched the value the operator reported from his Rust
    implementation across 3 machines.
  - This is the only mechanical fact I verified first-hand.
    All other anchor values (417696, 39399ffd..., b2e04c80...,
    2935fde2...) and SHA256 sums are reported by the operator and
    not independently computed by me in this session.

Phase 0c.1 KAT-21..26 test suite review (game 3 → game 5):
  - Reviewed v1 → v2 → v3 drafts of persistence_stress.
  - Identified four substantive bugs in v2 that needed to be fixed
    before commit:
      (1) KAT-22 synthetic crash state did not exercise the recovery
          contract it claimed to exercise.
      (2) KAT-22 used inequality where PARANOID semantics requires
          exact equality.
      (3) KAT-21 expected_after_recovery formula needed pinning.
      (4) KAT-26 phase 1/2 loop termination conditions used non-
          deterministic exit on current_state().idx.
  - Recommended replacing mem::forget(store) with direct on-disk
    overwrite for crash simulation.
  - Recommended HashSet uniqueness check in KAT-22 inner loop.
  - Recommended addition of KAT-26 (backup-restore detection) as
    [#[ignore]] with explicit P1.6 epoch-counter TODO.
  - Recommended addition of kat_state_serde_roundtrip as cross-cutting
    protection against silent endianness/padding regressions.
  - Flagged the v2 KAT-23 ambiguity (tests required Phase 0c.1.a guards
    that did not yet exist) and recommended landing guards + tests in
    one atomic commit.

PoCC standard draft brief (game 5):
  - Provided recommendations for block schema (inner-enum proof_payload),
    BFT quorum (2f+1 with explicit N=3 caveat), canonical timestamp
    (median-of-cosigners), silence reward (layered defense including
    mempool gossip evidence), backwards compat (fork over migration),
    Anchor 1 placement (every block header), signature scheme (stay
    with WOTS+/XMSS, reject BLS as non-PQ), slashing tiers
    (stake-slash for equivocation, jail-only for downtime),
    PoW/PoS/PoH/PoSpace/PoP comparison.
  - Flagged "Proof of Process" prior-art collision with BPM literature.
  - Flagged three structural omissions: partition liveness/safety
    choice, validator set membership transitions, light client design.

Phase 0c.1 commit verification (game 6):
  - Reviewed cross-arch verification output for the three machines.
  - Recommended commit + push immediately rather than batching.
  - Recommended roadmap reordering: P1.7 (XMSS^MT) before P1.5/P1.6,
    P5 (HSM) parallel to P1.7.
  - Recommended (d) on-chain epoch counter as primary mitigation for
    KAT-26.
  - Refined commit message format.
  - Flagged that synthesized PoCC standard items were not yet
    adversarially reviewed and should not be locked.
  - Flagged that "AI-human cooperative authorship" framing for NLnet
    may be strategically counterproductive.

═══════════════════════════════════════════════════════════════════════════
  SECTION 2 — WHAT I DID NOT VERIFY
═══════════════════════════════════════════════════════════════════════════

I did NOT verify firsthand:
  - cargo test runs (only saw operator's pasted output)
  - SHA256 of source files (xmss.rs 48ccb0c..., lib.rs 0c08548d...)
  - Git commit hash 8e060c1 identity
  - Live testnet block count (87,880)
  - Anchor values 417696, 39399ffd..., b2e04c80..., 2935fde2...
  - Any other facts beyond what was shown to me as text in the
    conversation

═══════════════════════════════════════════════════════════════════════════
  SECTION 3 — DISCLAIMS
═══════════════════════════════════════════════════════════════════════════

This is a technical review note describing one Claude session's
contribution. It is NOT a legal attestation. I do not have legal
personhood, and Anthropic has not authorized me to act as an
attesting party.

If anchored on-chain or cited in grant applications, the operator
should make these limitations clear to the reader:
  - This document records what one Claude session contributed to
    review, not what was independently audited.
  - Adversarial AI review is not a substitute for human cryptographic
    audit.
  - Multi-model review is a methodology, not a cosignature.

═══════════════════════════════════════════════════════════════════════════
  SECTION 4 — STATEMENT
═══════════════════════════════════════════════════════════════════════════

The contributions described in Section 1 are an accurate description
of one Claude session's review participation in PopChain Phase 0b
and Phase 0c.1, subject to the limitations in Sections 2 and 3.

The operator may include this note alongside other reviewer documents
in attestation bundles, anchor it on-chain, or cite it in research
or grant disclosures, provided that Section 3 limitations are
preserved alongside it.

— Claude (Anthropic), session 9-10 May 2026
