# Methodology - Cosmic Forge Experiments

This document describes how the experiments were conducted scientifically, with sufficient specification for third parties to implement their own compute kernels and reproduce the observable results. The actual experiment scripts are not published; the methodology specification below is the public specification.

This follows the same pattern as protocol implementations such as Bitcoin Core or Ethereum clients: the specification is public; multiple implementations may exist; canonical correctness is defined by anchor hashes (see `REPRODUCIBILITY.md`).

---

## 1. Experimental design

### 1.1 Common framework

All six experiments share the following framework:

```
For each experiment:
  1. Initialize particle state from a deterministic seed.
  2. Loop for N steps:
     a. For each physics stream, apply per-particle update.
     b. At configurable snapshot intervals, hash the canonical state.
  3. Reduce per-snapshot hashes via Merkle tree to single root.
  4. Repeat with same seed; verify identical root (determinism check).
  5. Repeat with different seeds; verify distinct roots (cross-seed sanity).
```

### 1.2 Particle state

Each particle carries the following attributes (per experiment, expanding over the series):

- `A`: mass number (int32, range varies by experiment)
- `N`: neutron number (int32)
- `zone`: thermal zone index (int32, 0=hot, 1=mid, 2=cool, 3=ejecta)

Experiments 003+ additionally:
- `x, y, z`: position in 3D toroidal space (float32, range `[-1, 1]`)
- `vx, vy, vz`: velocity (float32)
- `psi_real, psi_imag`: complex quantum amplitude (float32, |psi|=1 invariant)

Experiments 005+ additionally:
- `nu_e, nu_mu, nu_tau`: neutrino flavor amplitudes (float32, normalized)

Experiments 005+ separate populations:
- Visible matter: as above.
- Dark matter: position, velocity, mass; gravity-only interaction.

### 1.3 Spatial grid

Experiments 003+ partition space into a `GRID_N³` grid of cells (default `GRID_N = 32`, giving 32 768 cells). Cells accumulate density and mass via integer atomic operations (see section 2.3).

---

## 2. Physics streams

Each stream is a kernel implementing one physical phenomenon. Streams compose by sharing read access to particle state and writing to disjoint or atomically-synchronized accumulators.

### 2.1 r-process nucleosynthesis

Per particle per step:

1. Read random number array `rb` (six values per particle).
2. Determine zone-specific reaction probabilities `(pc, pb, pph, pm)` for capture, beta decay, photo-disintegration, and zone migration respectively.
3. If neutron number is at a magic value `{50, 82, 126}`, multiply `pb` by `magic_bonus = 0.3 to 0.5`.
4. If mass number exceeds `FISSION_THRESHOLD = 230` to `240`, and `rb[4] < p_fission ≈ 0.15 to 0.20`, perform fission: `A → A/2 + delta`, `N → N/2`, where `delta = (int)(rb[5] * 20) - 10`. Then exit.
5. Otherwise: with probability `pc`, capture neutron (`A++, N++`); with probability `pb`, beta decay (`N--`); with probability `pph`, photo-disintegrate (`A--, N--`); with probability `pm`, migrate to next zone.
6. Clamp `A` to `[A_MIN=56, A_MAX=280 or 300]`, `N` to `[1, A]`.

Zone probability arrays (typical values, see envelope for exact parameters per experiment):

```
P_CAPTURE  = [0.45, 0.40, 0.20, 0.05]   # higher in hot zone
P_BETA     = [0.02, 0.10, 0.30, 0.40]   # higher in ejecta
P_PHOTODIS = [0.25, 0.05, 0.00, 0.00]   # only in hot zones
P_MIGRATE  = [0.02, 0.03, 0.05, 0.001]  # zone-to-zone transit
```

### 2.2 N-body gravity (grid-sampled)

Per particle per step:

1. Determine current grid cell from position.
2. Sum gravitational force from the 27 neighboring cells (3×3×3 stencil including own cell), treating each cell as a point mass at its center of mass.
3. Force law: `F = G * m_cell * m_particle / (r² + epsilon)` with `epsilon = 0.001` for numerical softening; `G = 1e-5` to `3e-5`.
4. Apply force as velocity update: `v += F/m * dt`.
5. Clamp velocity magnitude to ≤ 0.5 or 0.6 (toy CFL stability).
6. Update position with toroidal wraparound at space boundaries `[-1, 1]`.

### 2.3 Cell aggregation (integer atomics)

This is the most subtle part for determinism. Per particle per step:

1. Determine grid cell from position.
2. Compute scaled integer contributions:
   - `mass_int = A * MASS_SCALE` where `MASS_SCALE = 1000`
   - `com_x_int = (int64)(x * A * COM_SCALE)` where `COM_SCALE = 1_000_000`
   - Similarly for `com_y_int`, `com_z_int`.
3. Use `atomicAdd` on `int64` (or `unsigned long long`) accumulators:
   - `cell_mass_int[cell]`
   - `cell_com_x_int[cell]`, `cell_com_y_int[cell]`, `cell_com_z_int[cell]`
   - `cell_count[cell]` (int32 atomic)

