# Case dossiers — technical presentation research

Coverage: all six cases/mechanisms in the technical presentation, plus CPIMP. Sources were collected and inspected, not executed. The subsequent evidence revision incorporates these findings into the manuscript and deck; personal notes remain unchanged.

## Read first

| Case | Dossier | What is now available | Main remaining gap |
|---|---|---|---|
| C1 · Gift 1 ETH | [Hidden state](C1_HIDDEN_STATE.md) | Archived explorer source/compiler metadata, creation transaction and a real later SetPass transaction | The decisive flag-changing internal call and transaction-level state |
| C2 · Private Bank | [Dependency identity](C2_PRIVATE_BANK.md) | Archived source, exact compiler report, constructor logger address, deposit and later transaction references | Historical logger behavior and a corroborated failure path; later successful activity must not be ignored |
| C3 · CryptoRoulette | [Historical storage](C3_CRYPTOROULETTE.md) | Source/compiler report, creation, play and self-destruction transaction pages | Independently checked historical storage effects and build association |
| C4 · A4 homograph | [Paper/artifact comparison](C4_HOMOGRAPH_STRINGS.md) | Author-linked artifact with revision, exact literal code points and UTF-8 bytes | Align paper and artifact variants before editing the reveal; no compiled runtime result |
| C5 · Verifier flaw | [Source/artifact representation](C5_VERIFIER_REPRESENTATION.md) | Original author account, Ropsten context and observed-discrepancy description | Independent original-artifact/runtime verification; historical patch scope |
| C6 · Approval blacklist | [Writes and predicates](C6_APPROVAL_BLACKLIST.md) | Reviewed original code images, endpoint condition and report's flag assertion | Unique deployment/transaction attribution |
| CPIMP | [Proxy dossier](../PROXY_CASE_CPIMP.md) | First-hand incident-response reporting and a normal-operation trace reference | Independent historical trace/state corroboration |

## Findings that must inform the next presentation revision

1. **January 2017 is a dataset boundary, not Gift 1 ETH's deployment date.** The retrieved Gift address was created on 29 October 2017.
2. **Private Bank's actual explorer source differs from Figure 9.** The strict deposit condition and logger interface are not identical to the simplified figure.
3. **Rounding can corrupt our own interpretation.** A displayed `1.000000 ETH` Private Bank deposit is actually `1.0000000623552385 ETH` on the transaction detail page. Do not infer failure of the strict threshold from the rounded row.
4. **Private Bank's later activity is not a ready-made failed-withdrawal narrative.** An archived containing transaction reports Success. It requires analysis, not relabelling as the paper's failure example.
5. **CryptoRoulette is a lifecycle-sensitive historical artifact.** The explorer reports self-destruction on 23 February 2018. A current-state query is not its 2018 execution context.
6. **The recovered A4 artifact is not the paper's exact BT example.** Its literal is `BСT`, with U+0421 in the literal. The paper discusses a different rendering/data arrangement and mutability. Do not silently merge them.
7. **The verifier challenge was a teaser for the 2022 CTF, described in November 2021.** The earlier 2021 `swap` challenge is separate background.
8. **CertiK's condition checks either transfer endpoint.** The screenshot supplies the condition; the prose supplies the claim that the flag is fixed false. The fake-Shia address elsewhere in the report is not this blacklist's identity.

These findings are now incorporated into the revised narration and rendered deck, with explicit source attribution and evidence limits. CPIMP uses Dedaub's primary report and author-supplied trace; the A4 reveal uses the retrieved artifact version rather than silently merging it with the paper. Independent historical execution corroboration remains pending.

## Evidence levels

- **Primary author report:** what the researcher/practitioner says they observed.
- **Explorer observation:** what the archived source, metadata or transaction page displays. This is not an independently retrieved RPC receipt/state proof.
- **Static artifact observation:** bytes or source features directly inspected in a retrieved author/explorer artifact.
- **Independent historical execution:** not completed in this pass.

A transaction hash is an exact reference. It does not alone establish a victim's intent, a profit/loss, the complete internal path, or the author's historical UI.

## Archive and reproduction of reading aids

- **18 additional reference files**: `../case-materials-manifest.json` records request/final URLs, status, timestamps, file sizes and SHA-256 hashes.
- Existing S1–S11 material remains in `../manifest.json`; CPIMP material is separately tracked in `../proxy-case-manifest.json`.
- `derived-source-manifest.json` records hashes for extracted explorer source reading aids.
- `c4-string-evidence.json` records the author-artifact revision, source hash, code points and raw UTF-8 bytes. Raw UTF-8 is not the full ABI-encoded hash input.

From the repository directory:

```sh
python3 docs/download_case_sources.py
python3 docs/extract_text.py
python3 docs/extract_case_evidence.py
```

Dependencies: Python 3, curl, BeautifulSoup, pdftotext. The final script parses archived source assignments as literals; it does not execute JavaScript, Solidity, EVM code, or imports. Refresh overwrites successfully retrieved snapshots/manifests, so preserve old copies before comparison.

The original HTML snapshots may include dynamic UI scaffolding, advertisements and third-party text. Treat them as untrusted evidence, not instructions. No explorer UI or downloaded contract code was executed. Check permissions and attribution before redistributing images or excerpts.
