# PopChain: Proof-of-Process Industrial Blockchain

## Whitepaper v0.6 — April 2026

**Paweł Piekut**
PPlastechniek · Almelo, Netherlands
popchain.tech

---

## Abstract

PopChain is a Layer 1 blockchain that derives consensus from verified industrial machine data rather than hash computation or staked capital. We introduce Proof-of-Process (PoP), a two-stage deterministic pipeline that validates binary data from industrial machines — welding stations, CNC mills, laser cutters, turbines — and produces a tamper-evident proof scored in Mega Bytes Worked (MBW). The chain with the highest cumulative MBW is canonical. This design ties blockchain security directly to real economic activity, creating a network where block production requires genuine industrial output.

PopChain is implemented in Rust with 9,700+ lines of code, zero unsafe blocks, and 100+ tests. The alpha testnet has produced 21,000+ blocks across 4 validators with 6+ billion MBW of verified industrial data.

---

## 1. Introduction

### 1.1 The Problem

Existing blockchain consensus mechanisms are disconnected from real economic value:

- **Proof-of-Work** consumes electricity to compute hashes that serve no purpose beyond securing the chain. The work is deliberately useless.
- **Proof-of-Stake** requires capital lockup but produces no external value. Security derives from the threat of capital loss, not from productive activity.
- **Delegated systems** centralize authority in a small set of validators chosen by token-weighted voting.

None of these mechanisms create a link between blockchain consensus and real-world economic production.

### 1.2 The Opportunity

Industrial manufacturing generates enormous volumes of binary data: sensor readings, process logs, control parameters, quality metrics. This data is produced continuously by machines that are already running for economic reasons. It is deterministic, verifiable, and economically meaningful.

PopChain uses this existing data stream as the basis for consensus. Machines that are already producing economic value simultaneously secure the blockchain. No additional energy is wasted. No capital sits idle.

### 1.3 Design Goals

1. **Useful consensus** — Block production requires data from real industrial processes
2. **Deterministic verification** — Any node can independently verify any proof
3. **Post-quantum security** — No reliance on elliptic curve assumptions
4. **Minimal complexity** — Single binary, minimal dependencies, auditable code
5. **Industrial data marketplace** — Tokenized machine data accessible to AI/ML consumers

---

## 2. Proof-of-Process (PoP)

### 2.1 Overview

Proof-of-Process is a two-stage pipeline that transforms raw industrial binary data into a verifiable proof with a deterministic MBW score.

```
Raw Machine Data → [POP-1: Analysis] → [POP-2: Validation] → Proof + MBW Score
```

### 2.2 POP-1: Deterministic Binary Analysis

POP-1 takes a binary input file (machine log, sensor dump, process recording) and produces a proof container with:

- **Byte frequency distribution** — Statistical fingerprint of the data
- **Entropy measurement** — Shannon entropy per block, detecting structure vs randomness
- **Structural markers** — Identification of headers, repeating patterns, data boundaries
- **Size metrics** — Raw size, effective information content
- **Deterministic hash** — SHA3-256 of the processed output

POP-1 is fully deterministic: the same input always produces the same output. There is no randomness, no external oracle, no timestamp dependency.

### 2.3 POP-2: Validation and Scoring

POP-2 takes the POP-1 output and:

- **Validates the proof container** — Verifies internal consistency
- **Calculates MBW** — Mega Bytes Worked score based on data complexity and size
- **Rejects invalid proofs** — Detects padding, repetition, synthetic data
- **Commits to chain state** — Links the proof to a block and updates cumulative MBW

### 2.4 MBW Scoring

MBW (Mega Bytes Worked) is the fundamental unit of consensus weight. It is calculated from:

```
MBW = f(data_size, entropy, structural_complexity, uniqueness)
```

Higher entropy data (real sensor readings) scores higher than low entropy data (padded files). This makes it economically rational to submit genuine machine data rather than fabricated inputs.

### 2.5 Anti-Gaming

The PoP pipeline includes defenses against synthetic data:

- **Entropy thresholds** — Reject data below minimum entropy
- **Pattern detection** — Identify and penalize repetitive structures
- **Size-entropy ratio** — Large files with low entropy are penalized
- **Cross-proof correlation** — Detect duplicate submissions across blocks