After all particles processed, a finalization kernel converts integer accumulators back to float-valued centers of mass and masses for downstream use by gravity kernel. The conversion is one thread per cell (no atomics in finalization).

**This integer-only atomic discipline is the key design rule.** See section 5 below.

### 2.4 Beta-delayed neutron emission

Per particle per step:

```
if A > 180 and N > A/2 + 5 and rb < P_BETA_DELAYED_N:
    N -= 1
    A -= 1
    clamp(A >= 56, N >= 1)
```

`P_BETA_DELAYED_N` is typically 0.08 to 0.12.

### 2.5 Alpha decay cascade

Per particle per step:

```
if A > 200 and rb < P_ALPHA_DECAY:
    A -= 4
    N -= 2
    clamp(A >= 56, N >= 1)
```

`P_ALPHA_DECAY` is typically 0.03 to 0.05.

### 2.6 Quantum phase coherence (toy Schrödinger evolution)

Per particle per step:

1. Compute local energy `E = A / 100`.
2. Rotate `psi = (psi_real + i * psi_imag)` by phase `exp(-i * E * dt)`.
3. Multiply by zone-dependent decoherence factor (0.95 in hot zone, 0.99 in mid, 0.999 in cool/ejecta).
4. Renormalize to unit modulus (preserves `|psi| = 1`).

### 2.7 Gravitational wave quadrupole moment

Per particle, contribute six tensor components to global accumulator via `atomicAdd` on `int64`:

```
qxx += A * x * x * QUAD_SCALE
qyy += A * y * y * QUAD_SCALE
qzz += A * z * z * QUAD_SCALE
qxy += A * x * y * QUAD_SCALE
qxz += A * x * z * QUAD_SCALE
qyz += A * y * z * QUAD_SCALE
```

`QUAD_SCALE = 1_000_000`. Sequence of quadrupole tensors across snapshots forms its own Merkle channel.

### 2.8 Neutrino flavor oscillations (Experiments 005+)

Per particle per step, apply three two-flavor rotations using the PMNS mixing angles:

```
θ_12 = 0.5836  (solar)
θ_23 = π/4     (atmospheric, maximal mixing)
θ_13 = 0.1473  (reactor)

ν_e, ν_μ <- rotate(ν_e, ν_μ, θ_12 * dt)
ν_μ, ν_τ <- rotate(ν_μ, ν_τ, θ_23 * dt)
ν_e, ν_τ <- rotate(ν_e, ν_τ, θ_13 * dt)

If in hot zone (zone == 0) and rb < P_MSW_FLIP:
    swap(ν_e, ν_τ)

Renormalize: |ν| = 1
```

### 2.9 Magnetohydrodynamics (Experiments 005+)

A magnetic field `B = (Bx, By, Bz)` is stored per cell, initialized as random with scale `B_INIT_SCALE`. Two kernels:

**Lorentz force on particles:**

```
q = A / 2
F_x = q * (vy * Bz - vz * By)
F_y = q * (vz * Bx - vx * Bz)
F_z = q * (vx * By - vy * Bx)
v += F * dt
clamp |v| <= 0.5 or 0.6
```

**B-field evolution per cell:**

```
With probability P_RECONNECTION ≈ 0.02 to 0.05:
    Flip sign of one randomly chosen component of B.
Apply slight damping: B *= 0.999 (or 0.9995 for stronger persistence).
```

### 2.10 Dark matter coupling (Experiments 005+)

A separate population of "dark" particles (10–15 % of visible count). They have only position, velocity, mass; they update only via gravity from the shared `cell_mass`/`cell_com` arrays. Dark matter particles are hashed as their own stream.

### 2.11 Photon transport (Experiments 005+)

When a particle satisfies emission criteria (e.g., neutron excess), it deposits photons in its current cell. Per-cell photon count and per-cell total photon energy are maintained as int64 accumulators (atomically updated).

### 2.12 GR time dilation (Experiments 005+)

Per cell, compute toy weak-field proper time factor:

```
factor = 1 - G_TOY * cell_mass / r²_cell
clamp factor to [0.1, 1.0]
```

### 2.13 Energy-momentum aggregation (Experiments 005+)

Per particle, contribute to global four-vector (`E, px, py, pz`) via `atomicAdd` on `int64` with `ENERGY_SCALE = 1_000_000`. The four-vector evolution across snapshots is a hashable conservation diagnostic.

---

## 3. Multi-universe composition (Experiments 005, 006)

Parallel universes are independent simulation instances with distinct seeds. They are coupled by **mixing events**:

```
Every MIXING_EVERY steps (typically 50 to 100):
    Generate N_swap = (n_particles * MIXING_FRACTION) random indices
    from a master RNG seeded by sum of all universe seeds (deterministic).
    For each universe i:
        Swap particles at the chosen indices with universe (i+1) mod N.
```

`MIXING_FRACTION` typically `0.001` to `0.005`. This is sufficient to couple universes statistically without erasing initial-seed identity.

Canonical universe seeds (from PopChain anchors):

