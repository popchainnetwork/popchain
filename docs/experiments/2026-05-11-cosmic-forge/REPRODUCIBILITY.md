# Reproducibility - Cosmic Forge Experiments

This document specifies how a third-party implementation can reproduce the canonical results of the Cosmic Forge experiment series. It enumerates the canonical anchor hashes that any compliant implementation must produce, the input parameters that determine each canonical run, and the verification procedure.

The actual experiment scripts are not published. Reproducibility is established by specification (`METHODOLOGY.md`) and anchor verification (this document).

---

## 1. Canonical anchor hashes

The following hashes are the canonical expected outputs of each experiment when run with the specified parameters. A third-party implementation following `METHODOLOGY.md` and `DETERMINISM-RULE.md` is expected to produce these exact hashes on a single GPU with consistent floating-point handling.

### 1.1 Experiment 001 - r-process-toy v0

```
Parameters:
  n_particles:        10 000
  n_steps:            1 000
  snapshot_every:     100
  seed:               29 246 651 490 (chain_mbw_v0)
  A_min, A_max:       56, 280
  fission_threshold:  240
  magic_bonus:        0.5
  p_fission:          0.15
  P_CAPTURE:          [0.45, 0.40, 0.20, 0.05]
  P_BETA:             [0.02, 0.10, 0.30, 0.40]
  P_PHOTODIS:         [0.25, 0.05, 0.00, 0.00]
  P_MIGRATE:          [0.02, 0.03, 0.05, 0.001]

Canonical output:
  final_state_hash:   7990495ca63b098b1622be841307f1d44acffb7b548e84832a3754defb19a031
```

### 1.2 Experiment 002 - r-process v1 MEGA

```
Parameters:
  n_particles:        1 000 000
  n_steps:            10 000
  snapshot_every:     100
  seed:               29 246 651 490
  (other parameters: same as Experiment 001)

Canonical outputs:
  main_run_final_hash:         964675b8799786e1f7a44c5a0193d09768e520c42d7c8fb2088792baef0efcf9
  determinism_common_hash:     44db2a94694552918872e56169bbe30efc1e9305cf6ba12d77506d71273d820c
                               (smaller run for 5-fold determinism check)

Cross-seed sanity (should yield distinct hashes):
  seed 29 246 651 490:         44db2a94694552918872e56169bbe30efc1e9305cf6ba12d77506d71273d820c
  seed 417 696:                ea51aef714c0310a8ebec1f7098dd9c85b226c6e4eff403068a83f075775fa5f
  seed 0xb2e04c806390bd6d:     4b128bbd71749853b1f7a931db242e12a1f323151fab9fa1ec963e30bca2afac
```

### 1.3 Experiment 003 - non-deterministic baseline (float atomics, expected to FAIL)

```
Parameters:
  n_particles:        10 000 000
  n_steps:            1 000
  snapshot_every:     50
  seed:               29 246 651 490
  physics_streams:    6 (r-process, gravity, beta-delayed, alpha decay,
                        quantum coherence, event horizon, gravitational wave)
  atomic_discipline:  FLOAT atomicAdd (intentional violation of §6.4.1)

Expected behavior:
  Three determinism stress runs MUST yield three DISTINCT envelope hashes.
  This experiment is included as a falsification anchor: any implementation
  reporting three identical hashes for this configuration is not faithfully
  reproducing the float-atomic non-determinism of CUDA hardware.

Reference outputs (illustrative, will vary per implementation):
  Run 1: 10b789309358be5d... (first 16 hex chars only - distinct per run)
```

### 1.4 Experiment 004 - deterministic fix (int atomics)

```
Parameters:
  n_particles:        10 000 000
  n_steps:            1 000
  snapshot_every:     50
  seed:               29 246 651 490
  physics_streams:    6 (same as Experiment 003)
  atomic_discipline:  INT64 atomicAdd with fixed-point scaling per §6.4.1

  Scaling constants:
    MASS_SCALE:       1 000
    COM_SCALE:        1 000 000
    QUAD_SCALE:       1 000 000

Canonical outputs:
  main_run_master_root:        5dfed1e8093dabae26baa87bd0c30c3f19c0eed414759cbb7d8f3db70eae7012
  determinism_common_hash:     cc49aea5d2e0062352e527aa54ec6c2c8a64f3738185d881762b21b3af38756d
                               (smaller run for 3-fold determinism check:
                                n_particles=1 000 000, n_steps=200)

  Per-stream Merkle roots of main run:
    nuclei:           fc2f63a140e3606ca620ba446938821975fec4c3d935ff4e13fe0e6f8e92c641
    spatial:          531f183385845312a63d4c348326ac229768cbfda9720c7e7eacf442a39ba58e
    quantum:          1d91307fa9c571ff2469a7fd393fee2ca2e5aae1c20dc37cde71a18748b1bf8d
    gravity:          ef34e72d79adba580f3e3e0045659c15f1447ee7f599b1d8d5426ef671eb1eb4
    quadrupole_GW:    6e8adb59a731342b91ccdfdb9eb191f0b3bb05d81fb401e672516f078dc7eb18
    event_horizons:   8a34751c476a16389b524d7e0b7d2999984141d2ac067e0b55bdaf21e3da0594
```