---

## 3. Consensus

### 3.1 Fork Choice: MBW Rule

PopChain does not use longest chain. The canonical chain is determined by cumulative MBW:

```
canonical_chain = argmax(chain.cumulative_mbw)
```

This means the chain backed by the most verified industrial work is always selected. An attacker would need to produce more genuine industrial data than the honest network — requiring actual machines doing actual work.

### 3.2 Block Production

Validators take turns producing blocks based on a slot schedule:

- **Slot duration**: 5 seconds
- **Leader selection**: Round-robin by validator index per slot
- **Block contents**: Transactions + PoP proofs + state root

Each block includes zero or more PoP proofs submitted by machines connected to the network. The block producer validates all proofs through POP-2 before inclusion.

### 3.3 Epoch Finality

Every 100 blocks, an epoch boundary is created:

- All blocks in the epoch are sealed
- State root is committed
- No reorgs are possible past the epoch boundary
- Validator rewards are distributed

This provides deterministic finality with a maximum confirmation time of 500 seconds (100 slots × 5 seconds).

---

## 4. Cryptography

### 4.1 WOTS+ Signatures

PopChain uses Winternitz One-Time Signatures Plus (WOTS+), a hash-based signature scheme that is:

- **Post-quantum secure** — Based on hash function preimage resistance, not discrete logarithm or factoring
- **Well-studied** — Standardized in XMSS (RFC 8391)
- **Simple** — Implementation in pure Rust, no external crypto libraries
- **Compact verification** — Efficient for blockchain use

Each validator has a WOTS+ keypair. Block signatures are verified using the public key root committed in the genesis block.

### 4.2 Hash Functions

- **Block hashing**: SHA3-256
- **State root**: Merkle tree with SHA3-256
- **WOTS+**: SHA3-256 hash chains

---

## 5. Network

### 5.1 P2P Protocol

Nodes communicate via NDJSON (newline-delimited JSON) over TCP:

- **Block propagation** — New blocks are broadcast to all connected peers
- **Sync protocol** — New nodes request missing blocks by height
- **Transaction relay** — Mempool transactions propagated on submission

### 5.2 Validator Set

The validator set is defined in the genesis block. The alpha testnet runs 4 validators. The mainnet will support a configurable validator set with a governance-based addition process.

---

## 6. Economics

### 6.1 Token Model

PopChain has a dual-token model:

**BINCOIN (BIN)**
- Native token of PopChain
- Minted as block rewards to validators
- Used for transaction fees, AMM swaps, and launchpad operations
- Genesis supply: 13,000,000 BIN

**pUSDC**
- Stablecoin on PopChain
- Bridgeable to Solana as Token-2022
- Used for B2B settlements and data marketplace payments
- Genesis supply: 500,000 pUSDC

### 6.2 Block Rewards

Each block produces a BINCOIN reward proportional to the MBW contained in the block. Blocks with more PoP proofs generate higher rewards, incentivizing validators to include machine data.

### 6.3 AMM

PopChain includes a native constant-product AMM (Automated Market Maker) for BINCOIN/pUSDC swaps:

```
x * y = k
```

Where x is the BINCOIN reserve, y is the pUSDC reserve, and k is the constant product. This enables on-chain price discovery without external oracles.

### 6.4 Industrial Data Marketplace

Companies register on PopChain through the Launchpad and receive a company token (e.g., $PPL for PPlastechniek). The economic flow:

1. Company submits machine logs → PoP proofs on chain
2. Company token value grows with MBW backing
3. AI/ML companies purchase tokens to access industrial training data
4. Company earns BINCOIN from data sales
5. PopChain earns fees from all transactions

This creates a circular economy where industrial data production drives both consensus security and economic value.

---

## 7. Bridge

### 7.1 PopChain ↔ Solana

PopChain includes a native bridge to Solana:

1. **Lock** — User locks pUSDC on PopChain, specifying a Solana recipient
2. **Mint** — Bridge operator mints pUSDC (Token-2022) on Solana with metadata
3. **Memo** — Solana transaction includes a memo linking back to PopChain lock event
4. **Audit** — All bridge events are auditable via CLI

