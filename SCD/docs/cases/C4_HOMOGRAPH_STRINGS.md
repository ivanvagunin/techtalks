# C4 — Homograph strings: paper versus author artifact

## Classification

**Research demonstration**, not an independently attributed criminal deployment. S2 is Ivanov et al., *Targeting the Weakest Link: Social Engineering Attacks in Ethereum Smart Contracts* (2021). The named legitimate projects are experimental carriers; their inclusion does not show those projects were compromised.

## Original source chain now recovered

The paper links the authors' [research page](https://nick-ivanov.github.io/se-info/). That page embeds an A4 artifact from a GitHub Gist. We retrieved the Gist API response, including the complete, non-truncated `A4.sol` content and revision metadata.

- Gist ID: `cbddfacdf36c8c815a55d7175dc90ab7`.
- Latest content revision reported: `6479448294d405eb74a0badc81a54f76275b706d`.
- Revision committed: **10 December 2020, 13:47:10 UTC**.
- Gist creation: **7 December 2020**.
- API `updated_at`: **20 January 2022**. Do not mistake this API timestamp for the commit date of the source content.
- Source pragma: `^0.5.11`; this is a constraint, not a pinned full build or confirmation of imported dependency versions.

We inspected source bytes only. We did not compile, deploy, run the token or retrieve the entire attack repository.

## Important discrepancy with the manuscript's paper example

S2 §4.2.1 / Figure 5 describes an ASCII `BT` literal and a visually similar returned symbol containing a Cyrillic replacement. The prose discusses a mutable `symbol()` return value.

The currently retrieved author A4 artifact instead contains a comparison against **`BСT`**, with a Cyrillic letter in the **literal itself**. Its visible constructor accepts a symbol argument; the file does not itself contain a symbol setter. Its imported dependencies have not been pinned or analysed here.

Therefore:

- Do not show this artifact's byte dump beside the paper's `BT` example and imply they are identical.
- Do not claim that this file independently establishes the paper's dynamic symbol-update scenario.
- Either present the paper version with its own evidence limitations, or explicitly present this version as **the authors' separately retrieved A4 artifact**.

This is a useful correction, not a reason to discard the example.

## Exact inert data evidence

The retrieved comparison literal has these code points:

| Character | Code point | Name |
|---|---|---|
| `B` | U+0042 | LATIN CAPITAL LETTER B |
| `С` | U+0421 | CYRILLIC CAPITAL LETTER ES |
| `T` | U+0054 | LATIN CAPITAL LETTER T |

UTF-8 bytes:

```text
Author artifact literal BСT: 42 d0 a1 54
ASCII control          BCT: 42 43 54
```

The byte strings differ. That is independently established by static inspection of the archived artifact, without executing a contract.

The artifact's helper hashes `abi.encode` of each string. **Do not caption the four-byte UTF-8 sequence as the complete hash preimage.** ABI encoding also contains structural information and padding. This pass establishes the raw string data difference, not captured compiler output, hash digests or a runtime branch result.

Machine-readable evidence and artifact hash: `c4-string-evidence.json`.

## Presentation treatment

Use a two-stage reveal: apparently familiar text, then the code-point and raw-byte table. Clearly title it “Author A4 artifact, revision 6479448…” rather than “exact reproduction of Figure 5”. State that this is string data, not Unicode Solidity identifiers.

Explain the predicate-input distinction; avoid suggesting that every non-ASCII string is malicious. A plain string-inspection panel is enough—there is no need for a deployed deceptive token demonstration.

## Sources / archive

- `../sources/s2-ivanov-2021.pdf`, §4.2.1 / Figure 5.
- `../sources/c4-author-research-page.html` (contains the embedded artifact link).
- `../sources/c4-a4-author-gist.json` (full fetched response with content/revision metadata).
- `../text/c4-a4-A4.sol.txt` (derived reading aid).
- `c4-string-evidence.json`; `../case-materials-manifest.json`.
- The authors' integration-repository README is also archived as `c4-author-artifact-readme.md`; it is not evidence of real-world compromise.

**Remaining:** choose which artifact version the talk will present and align the narrative accordingly. Only claim a compiled/runtime result after a separate, appropriately scoped observation exists; none is claimed here.