### 1.5 Experiment 005 - multiverse collider v4

```
Parameters:
  n_particles_per_universe:    2 500 000
  n_dm_per_universe:           250 000
  n_universes:                 4
  universe_seeds (ordered):
    chain_mbw_v0:     29 246 651 490
    pocc_anchor:      417 696
    kat6_prefix:      0xb2e04c806390bd6d
    kat10_xmss_root:  0x2935fde2b9d76e0b
  n_steps:            500
  snapshot_every:     25
  mixing_every:       100
  mixing_fraction:    0.001
  master_mix_seed:    sum of universe_seeds, masked to 32 bits
  physics_streams:    12 per universe (see METHODOLOGY.md §2)
  atomic_discipline:  INT64 throughout

Canonical outputs:
  main_run_multiverse_master:  252ba3c4b3ac93b0afeccc65bf74c9865327d95e74bd77232ada1167be40fae2
  determinism_common_hash:     2dc033872a18d277b0b86d9243392815f15ee9aeb914958691cc9ac51c6803dd
                               (smaller run: n_particles=500 000, n_steps=100)

  Per-universe Merkle roots (main run, ordered as universe_seeds above):
    chain_mbw_v0:     1c2982432a5acb44d4e6cdf349aa80ccd8f23ef6da4b8765ac5ea30a1b0ba960
    pocc_anchor:      72cee9d0b038aff1496180c5d13362d8b82af2c7d49462b235bab326464e651c
    kat6_prefix:      3014d92dba094caba092c1aad8448595d18ee3894dadbad1136206053f3ce6f2
    kat10_xmss_root:  55da9144cacf591ff12b90eae7f600af4aa75bf79e687b88225d7b7fc6897217

Construction:
  universe_root = Merkle(stream_root_1, ..., stream_root_12)
  multiverse_master = Merkle(universe_root_chain_mbw_v0, universe_root_pocc_anchor,
                              universe_root_kat6, universe_root_kat10)
```

### 1.6 Experiment 006 - maximum chaos generator

```
Parameters:
  n_particles_per_universe:    2 500 000
  n_dm_per_universe:           375 000  (DM_FRACTION = 0.15)
  n_universes:                 6
  universe_seeds (ordered):
    chain_mbw_v0:     29 246 651 490
    pocc_anchor:      417 696
    kat6_prefix:      0xb2e04c806390bd6d
    kat10_xmss_root:  0x2935fde2b9d76e0b
    kat1_prefix:      0x39399ffd3dcdf17c
    anchor_state:     0x41d7ebf3e3c96685
  n_steps:            500
  mixing_every:       50
  mixing_fraction:    0.005
  chaos_amplifiers:
    P_FEEDBACK:       0.10
    P_RESONANCE_NOISE:0.02
    P_SOC_AVALANCHE:  0.15
    fission_threshold:230
    G_TOY:            3e-5 (3x stronger gravity)
    B_INIT_SCALE:     0.05 (5x stronger B field)

Canonical outputs:
  multiverse_state_hash:       24655fcaed3aab576fdb2dee9e752b43671e77b83e4de87071dd4714528b967c

  Per-universe state hashes (final A histogram + final cell count + final energy):
    chain_mbw_v0:     39b0011db695396aec7bebbbb62f1126a9581a2f605a35977cef3db0b4249df3
    pocc_anchor:      31a81875d01422b382550fa782fd65dd3730e55c60c62996a8b42ab455869b45
    kat6_prefix:      be3ffd55e6d13946c6fc285a27ec15de3a8148881816ba1fae99848a71685779
    kat10_xmss_root:  c7cdcf23c8111683cab611d7030da78af37b9df4dea33846d9f0747ad1cfb925
    kat1_prefix:      6e6e264feefd5617851e201cc200da022cefb6f3b0ace7b54816209da978dbec
    anchor_state:     05620e8fe52bc37baea12e260d893c64f3133440f64b7d3da074d167cefd1ba9

Expected emergent statistics (toleranced):
  Power-law alpha (A distribution):   2.05 ± 0.10
  Cluster size power-law R²:          > 0.95
  Fractal dimension (box counting):   2.66 ± 0.01
  Shannon entropy A (final):          5.94 ± 0.01 bits
  Cross-universe KL divergence:       < 0.005 bits (all pairs)
  Energy drift:                       +51 ± 1 % from initial

Note: Experiment 006 was empirically observed to fail strict bit-identical
determinism between runs, due to subtle float-precision drift in the
detector statistics analysis layer (CPU-side numpy operations on float
quadrupole tensors). The chaos run physics itself remains GPU-deterministic;
the divergence appears in the post-processing analysis layer. Third-party
implementations may observe similar drift in detector outputs and should
focus reproducibility on the per-universe state hashes (which are derived
from int64 GPU state), not on the detector statistics.
```

---

## 2. Verification procedure for third parties

### 2.1 Step-by-step

