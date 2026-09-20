# C1 — Hidden state: Gift 1 ETH

## Identity and chronology

- Ethereum address: `0xd8993f49f372bb014fb088eabec95cfdc795cbf6`.
- S1, *The Art of The Scam*, Figure 7 / §3.2.3 describes the mechanism; Appendix A identifies this deployment.
- [Explorer](https://etherscan.io/address/0xd8993f49f372bb014fb088eabec95cfdc795cbf6) snapshot labels source **Exact Match**, contract `Gift_1_ETH`.
- Explorer-reported compiler: **v0.4.19-nightly.2017.10.28+commit.f9b24009**; optimisation **No**. Source pragma is `^0.4.17`; the pragma is not the exact compiler version.
- Creation: **29 October 2017, 17:58:53 UTC**, block **4453086**, transaction position **58**, explorer status **Success**.
- [Creation transaction](https://etherscan.io/tx/0xab8180c3eea86c9702daacb7fbe17368cfa9c313f90a6d341c72797bd738d7e3).

**Historical correction:** this address is not the January 2017 example. January 2017 is S1's earliest hidden-state honeypot in its dataset, not the creation date of Gift 1 ETH and not a proven first-ever Ethereum deception.

## What the source establishes

The archived explorer source contains the false initializer for `passHasBeenSet`, a guarded password-hash write, and a separate operation capable of setting the flag true after checking the supplied hash against the stored hash.

The setting path's conditional body is not the same as a transaction-wide assertion. If the flag condition is false, a successful outer transaction does not prove that the hash was written. The distinction is between transaction success and the intended state postcondition.

This materially supports the manuscript's source-versus-current-state explanation. It does not establish the value of the flag at any selected historical transaction.

## What S1 reports beyond the source

S1 attributes the deception to historical explorer filtering of zero-value internal messages. A nested call with no ether transfer could still set the flag, while a convenient displayed history did not show the change.

That is a historical claim from the researchers, not a result reproduced in this pass. Current explorer views cannot prove what an observer saw in 2017, and an empty modern internal-transactions view cannot establish that no internal state change occurred.

## A concrete historical transaction to investigate

[Transaction `0xa29c1875ef712b7b7c812bf2d1fa48e53ef56423a6882a55c51a1342880636da`](https://etherscan.io/tx/0xa29c1875ef712b7b7c812bf2d1fa48e53ef56423a6882a55c51a1342880636da)

The archived page reports:

- 3 November 2017, **19:58:42 UTC**;
- block **4484437**, position **13**;
- recipient is the Gift contract;
- method display `SetPass`; value **1 ETH**;
- status **Success**.

This is a real, identified historical transaction—not a fabricated example. However, **we have not established whether the guarded write occurred**. That needs the transaction pre-state and resulting state, or a sufficiently complete reviewed execution trace. The sender's intent is also not established.

## Strongest supported presentation claim

> The published source has a guarded state write. The explorer records a successful transaction into that entry point. Transaction success alone does not tell us whether the guard permitted the write.

Then attribute the missing-internal-call mechanism separately to S1. Do not narrate the identified transaction as a proven victim loss or the hidden state transition until those facts are recovered.

## Sources / archive

- `../sources/s1-torres-2019.pdf`, Figure 7, §3.2.3, Appendix A.
- `../sources/c1-gift-etherscan.html`, `c1-gift-creation.html`, `c1-gift-setpass.html`.
- Source reading aid: `../text/c1-gift-etherscan-Gift_1_ETH.sol.txt`.
- URL/timestamp/hash provenance: `../case-materials-manifest.json`; derived source hashes: `derived-source-manifest.json`.

## Remaining gate

Recover the flag-changing internal call and relevant transaction-level state, and check the claimed historical display omission. Explorer metadata/source/transaction pages have been read, not independently validated against an archive node. No code was compiled, deployed or replayed.
