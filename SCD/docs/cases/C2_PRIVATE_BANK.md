# C2 — Private Bank: dependency identity and the limits of the paper model

## Identity and provenance

- Ethereum address: `0xd116d1349c1382b0b302086a4e4219ae4f8634ff` (S1 Appendix A).
- [Explorer](https://etherscan.io/address/0xd116d1349c1382b0b302086a4e4219ae4f8634ff) reports **Exact Match**, contract `Private_Bank`.
- Compiler: **v0.4.19+commit.c4cbbb05**; optimisation **No**.
- Creation: **12 February 2018, 23:52:49 UTC**, block **5079695**, position **53**, explorer status **Success**.
- [Creation transaction](https://etherscan.io/tx/0x1bd6347bc5c6e0b7af095863e4a2713df4ea932757d852b5a181de817d4bd096).

## New evidence: the configured dependency

The explorer decodes the constructor's `_log` argument as:

`0xF8681Dad1cE4f1f414FB07FC07f81a3A82E91D8f`

The appended constructor word visible in the creation material agrees with that displayed address. This is a cross-check within explorer-supplied material, **not independent RPC/code-hash verification**.

The dependency page is archived. No verified source was recovered for it; its embedded source map is empty. Do not silently substitute the benign `Log` class printed beside the bank for this dependency's implementation.

## Important difference from S1 Figure 9

The retrieved source is not identical to the simplified paper figure:

- The actual source's deposit guard is **strictly greater than** `MinDeposit`; the figure uses greater-than-or-equal.
- The source's logger interface has **address, value and string** arguments; the figure simplifies the call to a string.

These are reasons to preserve the distinction between the paper's mechanism and an exact deployment analysis. They also make this a useful case for explaining why a copied simplified fixture is not a historical replay.

## The deposit: a rounding trap for our own research

[Deposit transaction](https://etherscan.io/tx/0x46fd827bbc02ef0ac626c0f850458191c1b8c36cb9c5375194bafa9642f38124):

- **13 February 2018, 00:23:48 UTC**;
- block **5079803**, position **58**;
- explorer status **Success**;
- exact displayed transaction value **1.0000000623552385 ETH**.

The address-history row rounds the amount to `1.000000 ETH`. The detailed transaction value is actually greater than one ether, so the row must not be used to claim that this transaction failed the source's strict deposit condition. No state-diff claim is made from the receipt alone.

This is a particularly relevant research lesson: our own convenient representation can erase a behaviorally significant difference.

## Evidence that prevents an overbroad failure claim

The address page includes later internal-transfer records. One containing transaction is:

[0x494a3fa918f12bb63e0de41474bc63e0c02137ae3ae1f3c58f63864c01fee537](https://etherscan.io/tx/0x494a3fa918f12bb63e0de41474bc63e0c02137ae3ae1f3c58f63864c01fee537)

Its archived page reports **Success**, **15 February 2018, 22:07:10 UTC**, block **5097030**, position **187**. Its top-level recipient is another contract, not Private Bank itself. It is linked from the bank's internal-transaction history.

**Do not present this as a failed withdrawal or identify its operator as a victim.** The containing transaction, nested execution and bank involvement need to be analysed together. The snapshot does not support a universal assertion that every interaction with this bank reverted or that nobody could withdraw.

## What the published research says

S1 Figure 9 explains a straw-man dependency which causes the attractive withdrawal path to fail. It supports the mechanism and the risk of trusting a displayed logger. It does not remove the need to establish the actual dependency behavior for this address at the chosen execution point.

The deck should say **“S1's published mechanism”** until a decisive historical call path is corroborated. Actual caller-dependent behavior, full failure propagation and state effects remain unresolved here.

## Sources / archive

- S1 Figure 9 / Appendix A.
- `../sources/c2-private-bank-etherscan.html`, `c2-private-bank-creation.html`, `c2-private-bank-logger.html`, `c2-private-bank-deposit.html`, `c2-private-bank-later-execution.html`.
- `../text/c2-private-bank-etherscan-Private_Bank.sol.txt`.
- Manifests: `../case-materials-manifest.json`, `derived-source-manifest.json`.

## Next evidence gate

Historical logger code identity and the relevant call/failure path. Do not build an exploit or extrapolate from a recreated logger. This pass collected public historical records only; no compiler or chain execution was performed.
