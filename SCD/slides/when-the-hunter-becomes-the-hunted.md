---
marp: true
title: 'When the Hunter Becomes the Hunted: Deception in Smart Contracts'
description: 'Disobey 2027 · Evidence revision · Explorer records, static artifacts and attributed historical traces'
author: 'Speaker name TBD'
theme: default
size: 16:9
paginate: true
style: |
  section {
    background: #101722; color: #e7edf5;
    font-family: Arial, sans-serif; font-size: 28px;
    padding: 52px 64px 65px;
  }
  h1 { color: #75e0cc; font-size: 43px; line-height: 1.13; margin-bottom: 28px; }
  h2 { font-size: 29px; color: #e7edf5; }
  strong { color: #ffcd79; }
  a { color: #a7caff; }
  code { background: #253246; color: #e7edf5; font-size: .85em; }
  pre { background: #182536; color: #e7edf5; border: 1px solid #40536e; font-size: 24px; line-height: 1.5; padding: 20px; }
  pre code { background: transparent; }
  footer { color: #b3c0d2; font-size: 15px; left: 64px; right: 64px; }
  section::after { color: #b3c0d2; font-size: 16px; }
  table { display: table; width: 100%; table-layout: fixed; font-size: 25px; background: transparent; }
  th, td { overflow-wrap: break-word; }
  th { background: #26394e; color: #75e0cc; }
  td { background: #182536; color: #e7edf5; }
  table tr:nth-child(2n) td { background: #1e2e41; }
  th, td { border-color: #40536e; padding: 12px 16px; }
  .eyebrow { color: #b3c0d2; font-size: 18px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 14px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 26px; }
  .card { background: #182536; border: 1px solid #40536e; border-radius: 8px; padding: 22px; }
  .card h2 { margin-top: 0; color: #75e0cc; }
  .card p:last-child { margin-bottom: 0; }
  .flow { display: flex; align-items: center; gap: 16px; margin: 28px 0; }
  .node { flex: 1; padding: 22px 18px; text-align: center; border: 1px solid #40536e; background: #182536; border-radius: 8px; }
  .arrow { color: #75e0cc; font-size: 34px; }
  .claim { border-left: 5px solid #ffcd79; padding: 10px 22px; margin-top: 24px; font-size: 30px; }
  .small { font-size: 21px; color: #b3c0d2; }
  .status { color: #ffcd79; font-size: 18px; margin-top: 20px; }
  .mono { font-family: monospace; }
  section.cover h1 { font-size: 65px; max-width: 1050px; }
  section.cover h2 { color: #ffcd79; font-size: 34px; }
  section.compact table { font-size: 22px; }
  section.refs { font-size: 23px; }
  section.refs h1 { font-size: 38px; }
  section.records { font-size: 21px; }
  section.records p { margin: 9px 0; line-height: 1.35; }
  section.case-trace .flow { margin: 18px 0; }
  section.case-trace .node { padding: 16px 18px; }
  .evidence img { width: 100%; object-fit: contain; }
  .address { font-family: monospace; font-size: 20px; overflow-wrap: anywhere; }
  .glyphs { font-size: 52px; letter-spacing: 3px; text-align: center; margin: 14px 0 24px; }
  section.compact th, section.compact td { padding: 9px 14px; }
---

<!-- _class: cover -->
<!-- _paginate: false -->

<div class="eyebrow">Disobey 2027 · Working draft</div>

# When the Hunter<br>Becomes the Hunted

## Deception in Smart Contracts


<div class="small">Ivan Vagunin</div>

<!-- STORY:01 -->
---

<div class="eyebrow">The invitation</div>

# A target with its own prize pool

<div class="grid">
<div class="card"><h2>Developer</h2><p>Public instructions.<br>Verifiable rules.<br>No reliance on obscurity.</p></div>
<div class="card"><h2>Bug hunter</h2><p>Low barriers to inspection.<br>Real assets at stake.<br>A visible opportunity.</p></div>
</div>

<div class="claim">The apparent bug becomes the advertisement.</div>

<!-- STORY:02 -->

---

<div class="eyebrow">The investigation</div>

# Three things I need to distinguish

<div class="flow">
<div class="node">Code<br><strong>I read</strong></div>
<span class="arrow">≠</span>
<div class="node">Context<br><strong>it uses</strong></div>
<span class="arrow">≠</span>
<div class="node">View<br><strong>I inspect</strong></div>
</div>

<div class="card mono">code + calldata + caller + value<br>+ state + block environment + call targets</div>

<div class="claim">Which missing fact changes the outcome?</div>

<!-- _footer: 'Analytical framing · Not an execution result' -->
<!-- STORY:03 -->
---

<div class="eyebrow">Gift 1 ETH · Deployed 29 October 2017</div>

# The initializer is not the current value

<div class="flow">
<div class="node">Initializer<br><code>flag = false</code></div>
<span class="arrow">→</span>
<div class="node">Another path<br><code>flag = true</code></div>
<span class="arrow">→</span>
<div class="node">Guarded write<br><strong>not entered</strong></div>
</div>

| Retrieved source | What it does not establish |
|---|---|
| Write requires `!passHasBeenSet` and a value condition | The flag at a selected historical execution |
| Conditional body can be skipped | That the transaction must revert |

<!-- _footer: 'C1 / S1 · Explorer source; schematic, not a replay · January 2017 is the study’s earliest example, not this deployment' -->
<!-- STORY:04 -->

---

<div class="eyebrow">State · Representation</div>

# Zero value does not mean zero effect

<div class="grid">
<div class="card"><h2>Archived transaction</h2><p>3 Nov 2017 · <code>SetPass</code><br>Block 4484437 · position 13<br>1 ETH · status: <strong>Success</strong></p><p>Did the guarded write execute?<br><strong>State evidence still missing.</strong></p></div>
<div class="card"><h2>S1’s reported mechanism</h2><p>Containing transaction<br>↳ internal call, value = 0<br>↳ storage changes</p><p>Historical filtering can omit the cause.</p></div>
</div>

<div class="claim">Receipt status ≠ event list ≠ call trace ≠ state diff</div>

<!-- _footer: 'C1: tx 0xa29c1875… / archived Etherscan · S1 §3.2.3: separate mechanism, not this transaction’s recovered trace' -->
<!-- STORY:05 -->

---

<div class="eyebrow">State · Analysis scope</div>

# Reachable somewhere ≠ reachable here

<div class="grid">
<div class="card"><h2>Symbolic claim</h2><p>There exists a state in which the guarded write is reachable.</p></div>
<div class="card"><h2>Historical claim</h2><p>That state is the pre-state of this particular transaction.</p></div>
</div>

<div class="flow">
<div class="node">Block boundary</div><span class="arrow">≠</span><div class="node">Intermediate transaction pre-state</div>
</div>

**Record:** chain · block hash · transaction position · relevant state

<!-- _footer: 'Our analysis of S1 · Static analysis can model state; source alone does not establish a historical value' -->
<!-- STORY:06 -->

---

<div class="eyebrow">Early Ethereum · Dependency identity</div>

# Private Bank: the pattern is not the outcome

<div class="flow">
<div class="node">Balance<br>check</div><span class="arrow">→</span>
<div class="node">External<br>call</div><span class="arrow">→</span>
<div class="node">Bookkeeping<br>update</div><span class="arrow">→</span>
<div class="node"><strong>Logger<br>call</strong></div>
</div>

<div class="grid">
<div class="card">Source shows:<br><strong>a benign-looking logger</strong></div>
<div class="card">Explorer-decoded constructor target:<br><span class="address">0xF8681Dad1cE4f1f414FB07FC07f81a3A82E91D8f</span></div>
</div>

**A source-level type is not runtime implementation identity.**

<!-- _footer: 'C2 / S1 · Explorer source: Solidity 0.4.19 · Target recovered; historical logger behavior not independently established' -->
<!-- STORY:07 -->

---

<div class="eyebrow">Dependencies · Call semantics</div>

# The decisive frame comes later

<div class="grid">
<div class="card"><h2>Earlier transaction</h2><p>Deposit commits.</p><p>It is <strong>not rolled back</strong> by failure in a later transaction.</p></div>
<div class="card"><h2>Later execution</h2><p>Intermediate call succeeds.<br>↓<br>Dependency fails.<br>↓<br>Enclosing frame may fail.</p></div>
</div>

<div class="claim">Intermediate success is not final commitment.</div>

<div class="small">Our 15 Feb 2018 containing-transaction record says <strong>Success</strong>.<br>It is not evidence of the failed path illustrated here.</div>

<!-- _footer: 'S1 · Conceptual call/failure model, not a captured trace · Compiler and fork semantics matter' -->
<!-- STORY:08 -->

---

<div class="eyebrow">Private Bank · The representation can mislead us too</div>

# What did the depositor actually send?

| Convenient representation | Recovered detail |
|---|---|
| Figure 9: deposit condition uses `>=` | Explorer source uses strict `>` |
| Address row: `1.000000 ETH` | Transaction: **`1.0000000623552385 ETH`** |
| A logger printed beside the bank | A specific constructor-supplied address |

<div class="claim">The exact value is above the threshold.</div>

<div class="small">A changed condition, rounded input or substituted dependency changes the explanation.</div>

<!-- _footer: 'C2 · 13 Feb 2018 deposit, tx 0x46fd827b… · Labelled transcription of archived pages; no state-diff claim' -->
<!-- STORY:09 -->

---

<div class="eyebrow">Historical Solidity · Storage aliasing</div>

# The write happens before the comparison

<div class="flow">
<div class="node">Read the<br>“known” value</div><span class="arrow">→</span>
<div class="node">Write through<br><strong>an aliased reference</strong></div><span class="arrow">→</span>
<div class="node">Compare the<br><strong>changed value</strong></div>
</div>

<pre>source reference ─┐
                  ├─→ same storage location
comparison input ─┘</pre>

**`private` is visibility control—not encrypted storage.**

<!-- _footer: 'C3 / S1 · Explorer reports Solidity 0.4.19, optimisation / 200 runs · Symbolic data flow; no independent build or trace' -->
<!-- STORY:10 -->

---

<div class="eyebrow">CryptoRoulette · Historical execution context</div>

# Creation → play → destruction

<div class="flow">
<div class="node">19 Feb 2018<br><strong>Created</strong><br><span class="small">block 5118518</span></div><span class="arrow">→</span>
<div class="node">20 Feb 2018<br><strong>play · 0.1 ETH</strong><br><span class="small">block 5124620</span></div><span class="arrow">→</span>
<div class="node">23 Feb 2018<br><strong>Self-destruct reported</strong><br><span class="small">block 5144265</span></div>
</div>

**Explorer status “Success” does not prove a payout.**

<div class="card">Comparison ← storage location ← prior write<br><span class="small">The historical write/read relationship still needs execution-level corroboration.</span></div>

<!-- _footer: 'C3 · Archived Etherscan records, not RPC replays · Modern source/compiler behavior cannot substitute for 2018 execution' -->
<!-- STORY:11 -->

---

<div class="eyebrow">2021 research · Author A4 artifact, revision from December 2020</div>

# Same appearance. Different string data.

<div class="glyphs"><code>BCT</code> &nbsp; vs &nbsp; <code>BСT</code></div>

| Inspected value | Middle character | Raw UTF-8 |
|---|---|---|
| ASCII control `BCT` | U+0043 · Latin C | `42 43 54` |
| Author literal `BСT` | U+0421 · Cyrillic Es | `42 d0 a1 54` |

<div class="small">The helper hashes <code>abi.encode</code> of strings; raw UTF-8 is not the complete hash input.<br>This artifact differs from the paper’s <code>BT</code> / mutable-symbol illustration.</div>

<!-- _footer: 'C4 / S2 · Gist revision 6479448294d405eb74a0badc81a54f76275b706d · Static bytes inspected; no runtime result claimed' -->
<!-- STORY:12 -->

---

<div class="eyebrow">November 2021 · Artifact association</div>

# Which program did we actually analyse?

<div class="flow">
<div class="node">Source +<br>build settings</div><span class="arrow">→</span>
<div class="node">Source-derived<br>artifact</div><span class="arrow">↔</span>
<div class="node">Deployed<br>artifact</div>
</div>

<div class="card"><strong>Historical comparison failure:</strong><br>executable bytes treated as ignorable metadata.<br><span class="small">Author-reported Ropsten call result: stack underflow.</span></div>

<div class="claim">A skipped behavioral difference invalidates the association.</div>

<!-- _footer: 'C5 / S4 · Nov 2021 teaser for Paradigm CTF 2022—not the separate 2021 swap challenge · Author observation, not our replay' -->
<!-- STORY:13 -->

---

<div class="eyebrow">Different layers · Different evidence</div>

# Three meanings of “it looked the same”

| Appearance | Unjustified equivalence | Evidence to inspect |
|---|---|---|
| Similar rendering | Same data | Encoded predicate inputs |
| Compatible interface | Same implementation | Actual target and code |
| Verified source display | Correct artifact association | Artifacts and comparison rules |

<div class="claim">Familiar appearance encourages an identity assumption.</div>

<!-- _footer: 'S1, S2, S4 · Technical distinctions, not a measured psychological taxonomy' -->
<!-- STORY:14 -->

---

<div class="eyebrow">2023–2024 publications · Transfer conditions</div>

# “Approval For All”: follow the write

<div class="evidence">

![width:1050px](../docs/sources/s3-snapshot-write.png)

![width:1050px](../docs/sources/s3-transfer-condition.png)

</div>

**Owner-restricted write → either endpoint listed → require the flag**

<div class="small">Images: write and condition. Report prose: flag is fixed false.<br>Full-contract invariant and unique deployment identity remain unresolved.</div>

<!-- _footer: 'S3 · CertiK, Honeypot Scams, 11 January 2024 · Original report images; deployment attribution unresolved' -->
<!-- STORY:15 -->

---

<div class="eyebrow">Transfer conditions · Observation scope</div>

# A successful transaction is not a specification

| A comparison must identify | Why it matters |
|---|---|
| Account and entry point | Different predicates may apply |
| Relevant pre-state | Membership and flags can differ |
| Dependencies and execution context | Same source is not the same system |
| State effect—not only receipt status | Success does not prove the intended write |

<div class="claim">Different context can explain different results<br>without a broken simulator.</div>

<!-- _footer: 'S3, S6 + our analysis · Comparison dimensions, not a table of observed executions' -->
<!-- STORY:16 -->

---

<!-- _class: case-trace -->
<div class="eyebrow">CPIMP · Dedaub incident-response report, July 2025</div>

# Expected result. Unexpected implementation.

<div class="evidence">

![width:1050px](../docs/sources/p2-image-2-1024x211.jpg)

</div>

<div class="flow">
<div class="node">Proxy</div><span class="arrow">→</span>
<div class="node"><strong>Inserted layer</strong></div><span class="arrow">→</span>
<div class="node">Intended implementation</div>
</div>

<div class="small">Two D-CALL rows in the author’s normal-operation trace.<br>Normal functionality + misleading implementation display ≠ expected execution path.</div>

<!-- _footer: 'P2 · Ethereum tx 0x481a0d29… · KIP-associated bond example, not Kinto’s loss timeline · Published trace, not our replay' -->
<!-- STORY:17 -->

---

<!-- _class: compact -->
<div class="eyebrow">The execution facts that change the answer</div>

# Revisit the evidence—not the labels

| Case | Evidence boundary |
|---|---|
| Hidden state | Transaction status ≠ state postcondition |
| Private Bank | Displayed source / rounded value ≠ execution inputs |
| Storage reference | Initial value ≠ value after preceding writes |
| Homograph | Rendered string ≠ encoded data |
| Verification | Source display ≠ justified artifact association |
| Token restriction | Familiar name ≠ write/read behavior |
| CPIMP | Expected output ≠ expected implementation path |

**Old mechanisms persist. New workflows and combinations emerge.**

<!-- _footer: 'Our synthesis · Evidence levels remain distinct · No claim of a universal complexity ladder or complete history through 2027' -->
<!-- STORY:18 -->

---

<!-- _class: cover -->
<div class="eyebrow">When the hunter becomes the hunted</div>

# “I recognised the bug.”

## Did I identify the execution?

<div class="claim">Which execution fact would prove<br>my interpretation wrong?</div>

<!-- STORY:19 -->

---

<!-- _class: cover -->

# Questions

Which execution fact would prove my interpretation wrong?

<div class="small">Disobey 2027 · Public materials URL TBD</div>

<!-- STORY:20 -->

---

<!-- _class: refs -->

# References · historical mechanisms

**S1 · Torres, Steichen, State**
*The Art of The Scam: Demystifying Honeypots in Ethereum Smart Contracts.* USENIX Security 2019.
[Paper](https://www.usenix.org/system/files/sec19-torres.pdf) · Figures 6, 7, 9; §3.2.3; Appendix A.

**S2 · Ivanov et al.**
*Targeting the Weakest Link: Social Engineering Attacks in Ethereum Smart Contracts.* 2021.
[Paper](https://arxiv.org/abs/2105.00132) · §4.2.1 / Figure 5.

**S4 · samczsun**
*Hiding in Plain Sight.* 11 November 2021.
[Original write-up](https://www.paradigm.xyz/writing/hiding-in-plain-sight).

<!-- Untimed. The manuscript and docs/manifest.json contain evidence status and archive provenance. -->

---

<!-- _class: refs -->

# References · trading and verification research

**S3 · CertiK.** *Honeypot Scams.* 11 January 2024.
[Report](https://www.certik.com/blog/honeypot-scams) · Blacklist discussion and images reproduced on slide 15.

**S5 · Ma et al.** *Abusing the Ethereum Smart Contract Verification Services for Fun and Profit.* NDSS 2024.
[Paper](https://www.ndss-symposium.org/wp-content/uploads/2024-992-paper.pdf).

**S6 · Gan, Wang, Lin.** *Why Trick Me: The Honeypot Traps on Decentralized Exchanges.* DeFi Security workshop, 2023.
[Paper](https://arxiv.org/abs/2309.13501).

<!-- Untimed. S5 provides wider context, not independent evidence for S4's exact challenge. -->

---

<!-- _class: refs -->

# CPIMP · primary report and related presentation

**P2 · Dedaub team.** *The CPIMP Attack.* 15 July 2025.
[First-hand response report](https://dedaub.com/blog/the-cpimp-attack-an-insanely-far-reaching-vulnerability-successfully-mitigated/) · Source of slide 17’s trace image.

**P1 · Peter Kacherginsky.** [BlockThreat Week 28, 2025](https://newsletter.blockthreat.io/p/blockthreat-week-28-2025).
Secondary chronology; do not merge Kinto’s timeline with KIP’s trace.

**Владислав Азерский · Николай Микрюков**
*Горшочек, не вари! Истории про Web3-ловушки*
ZeroNights, late **2025** · [recording published 2026](https://www.youtube.com/watch?v=ghPxyaHqFHo).

<!-- Untimed. Event timing confirmed by the author/user. Publication metadata: 2026-04-10. -->

---

<!-- _class: refs -->

# Appendix · published deployment identifiers

**Gift 1 ETH** · S1 Appendix A
`0xd8993f49f372bb014fb088eabec95cfdc795cbf6`

**Private Bank** · S1 Appendix A
`0xd116d1349c1382b0b302086a4e4219ae4f8634ff`

**CryptoRoulette** · S1 Appendix A
`0x94602b0e2512ddad62a935763bf1277c973b2758`

**Retrieved:** explorer source/compiler metadata, creation and selected transaction pages.
**Still unresolved:** independent historical state/code validation and decisive early-case execution paths.

Dossiers and hashes: `docs/cases/` · `docs/case-materials-manifest.json`

<!-- Untimed. Do not substitute same-named contracts or interpret a paper model as byte-for-byte deployed source. -->

---

<!-- _class: refs records -->

# Appendix · Gift and Private Bank records

**Gift creation · 29 Oct 2017 · block 4453086**<br>
[`0xab8180c3eea86c9702daacb7fbe17368cfa9c313f90a6d341c72797bd738d7e3`](https://etherscan.io/tx/0xab8180c3eea86c9702daacb7fbe17368cfa9c313f90a6d341c72797bd738d7e3)

**Gift SetPass · 3 Nov 2017 · block 4484437 / position 13**<br>
[`0xa29c1875ef712b7b7c812bf2d1fa48e53ef56423a6882a55c51a1342880636da`](https://etherscan.io/tx/0xa29c1875ef712b7b7c812bf2d1fa48e53ef56423a6882a55c51a1342880636da)

**Bank creation · 12 Feb 2018 · block 5079695**<br>
[`0x1bd6347bc5c6e0b7af095863e4a2713df4ea932757d852b5a181de817d4bd096`](https://etherscan.io/tx/0x1bd6347bc5c6e0b7af095863e4a2713df4ea932757d852b5a181de817d4bd096)

**Bank deposit · 13 Feb 2018 · exact value 1.0000000623552385 ETH**<br>
[`0x46fd827bbc02ef0ac626c0f850458191c1b8c36cb9c5375194bafa9642f38124`](https://etherscan.io/tx/0x46fd827bbc02ef0ac626c0f850458191c1b8c36cb9c5375194bafa9642f38124)

**Later containing transaction · 15 Feb 2018 · explorer status Success**<br>
[`0x494a3fa918f12bb63e0de41474bc63e0c02137ae3ae1f3c58f63864c01fee537`](https://etherscan.io/tx/0x494a3fa918f12bb63e0de41474bc63e0c02137ae3ae1f3c58f63864c01fee537)

<!-- _footer: 'C1 / C2 · Archived explorer records—not independent RPC receipts, victim attribution or complete failure traces' -->
<!-- Untimed. Absolute dates, hashes and exact value checked against the case dossiers. -->

---

<!-- _class: refs records -->

# Appendix · CryptoRoulette and CPIMP records

**CryptoRoulette creation · 19 Feb 2018 · block 5118518**<br>
[`0xefa4e5dc40389240dbb4027db38b351041b75b488d2e0720ee9b05488f2240e1`](https://etherscan.io/tx/0xefa4e5dc40389240dbb4027db38b351041b75b488d2e0720ee9b05488f2240e1)

**Play · 20 Feb 2018 · block 5124620 · 0.1 ETH · status Success**<br>
[`0xc109a14f9588baf3e2a6189795e7a8a10b84a4c5a573effb988c1cc986c0a0d7`](https://etherscan.io/tx/0xc109a14f9588baf3e2a6189795e7a8a10b84a4c5a573effb988c1cc986c0a0d7)

**Reported destruction · 23 Feb 2018 · block 5144265**<br>
[`0xe40affc8f5d2482bcd2f55eef6d65dbb10346017c05ae785d46503c4f2187d37`](https://etherscan.io/tx/0xe40affc8f5d2482bcd2f55eef6d65dbb10346017c05ae785d46503c4f2187d37)

**CPIMP · Ethereum normal-operation trace cited by Dedaub**<br>
[`0x481a0d295102f50e6e6621d86167a09d7826de635bcd7e1b5623f6462f9a4b46`](https://app.blocksec.com/explorer/tx/eth/0x481a0d295102f50e6e6621d86167a09d7826de635bcd7e1b5623f6462f9a4b46)

<div class="small">A transaction reference is not proof of a payout, complete storage effect or victim intent.</div>

<!-- _footer: 'C3: explorer observations · P2: author-supplied trace · Separate evidence levels, not independent replays' -->
<!-- Untimed. Do not infer historical runtime from currently displayed code or state. -->
