# Determinism Rule - Proposal for PCIP-0010 §6.4.1

This document specifies a normative amendment to PCIP-0010 (POP-2-COMPUTE Active Compute Profile) Section 6.4 (Determinism Requirements). The amendment introduces a new subsection §6.4.1 (Atomic Operation Discipline) whose text is provided in section 2 below. The amendment is supported by empirical evidence from the Cosmic Forge experiment series; the evidence is summarized in section 3.

This document is part of the public Cosmic Forge experiment publication package. The amendment will be folded into the canonical PCIP-0010 specification in a subsequent revision.

---

## 1. Background

PCIP-0010 §6.4 (Determinism Requirements) currently requires:

> Conformant POP-2-COMPUTE backend implementations MUST produce bit-identical proof artifacts for a given (workload spec, seed, hardware profile) triple, across re-runs on the same physical device.

This requirement is necessary for cryptographic verification of compute proofs but does not specify how to satisfy it at the kernel design level. Common patterns that violate this requirement when used naively include cross-particle accumulation, neighbor-list reductions, and global statistics aggregation.

The Cosmic Forge experiments empirically established the precise design rule whose violation is sufficient (and, in tested cases, only) to break determinism: floating-point atomic operations on shared GPU memory.

---

## 2. Amendment text - PCIP-0010 §6.4.1 (Atomic Operation Discipline)

Insert immediately after the existing §6.4 text:

### §6.4.1 Atomic Operation Discipline

**Normative requirement.** Conformant POP-2-COMPUTE backend implementations MUST NOT use atomic floating-point operations (`atomicAdd`, `atomicMin`, `atomicMax`, `atomicExch`, or equivalents in any backend) on `float32`, `float64`, or any other floating-point accumulator that participates in the proof's canonical output.

**Permitted alternative.** Conformant implementations MAY use atomic operations on integer types (`int32`, `uint32`, `int64`, `uint64`) without restriction. Integer atomic addition is associative and commutative bit-identically across permutations of operands and is therefore deterministic regardless of GPU warp scheduling order.

**Required pattern for floating-point accumulation.** When the workload semantically requires accumulation of a floating-point quantity, the implementation MUST follow this pattern:

1. Define a scaling constant `S` of integer type that yields the desired numerical precision when applied to the float value.
2. Convert each contribution to an integer: `contrib_int = (int64) round(contrib_float * S)`.
3. Accumulate via integer atomic: `atomicAdd(accumulator_int, contrib_int)` where `accumulator_int` is `int64` or `uint64`.
4. In a separate finalization step, after all atomic accumulations have completed, recover the float value: `accumulator_float = (float) accumulator_int / S`.
5. The finalization step MUST use exactly one thread per accumulator location (i.e., no further atomics). Alternatively, the finalization may be performed on host CPU after device-to-host transfer.

**Scaling factor selection.** Implementations SHOULD document scaling factors in machine-readable form within the proof workload specification. Implementations MUST ensure scaled values do not overflow the integer type during accumulation. For typical workloads with N particles up to 10⁸, mass values up to 10³, position values bounded by 1.0, recommended minimums are:

- Mass scale: `1 000` (precision ~10⁻³)
- Position × mass scale: `1 000 000` (precision ~10⁻⁶)
- Quadrupole tensor scale: `1 000 000` (precision ~10⁻⁶)
- Energy scale: `1 000 000` (precision ~10⁻⁶)

**Precision loss bound.** The maximum precision loss introduced by a scaling factor `S` is `1/S` per contribution. For accumulation of `N` contributions, worst-case accumulated error is `N/S`. Implementations MUST select `S` such that worst-case error does not affect the canonical proof output. For SHA-256 hashing of int64 accumulator state, the hash itself bit-identically reflects the integer state, so precision loss has no effect on canonical output; the precision concern applies only to physical interpretation of recovered float values.

**Verification.** A compliant backend implementation MUST pass the determinism stress test specified in §6.5: running the same workload with the same seed three times yields three bit-identical proof artifacts.