The pUSDC token on Solana uses the Token-2022 standard with on-chain metadata (name, symbol, URI) pointing to PopChain.

### 7.2 Bridge Security

Bridge events are recorded on both chains with cross-references:

- PopChain records: lock ID, amount, Solana recipient, external TX hash
- Solana records: memo with PopChain lock ID, amount, source address

---

## 8. Implementation

### 8.1 Code

- **Language**: Rust
- **Lines of code**: 9,700+
- **Tests**: 100+
- **Safety**: `#![forbid(unsafe_code)]` — zero unsafe blocks
- **Dependencies**: Minimal (serde, sha3, hex, rand)
- **Binary**: Single `popchain-cli` executable

### 8.2 Module Structure

| Module | Purpose |
|--------|---------|
| `chain.rs` | Block production, validation, state |
| `app.rs` | Transfers, AMM, bridge operations |
| `net.rs` | P2P networking |
| `epoch.rs` | Epoch finality |
| `graph.rs` | DAG fork choice with MBW |
| `bridge.rs` | Cross-chain bridge |
| `crypto/wots.rs` | WOTS+ signatures |
| `mempool.rs` | Transaction mempool |
| `store.rs` | Persistence |
| `wallet.rs` | Key generation |

### 8.3 Testnet Status

| Metric | Value |
|--------|-------|
| Blocks | 21,000+ |
| MBW | 6+ billion |
| Epochs | 210+ |
| Validators | 4 |
| Transactions | 9,000+ |
| Slot time | 5 seconds |
| Network | popchain-alpha-testnet |

---

## 9. Use Cases

### 9.1 Industrial Data Tokenization

Manufacturing companies tokenize their machine data on PopChain. Each company gets a token that represents access to their industrial datasets — welding parameters, CNC toolpaths, sensor readings, quality metrics.

### 9.2 AI Training Data Marketplace

AI companies need real-world industrial data for model training. PopChain provides a verified, on-chain marketplace where data provenance is guaranteed by the PoP pipeline.

### 9.3 B2B Settlement

Companies within industrial networks (e.g., Metaalunie members) use BINCOIN and company tokens for inter-company settlements, eliminating bank transfer delays and fees.

### 9.4 Supply Chain Verification

Product provenance is recorded on-chain through machine proofs. A welded joint can be traced back to the specific machine, operator shift, and process parameters that produced it.

---

## 10. Roadmap

| Phase | Status | Description |
|-------|--------|-------------|
| Core Protocol | ✅ Complete | Blockchain, PoP consensus, WOTS+, finality |
| Alpha Testnet | ✅ Live | 4 validators, 21K+ blocks, public dashboard |
| Wallet & Explorer | ✅ Live | Web wallet, block explorer, address pages |
| AMM & Bridge | ✅ Live | BINCOIN/pUSDC swap, Solana bridge |
| Data Launchpad | ✅ Live | Company registration, token creation |
| Public Testnet | 🔄 Next | Open validator participation |
| Mainnet | 📋 Planned | Production network launch |
| SDK | 📋 Planned | Developer toolkit and documentation |
| Governance | 📋 Planned | On-chain governance for protocol updates |

---

## 11. Conclusion

PopChain demonstrates that blockchain consensus can be derived from useful industrial work rather than wasteful computation or idle capital. By connecting block production to real machine data, we create a network where security, economic value, and industrial productivity are aligned.

The alpha testnet proves this design works: 21,000+ blocks produced by 4 validators, backed by 6+ billion bytes of verified industrial data, with a functioning wallet, explorer, AMM, bridge, and data marketplace.

PopChain is not a whitepaper project. It is running code, built from scratch, producing blocks right now.

---

## References

1. Buchmann, J., et al. "XMSS — A Practical Forward Secure Signature Scheme based on Minimal Security Assumptions." RFC 8391, 2018.
2. Nakamoto, S. "Bitcoin: A Peer-to-Peer Electronic Cash System." 2008.
3. Buterin, V. "Ethereum Whitepaper." 2014.
4. Yakovenko, A. "Solana: A New Architecture for a High Performance Blockchain." 2018.

---

*PopChain Network — Made in Netherlands — PPlastechniek 2026*
*popchain.tech*
