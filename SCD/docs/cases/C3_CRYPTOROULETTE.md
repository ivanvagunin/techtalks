# C3 — CryptoRoulette: historical storage-reference behavior

## Identity and chronology

- Ethereum address: `0x94602b0e2512ddad62a935763bf1277c973b2758` (S1 Appendix A).
- [Explorer](https://etherscan.io/address/0x94602b0e2512ddad62a935763bf1277c973b2758) reports **Exact Match**, contract `CryptoRoulette`.
- Compiler: **v0.4.19+commit.c4cbbb05**; optimisation **Yes, 200 runs**.
- Creation: **19 February 2018, 12:14:19 UTC**, block **5118518**, position **137**.
- [Creation transaction](https://etherscan.io/tx/0xefa4e5dc40389240dbb4027db38b351041b75b488d2e0720ee9b05488f2240e1).

All metadata above is explorer-reported and archived, not an independently reproduced build.

## What the retrieved source contributes

The source contains a secret value, participation bookkeeping using a local `Game` reference, and a subsequent comparison against the secret. The uninitialised reference precedes writes through its fields. This matches the historical storage-aliasing mechanism described in S1 Figure 6.

The important explanatory distinction is **write-before-read**: discovering a value before execution does not prove that the same value reaches a comparison after other instructions run.

Two concrete source details are useful but must not be conflated:

- The comments and shuffle logic describe numbers from **1 to 20**.
- The admission condition restricts the supplied number to **at most 10**.

The difference is visible in the explorer source. It is not, by itself, proof of the complete historical storage write/read sequence.

Do not repeat the paper's imprecise suggestion that every struct requires `new`. The issue is the historical semantics of an **uninitialised local storage reference**. Modern language behavior and diagnostics are different. The Solidity 0.5.0 breaking-changes documentation explicitly says uninitialised storage variables are disallowed; it also requires explicit data locations for relevant variable types.

## Real historical play transaction

[0xc109a14f9588baf3e2a6189795e7a8a10b84a4c5a573effb988c1cc986c0a0d7](https://etherscan.io/tx/0xc109a14f9588baf3e2a6189795e7a8a10b84a4c5a573effb988c1cc986c0a0d7)

The archived page reports:

- **20 February 2018, 13:17:49 UTC**;
- block **5124620**, position **196**;
- method display `play`, value **0.1 ETH**;
- status **Success**.

This establishes an explorer-documented invocation, not that the participant won, lost through a specific alias, or held a particular belief. We have not independently recovered its execution trace or storage changes.

## The contract's lifecycle matters

The explorer also explicitly reports a self-destruction:

[0xe40affc8f5d2482bcd2f55eef6d65dbb10346017c05ae785d46503c4f2187d37](https://etherscan.io/tx/0xe40affc8f5d2482bcd2f55eef6d65dbb10346017c05ae785d46503c4f2187d37)

- **23 February 2018, 21:43:55 UTC**;
- block **5144265**, position **24**;
- method display `kill`, explorer status **Success**.

This is an additional reason not to use current code/state as a substitute for the 2018 artifact. It predates Ethereum's EIP-6780 semantics. Current explorer retention of old source/bytecode is not proof that the code remains deployed now.

## Presentation value

Use the source chronology and symbolic write/read relationship, with the real play transaction as an explicitly explorer-sourced historical anchor. Once historical execution evidence is obtained, annotate the actual mutation before the comparison rather than showing an invented storage layout.

Avoid teaching how to exploit the contract or reproduce the historical vulnerability. The value of the case is how a correct observation about readable storage can still produce the wrong execution prediction.

## Sources / archive

- S1 Figure 6 / Appendix A.
- `../sources/c3-cryptoroulette-etherscan.html`, `c3-cryptoroulette-creation.html`, `c3-cryptoroulette-play.html`, `c3-cryptoroulette-destruction.html`.
- `../text/c3-cryptoroulette-etherscan-CryptoRoulette.sol.txt`.
- [Solidity 0.5.0 breaking changes](https://docs.soliditylang.org/en/v0.5.0/050-breaking-changes.html), archived as `c3-solidity-050-changes.html`.
- S9/EIP-6780 for the historical execution-era boundary.

**Remaining:** independent bytecode/build association, reviewed historical data flow, transaction-level state effects. No executable reconstruction was performed.