**Non-normative note.** The empirical basis for this requirement is documented in the Cosmic Forge experiment series (Experiments 003 and 004), summarized in section 3 below. Implementers are encouraged to consult that documentation when designing kernels.

---

## 3. Empirical basis

### 3.1 Failing case: Experiment 003

Experiment 003 (`hypermassive-multiphysics-collider-v0`) used `atomicAdd` on `float32` accumulators for cell mass, cell center-of-mass, and quadrupole tensor components. Running with identical seed three times produced three distinct envelope canonical hashes:

```
Run 1 multiverse master root: 10b789309358be5d (truncated)
Run 2 multiverse master root: 5acdcd17be8cb0cb (truncated)
Run 3 multiverse master root: 0ff1a0954bf9a80c (truncated)
```

Investigation traced the divergence to non-deterministic ordering of float additions within CUDA warps. Since `(a + b) + c ≠ a + (b + c)` for floating-point arithmetic in general (lost precision depends on operand magnitudes and order), different scheduling orders produce different bit patterns, which propagate to all downstream hashes.

### 3.2 Passing case: Experiment 004

Experiment 004 (`hypermassive-multiphysics-collider-v3-deterministic`) replaced every `atomicAdd(float)` with `atomicAdd(int64)` using fixed-point scaling, following exactly the pattern specified in section 2 above. Mass, center-of-mass, and quadrupole accumulators all became `int64` with scaling factors 1 000 and 1 000 000. The finalization step (one thread per cell) converted to float for downstream gravity kernel input.

Running with identical seed three times produced three bit-identical envelope canonical hashes:

```
Run 1 master root: cc49aea5d2e0062352e527aa54ec6c2c8a64f3738185d881762b21b3af38756d
Run 2 master root: cc49aea5d2e0062352e527aa54ec6c2c8a64f3738185d881762b21b3af38756d
Run 3 master root: cc49aea5d2e0062352e527aa54ec6c2c8a64f3738185d881762b21b3af38756d
```

The only design change between 003 and 004 was replacement of float atomics with int atomics. All other physics, all other kernel logic, all other parameter values were preserved. The result establishes that the integer atomic discipline is both necessary and sufficient for deterministic GPU compute proofs in the tested architecture (CUDA 12.9, NVIDIA RTX 3060, CuPy 14.0.1).

### 3.3 Generalization confirmed at larger scale

Experiment 005 (`multiverse-collider-v4`) extended the deterministic design to four parallel universes with 12 physics streams per universe and 15 distinct CUDA kernels. The same integer atomic discipline was applied throughout. Running with identical seeds three times again produced three bit-identical envelope canonical hashes:

```
Run 1 multiverse master: 2dc033872a18d277b0b86d9243392815f15ee9aeb914958691cc9ac51c6803dd
Run 2 multiverse master: 2dc033872a18d277b0b86d9243392815f15ee9aeb914958691cc9ac51c6803dd
Run 3 multiverse master: 2dc033872a18d277b0b86d9243392815f15ee9aeb914958691cc9ac51c6803dd
```

The discipline scales: 48 distinct deterministic processes (4 universes × 12 streams) composing to a single bit-identical multiverse hash.

---

## 4. Implementation guidance

### 4.1 Identifying float atomics in existing code

Implementers porting existing GPU compute kernels to the POP-2-COMPUTE canonical form should audit for the following patterns:

- Direct `atomicAdd(float*, float)` calls.
- Cooperative reductions that internally use float atomic operations.
- Library functions (CUB, Thrust, Kokkos, etc.) that may use float atomics under the hood.
- Operations on `__half` (FP16) or `bfloat16` shared-memory accumulators.
- Reductions across thread blocks using float-typed semaphores or counters.

Each occurrence must be replaced or the workload restructured.

### 4.2 Common patterns and their integer-atomic equivalents

**Cell mass accumulation:**
```
// FORBIDDEN
atomicAdd(&cell_mass_float[cell_idx], particle_mass);

// REQUIRED
long long contrib = (long long)(particle_mass * MASS_SCALE);
atomicAdd((unsigned long long*)&cell_mass_int[cell_idx], (unsigned long long)contrib);
```