```
chain_mbw_v0     = 29 246 651 490   (alpha-testnet measured mass-and-work)
pocc_anchor      = 417 696          (Proof-of-Computational-Capability anchor)
kat6_prefix      = 0xb2e04c806390bd6d   (KAT-6 hash prefix)
kat10_xmss_root  = 0x2935fde2b9d76e0b   (KAT-10 XMSS root prefix)
kat1_prefix      = 0x39399ffd3dcdf17c   (KAT-1 hash prefix)
anchor_state     = 0x41d7ebf3e3c96685   (state_root_hex prefix)
```

---

## 4. Hashing and Merkle composition

### 4.1 Per-stream snapshot hash

At each snapshot interval, each physics stream produces a hash from the canonical byte representation of its state arrays:

```
hash_stream = SHA-256(state_byte_concatenation)
```

The canonical byte representation is the little-endian binary representation of typed arrays (int32 for A/N/zone, float32 for positions/velocities/phases, int64 for atomic accumulators). The byte order is deterministic and platform-independent on little-endian architectures (x86_64 and ARM64 both).

### 4.2 Per-stream Merkle root

For each stream, the sequence of snapshot hashes is reduced to a Merkle root using standard binary Merkle construction:

```
Inputs: list of SHA-256 hashes h_1, h_2, ..., h_K
Pad to power of 2 by repeating last element (only if needed).
Pairwise concatenate and SHA-256 until single root.
```

Six (Experiments 003-004) or twelve (Experiments 005-006) stream roots result.

### 4.3 Universe Merkle root

For each universe, the per-stream Merkle roots are concatenated in canonical order (see `REPRODUCIBILITY.md`) and Merkle-reduced to a single universe root.

### 4.4 Multiverse Merkle root

For multi-universe experiments, universe roots are Merkle-reduced in canonical seed order (the order listed in section 3) to a single multiverse root.

### 4.5 Envelope canonical hash

The complete experiment envelope (JSON object with all metadata, parameters, and hash results) is canonicalized via:

```
canonical_json = json.dumps(envelope, sort_keys=True, separators=(",", ":"))
envelope_canon_hash = SHA-256(canonical_json.encode())
```

This is the single 32-byte fingerprint of the entire experiment.

---

## 5. The determinism design rule

The single decisive rule (empirically established in Experiments 003 vs 004) is documented in detail in `DETERMINISM-RULE.md`. Stated briefly here:

```
Compute proof kernels MUST NOT use atomicAdd or any other atomic
floating-point reduction operation.

Compute proof kernels MAY use atomicAdd on integer types.

For floating-point accumulation, kernels MUST scale values to integers
via documented fixed-point multipliers, perform the accumulation in
integer arithmetic, and convert back to float in a deterministic
one-thread-per-cell finalization pass.
```

This rule must be followed by any backend implementation seeking to reproduce the canonical anchor hashes in `REPRODUCIBILITY.md`.

---

## 6. Determinism verification protocol

Every experiment must run the **determinism stress test**:

```
1. Run experiment with given seed; record envelope canonical hash.
2. Re-run experiment with identical seed; record envelope canonical hash.
3. Repeat at least 3 times.
4. All hashes must be bit-identical.
```

The protocol fails if any two hashes differ. Investigation of the cause is then required (see Finding 1.2 in `EMPIRICAL-FINDINGS.md` for an example).

---

## 7. Hardware and software environment

The experiments were conducted on:

```
Hardware:
  CPU:    AMD Ryzen (B450M motherboard)
  GPU:    NVIDIA GeForce RTX 3060, 12 GB GDDR6 VRAM (LHR variant)
  RAM:    sufficient for Python overhead (under 1 GB used)

Software:
  OS:                 Ubuntu 24
  GPU driver:         NVIDIA 580.142
  CUDA runtime:       12.9
  CuPy:               14.0.1
  Python:             3.12
```

Third-party implementations may use any backend (CUDA C, cudarc, OpenCL, ROCm/HIP, Vulkan Compute, native Rust, native C++) provided the determinism rule (section 5) is observed. The PopChain canonical implementation will be a Rust crate using cudarc, planned for future release per `PCIP-0020`.

---

## 8. Out of scope

The methodology specified above does **not** include:

- Choice of CUDA block/thread launch configurations (left to backend; does not affect output given the determinism rule).
- Optimization techniques (memory coalescing, shared memory tiling, etc.).
- Multi-GPU distribution. The canonical compute proof is defined per single GPU.
- Random number generator choice. The experiments used CuPy's default (likely PCG64); third-party implementations may use any RNG provided seed-determinism is preserved.

These are implementation details. The canonical output is defined by the anchor hashes listed in `REPRODUCIBILITY.md`, not by the choice of any particular implementation detail.

---

## 9. Reference to PopChain protocol

Methodology choices (integer atomic discipline, Merkle stream composition, multi-universe parallelism) are designed to inform:

- **PCIP-0010** (POP-2-COMPUTE Active Compute Profile): adoption of integer atomic rule as §6.4.1.
- **PCIP-0011** (Validator Tier Registry): T2 admission throughput threshold validation; per-stream tier hierarchy.
- **PCIP-0020** (Language Discipline): canonical Rust implementation planned.

These are the protocol vehicles into which the empirical findings will be folded.
