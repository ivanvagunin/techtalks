# C6 — “Approval For All”: names, writes and transfer conditions

## Primary report

**CertiK, “Honeypot Scams”, 11 January 2024.**

[Report](https://www.certik.com/blog/honeypot-scams), archived in `../sources/s3-certik-honeypot-scams.html`. Three associated screenshots were already downloaded and have now been visually reviewed.

This is a practitioner-reported mechanism. A unique chain/address identity for this particular blacklist example remains unresolved. January 2024 is the publication date, not proof that the mechanism was invented then.

## What is directly visible in the images

### Entry point / write

`../sources/s3-snapshot-write.png` shows:

- an entry point named `approveForAll`;
- an array of addresses;
- an `onlyOwner` modifier;
- each supplied address being marked in `_snapshot`;
- an `Approval` event emitted inside the loop.

The image establishes these visible statements, not the complete implementation of the modifier, every storage writer, or the whole token specification.

### Later read / restriction

`../sources/s3-transfer-condition.png` shows a condition on **either endpoint**:

- `_snapshot[from]` **or** `_snapshot[to]`;
- when that condition holds, `_snapshotApplied` must equal true.

The prose report says `_snapshotApplied` is hardcoded false. That assertion is in the article; the cropped condition image does not itself show the flag's declaration or prove the absence of every possible writer.

The distinction is important for captions: **image-observed condition** versus **report-described flag invariant**.

### Transaction-label view

`../sources/s3-approval-label.png` shows repeated entries labelled “Approve For All”, but hashes and addresses are truncated. Their prefixes/suffixes are not sufficient to establish full deployment or transaction identifiers safely.

Do not invent a full address, a chain, a transaction hash or an amount from that crop.

## Strongest supported technical explanation

Follow the stored membership bit from the write into the later condition. Under the flag value described by the report, an operation involving a listed endpoint cannot satisfy that extra requirement.

This supports a restriction claim, not a blanket statement that every unlisted account can trade. Other conditions may apply. It also does not establish the entire ERC-20 approval state from the function name or the emitted event.

The psychologically misleading cue is familiar approval language and event naming. The technical evidence is the storage write and subsequent predicate, not an inferred mental state of an unknown trader.

## Attribution trap inside the same article

The article separately links a **fake Shia token** in another example. That linked address must not be reused as the deployment identity for the `approveForAll` / `_snapshot` blacklist merely because it appears in the same report.

Likewise, balance-change-without-events examples later in the article are separate mechanisms. They cannot establish this example's transaction sequence.

## What we can show now

The existing deck already uses the write/read screenshots. Refine the caption to say:

> The image shows an owner-restricted membership write and a transfer condition checking either endpoint. CertiK's accompanying prose states that the required flag is false.

Use a report-derived logical outcome, not a table of invented before/after executions. A disclosed restriction can serve as a conceptual benign control; do not call every restriction criminal.

## What remains to make this an on-chain case

A unique deployment identity and historical verified source, then the relevant state-changing transaction and a later affected operation with reviewed state/trace evidence. If those cannot be recovered, keep this as a short, attributed report example rather than the presentation's most substantial real-world anchor.

S6 (*Why Trick Me*, 2023) supports the broader DEX-trap context, but it does not supply the missing provenance for these particular images.

## Sources / archive

- S3 article and three named PNGs in `../sources/`.
- S6 archived paper for the adjacent research context.
- Original download provenance: `../manifest.json`.

No deployed blacklist token was constructed, simulated or tested in this pass. Source-image reading does not establish current client behavior or criminal intent.