**Center-of-mass accumulation (weighted average):**
```
// FORBIDDEN
atomicAdd(&com_x_float[cell_idx], px * pmass);
atomicAdd(&mass_total_float[cell_idx], pmass);

// REQUIRED
long long cx_contrib = (long long)((double)px * (double)pmass * (double)COM_SCALE);
long long m_contrib  = (long long)((double)pmass * (double)MASS_SCALE);
atomicAdd((unsigned long long*)&com_x_int[cell_idx], (unsigned long long)cx_contrib);
atomicAdd((unsigned long long*)&mass_total_int[cell_idx], (unsigned long long)m_contrib);

// finalization (one thread per cell):
double mf  = (double)mass_total_int[cell_idx] / (double)MASS_SCALE;
double cmx = (double)com_x_int[cell_idx] / (double)COM_SCALE / mf;
com_x_float_output[cell_idx] = (float)cmx;
```

**Global tensor reduction (quadrupole):**
```
// FORBIDDEN
atomicAdd(&qxx_float, m * x * x);

// REQUIRED
long long qxx_contrib = (long long)((double)m * (double)x * (double)x * (double)QUAD_SCALE);
atomicAdd((unsigned long long*)&qxx_int, (unsigned long long)qxx_contrib);
```

### 4.3 Performance considerations

Integer atomic operations on modern NVIDIA hardware (Ampere generation and later, including RTX 30/40 series) are highly optimized. The performance penalty of replacing `atomicAdd(float)` with `atomicAdd(int64)` is empirically small. In the Cosmic Forge experiments, throughput went from 157.6M particle-steps/sec (Experiment 003, float atomics) to 137.8M particle-steps/sec (Experiment 004, int atomics) - a 13 % reduction at the cost of full determinism. This reduction is acceptable given the cryptographic necessity of bit-identical output.

### 4.4 Backend portability

The integer atomic discipline is implementable on all major GPU compute backends:

- CUDA C / C++: `atomicAdd` is well-specified on `int`, `unsigned int`, `unsigned long long`, with hardware support since Kepler.
- cudarc (Rust): exposes `atomicAdd` on integer types via raw CUDA bindings.
- OpenCL: `atom_add` on `int`/`long` types specified in OpenCL 1.0+.
- ROCm/HIP: `atomicAdd` on integer types fully supported on Radeon Instinct and consumer Radeon devices.
- Vulkan Compute: `imageAtomicAdd` and buffer-backed atomic operations on integer types since SPIR-V 1.0.

This means a compliant POP-2-COMPUTE backend can be written for any of these stacks without violating the determinism rule.

---

## 5. Adoption path

This proposed amendment is published as part of the Cosmic Forge experiment publication, in advance of formal incorporation into PCIP-0010. The adoption path is:

1. **Public review period** of this document. Comments may be submitted via the `popchainnetwork/popchain` repository issue tracker.
2. **Revision of PCIP-0010** incorporating §6.4.1 with text substantially as specified in section 2 above. The revision will be assigned a fresh sha256 anchor in the PCIP series, recorded in the PopChain canonical PCIP index.
3. **Implementation in canonical POP-2-COMPUTE backend** (planned Rust + cudarc crate, `popchain-gpu`). The implementation will conform to §6.4.1.
4. **Inclusion in PCIP-0011 validator admission tests:** any T2-aspirant validator must demonstrate compute proof determinism via the §6.5 stress test, which implicitly verifies §6.4.1 compliance.

---

## 6. Compatibility notes

This amendment does not invalidate existing PopChain alpha-testnet proofs. The alpha-testnet does not require bit-identical compute proofs; PoCC anchor and validator tier registry both use chain-state hashing, not GPU compute output. The amendment applies prospectively to POP-2-COMPUTE workloads admitted at beta or mainnet.

Backends that currently use float atomics will need to be revised before being deployed as canonical POP-2-COMPUTE proof generators. The revision is local (kernel-level) and does not affect the workload specification at the protocol layer.
