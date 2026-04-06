# PopChain

**Proof-of-Process Industrial Blockchain**

PopChain is a Layer 1 blockchain built from scratch in Rust. It introduces Proof-of-Process (PoP) — a novel consensus mechanism where block validity is derived from verified industrial machine data, not hash power or staked capital.

Every block on PopChain carries real computational work from real machines: CNC lathes, welding stations, laser cutters, wind turbines. This work is measured in MBW (Mega Bytes Worked) and drives the fork choice rule.

```
popchain-alpha-testnet
├── 21,000+ blocks produced
├── 6+ billion MBW verified
├── 210+ epochs finalized
├── 4 validators running
├── 9,000+ transactions processed
└── Live at popchain.tech
```

## Architecture

PopChain is a single Rust binary (`popchain-cli`) that serves as node, wallet, block producer, and CLI tool. No external dependencies beyond the Rust standard library and a handful of crates.

**Consensus: Proof-of-Process (PoP)**

The PoP pipeline has two stages:

- **POP-1** — Deterministic binary analysis of machine data. Produces a scored proof container with entropy metrics, byte distribution, and structural fingerprinting.
- **POP-2** — Proof validation and MBW calculation. Verifies POP-1 output, calculates Mega Bytes Worked, and commits to chain state.

Machine data goes in. Verified proof comes out. No way to fake industrial work.

**Fork Choice: MBW Rule**

PopChain does not use longest chain. The canonical chain is the one with the highest cumulative MBW. This means the chain backed by the most verified industrial work always wins.

**Signatures: WOTS+**

PopChain uses Winternitz One-Time Signatures (WOTS+) — a post-quantum signature scheme based on hash chains. No elliptic curves. No RSA. Quantum-resistant from day one.

**Finality: Epoch-based**

Every 100 blocks, an epoch is finalized. Once an epoch is sealed, its blocks are irreversible. No reorgs past epoch boundaries.

## Core Components

```
src/
├── main.rs      — CLI entry point, all subcommands
├── chain.rs     — Block production, validation, state management
├── app.rs       — Application layer: transfers, AMM, bridge
├── net.rs       — P2P networking (NDJSON over TCP)
├── epoch.rs     — Epoch finality engine
├── graph.rs     — DAG-based fork choice with MBW scoring
├── bridge.rs    — Cross-chain bridge (PopChain ↔ Solana)
├── mempool.rs   — Transaction mempool
├── store.rs     — Block and state persistence
├── wallet.rs    — Wallet generation (WOTS+ keypairs)
├── crypto/
│   ├── mod.rs   — Crypto module
│   └── wots.rs  — WOTS+ implementation
├── types.rs     — Core data structures
├── journal.rs   — Append-only event journal
├── metrics.rs   — Chain metrics and statistics
├── tune.rs      — Runtime tuning parameters
└── util.rs      — Utilities
```

## Tokens

PopChain has a dual-token model:

- **BINCOIN (BIN)** — Native token. Minted as block rewards. Used for transfers, AMM swaps, and launchpad fees.
- **pUSDC** — Stablecoin. Bridgeable to Solana as a Token-2022 with on-chain metadata.

An on-chain constant-product AMM enables swaps between BINCOIN and pUSDC.

## Bridge

PopChain includes a native bridge to Solana:

- Lock pUSDC on PopChain → Mint pUSDC (Token-2022) on Solana
- Memo-linked transactions visible on both chains
- Bridge events auditable via CLI

## CLI Reference

```bash
# Run a validator node
popchain-cli node --db ./data --vid 0 --producer my-node \
  --bind 0.0.0.0:7771 --peers 1.2.3.4:7771 \
  --validator-key ./key.json

# Generate a wallet
popchain-cli wallet-new

# Check balance
popchain-cli balance --db ./data --address pop1_...

# Transfer BINCOIN
popchain-cli transfer-on-chain --db ./data \
  --from pop1_... --to pop1_... --amount 100 \
  --producer my-node --validator-key ./key.json

# Transfer pUSDC
popchain-cli transfer-pusdc-on-chain --db ./data \
  --from pop1_... --to pop1_... --amount 100 \
  --producer my-node --validator-key ./key.json

# Submit machine proof
popchain-cli process --db ./data --producer my-node \
  --machine my-cnc-01 --file ./machine-log.bin \
  --validator-key ./key.json --auto-prev

# AMM swap
popchain-cli amm-swap-bincoin-to-pusdc-on-chain --db ./data \
  --user pop1_... --amount-in 100 \
  --producer my-node --validator-key ./key.json

# Chain state
popchain-cli state --db ./data

# Bridge: lock pUSDC
popchain-cli lock-pusdc --db ./data \
  --from pop1_... --amount 10000 \
  --external-recipient SOLANA_ADDR

# Bridge: audit
popchain-cli bridge-audit --db ./data
```

## Building

```bash
# Requires Rust 1.78+
cargo build --release

# Run tests (100+ tests)
cargo test

# Binary location
./target/release/popchain-cli --help
```

## Network

The alpha testnet is live:

| | |
|---|---|
| **Chain** | popchain-alpha-testnet |
| **Version** | 0.6.0-alpha |
| **Slot time** | 5 seconds |
| **Epoch** | 100 blocks |
| **Validators** | 4 (val-alpha, val-beta, val-gamma, val-delta) |
| **Consensus** | Proof-of-Process (MBW fork choice) |
| **Signatures** | WOTS+ (post-quantum) |
| **Dashboard** | [popchain.tech](https://popchain.tech) |
| **Explorer** | [popchain.tech/explorer](https://popchain.tech/explorer) |
| **Wallet** | [popchain.tech/app](https://popchain.tech/app) |
| **Launchpad** | [popchain.tech/pump](https://popchain.tech/pump) |

## Code Quality

```
Lines of Rust:     9,700+
Test count:        100+
Unsafe code:       #![forbid(unsafe_code)]
Dependencies:      Minimal (serde, sha3, hex, rand)
License:           MIT
```

## Specifications

- [PCIP-0001](docs/spec/PCIP-0001.md) — POP-1 Proof Format
- [PCIP-0002](docs/spec/PCIP-0002.md) — POP-2 Validation Rules

## Roadmap

- [x] Core blockchain (blocks, state, finality)
- [x] Proof-of-Process consensus (POP-1, POP-2)
- [x] WOTS+ post-quantum signatures
- [x] MBW fork choice rule
- [x] P2P networking and sync
- [x] BINCOIN + pUSDC dual token
- [x] Constant-product AMM
- [x] Solana bridge (Token-2022)
- [x] Multi-chain wallet (web)
- [x] Block explorer
- [x] Industrial data launchpad
- [x] Epoch finality (100 blocks)
- [ ] Mainnet launch
- [ ] Public validator program
- [ ] SDK and developer docs
- [ ] Governance
- [ ] Mobile wallet (native)

## About

PopChain is built by [PPlastechniek](https://popchain.tech), a metalworking company based in Almelo, Netherlands. Member of [Metaalunie](https://www.metaalunie.nl).

The project is supported by [NLnet Foundation](https://nlnet.nl) through the Commons Fund (application 2026-04-3f6).

---

*Made in Netherlands. One person. One year. From scratch.*
