# C5 — Hiding in Plain Sight: historical source-verification failure

## Primary source and correct event identity

**samczsun, “Hiding in Plain Sight”, 11 November 2021.**

[Original article](https://www.paradigm.xyz/writing/hiding-in-plain-sight), archived in `../sources/s4-hiding-in-plain-sight.html`.

The article describes a researcher-built challenge using a real historical Etherscan verification flaw. Its author explains that it was developed as a teaser around planning for **Paradigm CTF 2022**.

**Do not call this the Paradigm CTF 2021 `swap` challenge.** The article opens by referring to that earlier challenge as background. We followed and archived the linked `swap` write-up, dated 8 April 2021, specifically to disambiguate the two. It is a separate compiler-bug challenge, not corroboration of the metadata-verifier failure.

## Technical mechanism and evidence

Source verification relates submitted source and build settings to code artifacts. It does not certify benign behavior. The original author reports that the verifier's metadata recognition could treat behaviorally meaningful bytes as ignorable during comparison.

The significance is artifact association: an accepted verification result could support source that did not describe the deployed behavior. This is not simply an analyst overlooking a condition in correctly associated source.

The author's article includes verification UI screenshots and an observed call failure. It reports the call producing a **stack-underflow error** despite what the displayed source would suggest. Those are **author-reported observations**, not our execution results.

The reported experiments were on **Ropsten**, not Ethereum mainnet. The article's sample address is:

`0x3cd2138cabfb03c8ed9687561a0ef5c9a153923f`

This address is an identifier within that historical testnet account. It must not be attached to a mainnet explorer link or represented as a current reachable demonstration. The article's displayed call example is not itself a transaction receipt with a transaction hash.

## What has and has not been checked

Checked in the archived primary article:

- author, date, historical experimental context;
- the stated source/bytecode comparison failure;
- the distinction between the earlier `swap` challenge and the later teaser;
- the Ropsten context and author-shown behavioral discrepancy.

Not checked independently:

- historical RPC state or runtime trace;
- a fresh build and comparison of original artifacts;
- the exact historical verifier implementation or patch timeline;
- whether any analogous present-day behavior exists.

No current-service testing or bypass reproduction was performed.

## Relationship to the other cases

- Private Bank: source can be correctly displayed while the reader assigns the wrong identity to a dependency.
- CPIMP: the proxy's reported implementation relationship can be misleading despite normal functionality.
- This case: the association between displayed source and deployed artifact itself can be incorrect.

Do not collapse these into “Etherscan is untrustworthy.” They are distinct failure modes with different evidence and historical applicability.

## Best presentation panel

A credited author screenshot or a clearly labelled conceptual comparison, accompanied by the author-reported call discrepancy. Show which kind of artifact each panel describes: source, source-derived build material, deployed runtime, or verifier comparison view.

Do not add invented byte offsets, reconstructed masks, fabricated current explorer screenshots, operational bypass instructions or new exploitation artifacts. The primary published evidence already supports the historical explanation.

## Sources / archive

- S4 article and `../text/s4-hiding-in-plain-sight.html.txt`.
- S5 NDSS 2024 paper/slides for broader verification-service research, **not** proof of the exact S4 experiment.
- `../sources/c5-ctf-challenge-context.html`: earlier [Paradigm CTF 2021 — swap](https://samczsun.com/paradigm-ctf-2021-swap/), archived to establish the distinction, not as the main case.
- Original S4 provenance in `../manifest.json`; newly followed context in `../case-materials-manifest.json`.

**Presentation-ready scope:** an attributed historical research demonstration. Not an observed criminal campaign or independently reproduced verification bypass.
