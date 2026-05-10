#!/usr/bin/env python3
"""
PopChain Phase 0c.1 — On-Chain Attestation Verifier

Scans recent blocks of popchain-alpha-testnet for proof_submit_v0
transactions matching the SHA256 hashes of the Phase 0c.1 attestation
bundle. Reports MATCH / MISSING per file.

Usage:
    python3 tools/verify_attestations.py [--db-path PATH]

Default DB path: /home/uncrfactory/popchain-data/val-alpha/blocks/

Requires read access to a popchain validator's block storage. For
public verification, see the popchain.tech/explorer.html block lookup
or query the popchain-alpha-testnet RPC endpoint.

Deterministic output: same hashes on input → same output. No network
calls, no external dependencies beyond Python 3 stdlib.
"""

import json
import base64
import os
import sys
import argparse


# Phase 0c.1 attestation bundle SHA256 hashes (sorted by file name)
ATTESTATIONS = {
    "1f0d1df4b0613a616a17c4a1b07ca7c59879abd489b843253608e909a99dffa3": "01_gemini_md.md",
    "90fbbbf28bb83db78643450858ffcfc689a6126401c706f7cf74ed74e36d51ae": "02_gemini_pdf.pdf",
    "80bd3b329fbe821693727495589c28b7553f6b6d36405a38532237ae81379fdc": "03_gpt.md",
    "bf8f87c4406f995efa085b2bdcfb54cdcc24268e63f9ec9913b024d570167c65": "04_claude_signed.txt",
    "38dc96765f35954e123e1dea8462bb77f9ea865998c05f40f4a313dd72f9b8db": "05_grok_short.md",
    "e4c4332ce96c7e1d02c3377f2daf36a8a95223b350974f954fc74019bff00c65": "06_grok_refined.md",
    "c10fca7078470075367978e2e664ffc8495c41e0b6df4f892fba2f8dde8fa429": "07_claude_review_note.md",
    "b6657030de2ce6e921f9daa00b3750c19cd5d7a2f4ef08699fc3f09251ed95f4": "ATTESTATIONS_LEDGER.md",
    "712c00ad0aba94f779981b1fa549d9574e97387b950ce69edf4ac75a68c9ba9c": "MASTER_ROOT.txt",
}


def scan_blocks(db_path, max_blocks=100):
    """Scan recent blocks (by mtime) for proof_submit_v0 events.

    Returns dict mapping sha256_hex → (block_height, block_hash, file_name,
    score, grade, epoch_id) for matched attestations.
    """
    if not os.path.isdir(db_path):
        sys.exit(f"ERROR: db path not found: {db_path}")

    files = []
    for f in os.listdir(db_path):
        if f.endswith(".json"):
            full = os.path.join(db_path, f)
            files.append((os.path.getmtime(full), full))
    files.sort(reverse=True)
    recent = [path for _, path in files[:max_blocks]]

    found = {}
    for path in recent:
        try:
            with open(path) as fp:
                d = json.load(fp)
        except (json.JSONDecodeError, OSError):
            continue
        height = d["header"]["height"]
        bhash = d["block_hash_hex"]
        epoch = d["header"]["epoch_id"]
        for ev in d.get("app_events", []):
            if ev.get("kind") != "proof_submit_v0":
                continue
            if "payload_b64" not in ev:
                continue
            try:
                decoded = base64.b64decode(ev["payload_b64"]).decode("utf-8")
                p = json.loads(decoded)
                fhash = p.get("sha256_hex", "")
                fname = p.get("file_name", "")
                score = p.get("score", "?")
                grade = p.get("grade", "?")
                if fhash in ATTESTATIONS:
                    found[fhash] = (height, bhash, fname, score, grade, epoch)
            except (ValueError, KeyError):
                continue
    return found


def main():
    parser = argparse.ArgumentParser(
        description="Verify Phase 0c.1 attestation bundle on-chain anchoring."
    )
    parser.add_argument(
        "--db-path",
        default="/home/uncrfactory/popchain-data/val-alpha/blocks/",
        help="Path to validator block storage directory.",
    )
    parser.add_argument(
        "--max-blocks",
        type=int,
        default=100,
        help="Number of recent blocks to scan (default: 100).",
    )
    args = parser.parse_args()

    found = scan_blocks(args.db_path, args.max_blocks)

    print("=" * 100)
    print("PHASE 0c.1 ATTESTATIONS ON-CHAIN VERIFICATION")
    print("=" * 100)
    expected = len(ATTESTATIONS)
    for h, name in ATTESTATIONS.items():
        if h in found:
            height, bhash, fname, score, grade, _epoch = found[h]
            match_str = "MATCH" if fname == name else "MISMATCH(" + fname + ")"
            print(f"{name:<30} HEIGHT {height:<8} {bhash[:32]} score={score} grade={grade} | ON-CHAIN {match_str}")
        else:
            print(f"{name:<30} NOT FOUND in last {args.max_blocks} blocks")

    print()
    print(f"FOUND: {len(found)}/{expected}  MISSING: {expected - len(found)}/{expected}")

    if len(found) < expected:
        sys.exit(1)


if __name__ == "__main__":
    main()