1. Implement the kernels per `METHODOLOGY.md` sections 2 (physics streams) and the determinism discipline per `DETERMINISM-RULE.md` section 2.

2. Implement the per-stream snapshot hashing per `METHODOLOGY.md` section 4: canonical byte representation, SHA-256 per snapshot, Merkle reduction.

3. Implement the multi-universe composition per `METHODOLOGY.md` section 3, using the canonical seeds listed in this document.

4. Run each experiment in turn with the canonical parameters specified in section 1 above.

5. Compare your implementation's output hashes to the canonical hashes in section 1. Bit-identical match is the success criterion.

### 2.2 Partial verification

A third party may verify a single experiment (e.g., Experiment 004) without implementing all six. The single-experiment determinism check (running same seed three times, observing bit-identical output, matching the canonical hash) is sufficient evidence of a conforming implementation.

### 2.3 Tolerance for cross-implementation drift

The canonical hashes were generated on `NVIDIA RTX 3060` running `CUDA 12.9 / CuPy 14.0.1`. Third-party implementations on the same hardware family (Ampere generation NVIDIA GPUs) and the same arithmetic standard (IEEE 754 binary32, IEEE 754 binary64) using the same RNG algorithm (CuPy default, PCG64) should reproduce bit-identical hashes.

Implementations on different hardware families, different floating-point standards, or different RNG algorithms may produce different hashes for the same logical workload. The Cosmic Forge canonical hashes are not portable across hardware families. Cross-hardware portability would require a portable RNG specification and a portable arithmetic profile, both of which are outside the scope of this experiment series.

The PopChain canonical POP-2-COMPUTE profile (forthcoming in PCIP-0010 revision) will specify a hardware profile and RNG profile for canonical proof generation; until then, the Cosmic Forge anchor hashes serve as research-quality empirical references.

---

## 3. Hardware and software baseline

The canonical anchor hashes in section 1 were generated on the following baseline:

```
Host machine:        forged-solana-labs-B450M-HDV-R4-0
GPU:                 NVIDIA GeForce RTX 3060 (LHR), 12 GB GDDR6
CUDA runtime:        12090 (12.9)
CuPy version:        14.0.1
NVIDIA driver:       580.142
Python:              3.12
OS:                  Ubuntu 24
Architecture:        x86_64
Endianness:          little-endian
Float format:        IEEE 754 binary32 (float32)
Integer format:      two's complement little-endian int32 / int64
```

The integer atomic operations used (`atomicAdd` on `unsigned long long`) are specified by CUDA from Kepler architecture onward. The deterministic semantics of these operations are platform-stable across the entire Ampere generation (RTX 30 / A100 / etc.) and later, when the integer atomic discipline is followed.

---

## 4. Recommended verification sequence

A laboratory wishing to verify the Cosmic Forge results from scratch is recommended to follow this sequence:

1. **Verify Experiment 001** first. It uses only element-wise operations, no atomics. Bit-identical match should be achieved easily on any Ampere or later NVIDIA GPU.

2. **Verify Experiment 002** next. It uses custom CUDA C kernels but no atomics. Bit-identical match should be achieved.

3. **Reproduce Experiment 003 (failing case)** to confirm float atomic non-determinism. Three runs must produce three distinct hashes (the canonical hashes are unstable; what is canonical is the *failure*).

4. **Verify Experiment 004 (deterministic fix)** by following the integer atomic discipline. This is the key reproducibility test; bit-identical match confirms a conforming implementation.

5. **Verify Experiment 005 (multi-universe)** to confirm scaling.

6. **Verify Experiment 006 (chaos)** primarily for the per-universe state hashes; emergent statistics are reported with tolerances above.

---

## 5. Reporting verification results

Third parties verifying these results are encouraged to report findings via:

```
GitHub issue:  https://github.com/popchainnetwork/popchain/issues
Label:         cosmic-forge-verification
```

A successful verification report should include:

- Hardware specification (GPU model, driver version, CUDA runtime).
- Software stack (programming language, GPU compute library, RNG library and version).
- Implementation summary (which experiments verified, how kernels structured).
- The hashes your implementation produced for each verified experiment.
- Match status against canonical hashes.

Reports of mismatches are equally valuable. A mismatch with documented configuration helps identify the hardware/software boundary of canonical portability and informs the canonical POP-2-COMPUTE hardware profile specification.

---

## 6. License and citation

This reproducibility specification is part of the public Cosmic Forge experiment publication, released under Apache-2.0 license per the `popchain` public repository.

When citing the Cosmic Forge results in academic or technical work, please reference:

```
PopChain Foundation. Cosmic Forge Experiments: Empirical Investigation of
GPU Compute Proof Determinism and Emergent Multi-Physics Universality.
PopChain public documentation, 2026-05-11.
https://github.com/popchainnetwork/popchain/tree/main/docs/experiments/2026-05-11-cosmic-forge
```

Citations of specific anchor hashes should reference the experiment identifier and the field name from this document (e.g., "Cosmic Forge Experiment 004, main_run_master_root, value `5dfed1e8...`").
