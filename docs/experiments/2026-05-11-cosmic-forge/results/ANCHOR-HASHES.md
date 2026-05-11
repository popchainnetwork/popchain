# Anchor Hashes - Cosmic Forge Canonical Reference

This file is the master canonical hash registry for the Cosmic Forge experiment series. Every value below is a fixed reference. A conforming third-party implementation of POP-2-COMPUTE following `METHODOLOGY.md` and `DETERMINISM-RULE.md` is expected to reproduce these hashes on Ampere-generation NVIDIA GPUs with CUDA 12.9 and IEEE 754 binary32/binary64 arithmetic.

The hashes are presented in a single table for indexing and machine reading. Detailed parameters per experiment are in `REPRODUCIBILITY.md`.

---

## Format

```
EXPERIMENT_ID                                  HASH (SHA-256 hex)
EXPERIMENT_ID.field                            HASH (SHA-256 hex)
```

---

## Table

### Experiment 001 - r-process-toy-v0

```
exp001.final_state_hash                        7990495ca63b098b1622be841307f1d44acffb7b548e84832a3754defb19a031
```

### Experiment 002 - r-process-v1-MEGA

```
exp002.main_run_final_hash                     964675b8799786e1f7a44c5a0193d09768e520c42d7c8fb2088792baef0efcf9
exp002.determinism_common_hash                 44db2a94694552918872e56169bbe30efc1e9305cf6ba12d77506d71273d820c
exp002.cross_seed.chain_mbw_v0                 44db2a94694552918872e56169bbe30efc1e9305cf6ba12d77506d71273d820c
exp002.cross_seed.pocc_anchor                  ea51aef714c0310a8ebec1f7098dd9c85b226c6e4eff403068a83f075775fa5f
exp002.cross_seed.kat6_prefix                  4b128bbd71749853b1f7a931db242e12a1f323151fab9fa1ec963e30bca2afac
```

### Experiment 003 - hypermassive-multiphysics-collider-v0 (float atomics, expected NON-DETERMINISTIC)

```
exp003.determinism_check                       FAIL (3 distinct hashes by design)
exp003.canonical_note                          See REPRODUCIBILITY.md section 1.3
```

### Experiment 004 - hypermassive-multiphysics-collider-v3-deterministic

```
exp004.main_run_master_root                    5dfed1e8093dabae26baa87bd0c30c3f19c0eed414759cbb7d8f3db70eae7012
exp004.determinism_common_hash                 cc49aea5d2e0062352e527aa54ec6c2c8a64f3738185d881762b21b3af38756d
exp004.stream.nuclei                           fc2f63a140e3606ca620ba446938821975fec4c3d935ff4e13fe0e6f8e92c641
exp004.stream.spatial                          531f183385845312a63d4c348326ac229768cbfda9720c7e7eacf442a39ba58e
exp004.stream.quantum                          1d91307fa9c571ff2469a7fd393fee2ca2e5aae1c20dc37cde71a18748b1bf8d
exp004.stream.gravity                          ef34e72d79adba580f3e3e0045659c15f1447ee7f599b1d8d5426ef671eb1eb4
exp004.stream.quadrupole_GW                    6e8adb59a731342b91ccdfdb9eb191f0b3bb05d81fb401e672516f078dc7eb18
exp004.stream.event_horizons                   8a34751c476a16389b524d7e0b7d2999984141d2ac067e0b55bdaf21e3da0594
```

### Experiment 005 - multiverse-collider-v4

```
exp005.multiverse_master_root                  252ba3c4b3ac93b0afeccc65bf74c9865327d95e74bd77232ada1167be40fae2
exp005.determinism_common_hash                 2dc033872a18d277b0b86d9243392815f15ee9aeb914958691cc9ac51c6803dd
exp005.universe.chain_mbw_v0                   1c2982432a5acb44d4e6cdf349aa80ccd8f23ef6da4b8765ac5ea30a1b0ba960
exp005.universe.pocc_anchor                    72cee9d0b038aff1496180c5d13362d8b82af2c7d49462b235bab326464e651c
exp005.universe.kat6_prefix                    3014d92dba094caba092c1aad8448595d18ee3894dadbad1136206053f3ce6f2
exp005.universe.kat10_xmss_root                55da9144cacf591ff12b90eae7f600af4aa75bf79e687b88225d7b7fc6897217
```

### Experiment 006 - maximum-chaos-generator-v0

```
exp006.multiverse_state_hash                   24655fcaed3aab576fdb2dee9e752b43671e77b83e4de87071dd4714528b967c
exp006.universe.chain_mbw_v0                   39b0011db695396aec7bebbbb62f1126a9581a2f605a35977cef3db0b4249df3
exp006.universe.pocc_anchor                    31a81875d01422b382550fa782fd65dd3730e55c60c62996a8b42ab455869b45
exp006.universe.kat6_prefix                    be3ffd55e6d13946c6fc285a27ec15de3a8148881816ba1fae99848a71685779
exp006.universe.kat10_xmss_root                c7cdcf23c8111683cab611d7030da78af37b9df4dea33846d9f0747ad1cfb925
exp006.universe.kat1_prefix                    6e6e264feefd5617851e201cc200da022cefb6f3b0ace7b54816209da978dbec
exp006.universe.anchor_state                   05620e8fe52bc37baea12e260d893c64f3133440f64b7d3da074d167cefd1ba9
```

---

## Source PopChain anchors used as seeds

For traceability, the canonical PopChain anchor hashes that serve as universe seeds in the experiments:

```
chain_mbw_v0     = 29 246 651 490           (alpha-testnet measured mass-and-work, decimal)
pocc_anchor      = 417 696                  (Proof-of-Computational-Capability anchor)
kat6_prefix      = 0xb2e04c806390bd6d       (first 8 bytes of KAT-6 hash:
                                             b2e04c806390bd6d60c80cb82178aa6032c4bd76b14d931d93e01e49c8005dad)
kat10_xmss_root  = 0x2935fde2b9d76e0b       (first 8 bytes of KAT-10 XMSS root:
                                             2935fde2b9d76e0b7a9c733cd518cc9df07cf282163cadc990c8587c7b903606)
kat1_prefix      = 0x39399ffd3dcdf17c       (first 8 bytes of KAT-1 hash:
                                             39399ffd3dcdf17c4a484002ebade955471f4656fa1d562b2820af29d2a13d22)
anchor_state     = 0x41d7ebf3e3c96685       (first 8 bytes of state_root_hex at experiment time:
                                             41d7ebf3e3c9668508dd070ca0a815a8299fe9fda63dbc569949c89b7e494dd5)
```

These seeds are themselves derivable from the PopChain alpha-testnet canonical state at the experiment timestamp (2026-05-10 to 2026-05-11). The state_root_hex was extracted from validator val-alpha block height 83 703.

---

## Hash format

All hashes are SHA-256, presented as lowercase hexadecimal strings of length 64. Verification:

```python
import hashlib
assert hashlib.sha256(canonical_bytes).hexdigest() == expected_hash
```

For Merkle-derived hashes, the construction algorithm is specified in `METHODOLOGY.md` section 4.

---

## Version control

This file is version 1.0, dated 2026-05-11, generated from the empirical runs documented in the envelope JSON files in the `results/` directory of this experiment publication.

Future revisions, if any, will be tagged with semantic version and accompanied by a changelog. Anchor hashes themselves are immutable; they will not be revised. Any future correction (e.g., to a documented parameter that was misstated) will be communicated via the changelog without modifying the underlying hash values.
