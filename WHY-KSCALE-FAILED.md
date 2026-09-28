# Why K-Scale Labs failed: an evidence-based post-mortem
### And what Glappy should do differently

*Prepared for Russell Avre (Glappy Inc). Researched 2026-09-28 (US Central) from public sources only. I did not read the K-Scale Discord (the signed-in account has no access; see `../klabs/DISCORD-NOTES.md`).*

**How to read this**
- Every factual claim has an inline source link. **[unverified]** means the claim comes from a single secondary source, conflicts with another source, or could not be checked. **[my analysis]** marks my own interpretation, kept separate from what founders and press said.
- The single most useful primary source turned out to be K-Scale's own **65-page investor whitepaper** (PDF created 2025-11-04). After the shutdown, Ben Bolte linked it from `kscale.ai` with the caption "This is how K-Scale planned to make money" ([kscale.ai farewell page, Wayback 2026-01-29](https://web.archive.org/web/20260129051959/https://kscale.ai/)). It contains 12 months of cash flow, unit economics and the raw pre-order table. The PDF is here: [Wayback capture](https://web.archive.org/web/20251125215846/https://kscale.ai/whitepaper.pdf). I saved a copy to `artifacts/kscale-investor-whitepaper-2025-11-04.pdf`. It is a fundraising document, so its projections are optimistic by design. Its *historical* numbers (cash flow, orders) are the best public data available. Below it is cited as **"Whitepaper"**.
- Some figures below are my own arithmetic on Whitepaper tables. Those are labelled **[my arithmetic]**.

---

## Executive summary

1. **The stated reason is plain: K-Scale ran out of money and could not find a lead investor.** In his letter to customers, CEO Benjamin Bolte wrote that the company had "just a few months of runway" at launch. He said he "was able to raise a small amount of capital" but had "not been able to find a lead investor". Without funding for production tooling and certification, "the unit economics for our product do not make sense" ([full letter, Mike Kalil](https://mikekalil.com/blog/k-scale-labs-shuts-down/); [Humanoids Daily, 2025-11-04](https://www.humanoidsdaily.com/news/k-scale-labs-cancels-k-bot-orders-open-sources-all-ip-after-funding-fails)). Cash fell from $2.43M (Oct 2024) to $550K (Sep 2025) ([Whitepaper, Table 10](https://web.archive.org/web/20251125215846/https://kscale.ai/whitepaper.pdf)). The company was seeking a $25M raise (Whitepaper, "Capital Requirements").
2. **The founder names one strategic mistake as "probably number one": betting the company on the big $8,999 K-Bot instead of the cheap Z-Bot.** Bolte said a VC told him that 100 K-Bot pre-orders would unlock a $20M Series A. He "bet the farm on the K-Bot launch", and VCs stayed "too skeptical". He avoided leading with the Z-Bot because he feared looking like "a toy company" ([Humanoids Daily interview write-up, 2025-11-07](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch); [video](https://www.youtube.com/watch?v=k1fJgOYc2Tg)).
3. **Pre-orders looked like traction but brought in almost no cash.** K-Scale reported "130+ pre-orders representing $2M in booked order value" (Whitepaper, "Traction"). But deposits were only $100–$500 each (Whitepaper, Appendix C). By my sum of the raw table, roughly **$0.1M in cash was collected against ~$2.15M of bookings** [my arithmetic]. The Founder's Edition base price of $8,999 was **below K-Scale's own estimated all-in Gen 1 cost of $9,850** (Whitepaper, Table 2) [my analysis].
4. **Execution, scope and team problems made the cash run out faster.** The former COO says the team got "stuck on locomotion" and that timelines were "a running joke". He says there was no supply chain when he joined, and describes the GitHub as "full of repos… motion without convergence" ([Rui Xu, The Robot Report, 2026-03-02](https://www.therobotreport.com/6-lessons-learned-watching-a-robotics-startup-die-from-the-inside/)). The public footprint supports the scope problem: 118 original repos, and five named robot products advertised within about four months (K-Bot, Z-Bot, M-Bot, then K-Bot Air and K-Bot Mini). Co-founders left before the end.
5. **Competing on price against China while also funding US production was the structural problem.** Bolte's letter contrasts K-Scale with Unitree, Booster, EngineAI and Noetix, which financed tooling at scale ([letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/)). He later said the robot was machined in China because US CNC shops refused the parts ([Optim/Shack15 talk notes, 2026](https://www.optim.vc/a-conversation-with-ben-bolte-on-the-state-of-humanoid-robotics-hardware-intelligence-and-where-the-opportunity-lives/)). Open source did not cause the failure. But on the founder's own account, the open model could not be monetised before the cash ran out ("Android kind of only came out after the iPhone. So maybe it's a bit early", [Humanoids Daily](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch)).

**Overall confidence: medium-high.** The core cause (no lead investor, burn above revenue, expensive product) is stated by the CEO and confirmed by the company's own financials. The relative weight of the secondary causes (scope, team, open-source model) is my judgement, built mainly on the COO's account and public artifacts.

---

## 1. Timeline

| When (US Central) | Event | Source |
|---|---|---|
| Late 2023 | Bolte, unemployed in New York, starts experimenting with cheap actuators and applies to YC **[secondary]** | [Chain of Thought essay (based on a Bolte interview)](https://agents.chainofthought.xyz/p/k-scale-the-team-that-tried-to-beat-tesla) |
| Winter 2024 | **YC W24 confirmed.** YC lists founders Benjamin Bolte and Matthew Freed as "Former Founders", team size 10, status **Inactive** | [YC company page](https://www.ycombinator.com/companies/k-scale-labs) |
| Early 2024 | "Stompy" 3D-printed humanoid, BOM under $10k, five hardware iterations in three months; standing and waving by YC Demo Day | [YC page](https://www.ycombinator.com/companies/k-scale-labs); [Launch HN](https://news.ycombinator.com/item?id=44456904) |
| 2024-04-03 | $500K pre-seed (Crunchbase: Lombardstreet Ventures "and 2 other investors"; Preqin: Lombardstreet and YC) | [Crunchbase](https://www.crunchbase.com/organization/k-scale-labs); [Preqin](https://www.preqin.com/data/profile/asset/k-scale-labs/639430) |
| 2024-08-31 | Zeroth-01 (the small bot) built in 24 hours at a K-Scale hackathon by Jingxiang Mo, Kelsey Pool and Denys Bezmenov | [Hackster](https://www.hackster.io/news/why-not-build-this-bot-5fea87487349); see `../klabs/HUMANOID-RESEARCH.md` §1.2 |
| Nov 2024 | Website lists 11 team members (including COO Rui). Backers named: Fellows Fund, GFT Ventures, Lombardstreet, Ninja Capital, YC, AI Grant, Pioneer Fund | [kscale.dev, Wayback 2024-11-09](https://web.archive.org/web/20241109035543/https://kscale.dev/) |
| Aug 2024 – Feb 2025 | "6 generations of robots in less than a year": Stompy Mini (Aug 2024), K-Bot v0.1 and Zeroth Bot (Nov 2024), Z-Bot (Jan 2025, "used in CS courses at Stanford"), K-Bot (Feb 2025) | [kscale.dev, Wayback 2025-09-12](https://web.archive.org/web/20250912064906/https://www.kscale.dev/) |
| Jan 2025 | Zeroth Bot Kickstarter **pre-launch** page with paid Facebook ads ("Launching Soon on Kickstarter"). The Kickstarter project is still in "submitted"/pre-launch state today, so it **never launched** | [Wayback 2025-01-25](https://web.archive.org/web/20250125181339/https://pre-launch.grandjourney.ai/?campaign_id=120221636441070339&ad_id=120221646180110339&utm_id=120221636441070339); [Kickstarter page](https://www.kickstarter.com/projects/zerothbot/zeroth-bot-the-programmable-humanoid-robot) (page metadata `project_state: submitted`, checked 2026-09-28) |
| Feb–Apr 2025 | First K-Bot pre-orders appear in the raw order table | Whitepaper, Appendix C, Table 17 |
| 2025-05-18/19 | Soft launch on HN (142 points). Fellows Fund partner posts that Fellows "proudly led their seed round" | [HN](https://news.ycombinator.com/item?id=44023680); [LinkedIn (Alex Ren)](https://www.linkedin.com/posts/alexchengmingren_we-first-met-benjamin-bolte-and-his-incredible-activity-7330353825679134720-nW0W) (post date decoded from ID: 2025-05-19) |
| May 2025 | Reported: Sam Altman pre-ordered a K-Bot, and a nonprofit he co-founded donated $250K **[secondary]** | [Humanoids Daily, 2025-05-20](https://www.humanoidsdaily.com/news/k-scale-labs-betting-on-open-source-for-the-future-of-humanoid-robotics) |
| Jun 2025 | Website shows three products: **K-Bot from $8,999** (struck-through $15,999), **Z-Bot from $999** ($1,999), **M-Bot from $2,999** ($3,999). Z-Bot and M-Bot are "Sign up for updates" only | [kscale.dev, Wayback 2025-06-08](https://web.archive.org/web/20250608221251/https://www.kscale.dev/) |
| 2025-06-11 / 06-16 | Taotao (Tao Motor) US subsidiary RevEdge Inc. agrees to invest **$2M**. Tao Motor signs a strategic ODM (contract design and manufacturing) deal to localise US mass production | [Taotao investor Q&A via Stockstar, 2025-06-19](https://stock.stockstar.com/IG2025061900004550.shtml) (Chinese) |
| 2025-07-01 | K-Bot pre-orders open publicly (X post). Launch HN on 07-03 (233 points) | [X post via HN](https://news.ycombinator.com/item?id=44438003); [Launch HN](https://news.ycombinator.com/item?id=44456904) |
| Aug 2025 | K-Bot page: list price $16,000, "$10,999 second batch pricing", "Ships December 2025". FAQ: "We expect to ship the first robots to customers by November 2025". "Full Autonomy" roadmap runs to **Jun 2028** | [kscale.dev/kbot, Wayback 2025-08-01](https://web.archive.org/web/20250801200120/https://www.kscale.dev/kbot) |
| Aug 2025 | Investor page claims "the best-selling humanoid robot in America" | [kscale.dev/investors, Wayback 2025-08-09](https://web.archive.org/web/20250809182341/https://www.kscale.dev/investors) |
| Aug 2025 | Taotao says it completed small-batch trial production of some K-Scale robot products; mass production "depends on market feedback" **[secondary]** | [bs178 / Guandian, 2025-09-02](https://www.bs178.com/s-1-390197a32414927b/) (Chinese) |
| Sep 2025 | Co-founding engineer Jingxiang Mo leaves (announced 2025-10-20) and starts a new venture | [Mike Kalil](https://mikekalil.com/blog/k-scale-labs-shuts-down/); [LinkedIn](https://www.linkedin.com/posts/jingxiangmo_in-september-i-decided-to-leave-k-scale-activity-7386090919592173569-LjVV) |
| 2025-09-24 | **First K-Bot Founder's Edition delivered.** Second batch "sold out" and new orders paused | [Humanoids Daily, 2025-09-26](https://www.humanoidsdaily.com/news/k-scale-labs-delivers-first-k-bot-humanoid-sells-out-second-batch) |
| 2025-09-30 | Cash balance **$550.0K** | Whitepaper, Table 10 |
| Oct 2025 | Website nav now lists **K-Bot, K-Bot Air, K-Bot Mini**. Whitepaper claims "5 robots in customer hands (October 2025)" | [kscale.dev, Wayback 2025-10-02](https://web.archive.org/web/20251002053407/https://www.kscale.dev/); Whitepaper, "Traction" |
| Before 2025-11-04 | K-Scale explored a sale to **1X and The Bot Co.** (headline only; article paywalled) **[details unverified]** | [The Information (headline)](https://www.theinformation.com/briefings/exclusive-humanoid-robotics-startup-k-scale-shut-exploring-sale-1x-bot-co) |
| **2025-11-04** | **Shutdown letter to pre-order customers:** orders cancelled, deposits refunded, "most of the team" laid off, "less than a month of runway", all IP to be released | [Humanoids Daily](https://www.humanoidsdaily.com/news/k-scale-labs-cancels-k-bot-orders-open-sources-all-ip-after-funding-fails); [full text](https://mikekalil.com/blog/k-scale-labs-shuts-down/) |
| 2025-11-05/06 | Mo's **Gradient Robots** emerges: "inherited the K-Scale spirit, mission, and core engineering team", "the open-source Unitree for America", pre-seed closed in September | [Mike Kalil](https://mikekalil.com/blog/gradient-robots-k-scale/) |
| 2025-11-07 | Bolte's post-mortem interview ("I bet the farm on the K-Bot launch") | [Humanoids Daily](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch) |
| Jan 2026 | `kscale.dev` redirects to `kscale.ai`, which hosts Bolte's farewell note "To my fellow builders" with links to GitHub and the whitepaper | [kscale.dev redirect, Wayback 2026-01-19](https://web.archive.org/web/20260119022321/https://kscale.dev/); [kscale.ai, Wayback 2026-01-29](https://web.archive.org/web/20260129051959/https://kscale.ai/) |
| 2026-03-02 | Former COO Rui Xu publishes "6 lessons I learned watching a robotics startup die from the inside" | [The Robot Report](https://www.therobotreport.com/6-lessons-learned-watching-a-robotics-startup-die-from-the-inside/) |
| 2026-03-07/08 | Bolte joins OpenAI | [Humanoids Daily, 2026-03-08](https://www.humanoidsdaily.com/news/openai-hardware-leader-caitlin-kalinowski-resigns-over-pentagon-deal-as-benjamin-bolte-joins) |
| 2026-04-03 | Rui Xu reported hired to lead hardware at Meta Superintelligence Labs (after Dreamer) | [Business Insider](https://www.businessinsider.com/meta-superintelligence-labs-taps-leader-for-hardware-role-2026-4) |
| 2026-09-28 | kscale.dev and docs.kscale.dev fail DNS. The GitHub repos and Discord survive | `../klabs/HUMANOID-RESEARCH.md` §0 |

### Promised vs actual delivery
| Promise | Actual |
|---|---|
| First K-Bots "by November 2025" ([FAQ, Aug 2025](https://web.archive.org/web/20250801200120/https://www.kscale.dev/kbot)) | First unit delivered 2025-09-24, **ahead of promise** ([Humanoids Daily](https://www.humanoidsdaily.com/news/k-scale-labs-delivers-first-k-bot-humanoid-sells-out-second-batch)). Units delivered in total: **conflicting**. "At least two" and "only two" per [Kalil](https://mikekalil.com/blog/gradient-robots-k-scale/); "5 robots in customer hands (October 2025)" per the Whitepaper **[unverified which is right]** |
| Second batch "Ships December 2025" at $10,999 | Cancelled and refunded 2025-11-04 |
| Z-Bot $999 ([site, Jun 2025](https://web.archive.org/web/20250608221251/https://www.kscale.dev/)) and a Kickstarter "launching soon" (Jan 2025) | Kickstarter never launched ([Kickstarter](https://www.kickstarter.com/projects/zerothbot/zeroth-bot-the-programmable-humanoid-robot)). I found no evidence of a commercial Z-Bot shipping. (Humanoids Daily wrote that Z-Bot "launched via Kickstarter in early 2025" ([source](https://www.humanoidsdaily.com/news/k-scale-labs-betting-on-open-source-for-the-future-of-humanoid-robotics)); the Kickstarter page itself contradicts that.) |
| M-Bot "later this year" ([Launch HN](https://news.ycombinator.com/item?id=44456904)); K-Bot Air/Mini (nav, Oct 2025) | Never shipped |
| Gen 2 roadmap: EVT Nov 15 2025, DVT Dec 15 2025, Amazon FBA launch Apr 1 2026, "Full Autonomy" Jun 2028 | Company closed before EVT (Whitepaper, Table 11) |

---

## 2. The numbers

### Funding (sourced figures only)
| Round | Amount | Investors | Source / confidence |
|---|---|---|---|
| Pre-seed, 2024-04-03 | $500K | Lombardstreet Ventures, YC, + others | [Crunchbase](https://www.crunchbase.com/organization/k-scale-labs), [Preqin](https://www.preqin.com/data/profile/asset/k-scale-labs/639430). Good |
| Seed | ~$4M at a ~$50M valuation | Led by Fellows Fund (lead confirmed by [Fellows partner post](https://www.linkedin.com/posts/alexchengmingren_we-first-met-benjamin-bolte-and-his-incredible-activity-7330353825679134720-nW0W)). Bolte's thank-you in that post lists YC, AI Grant, Fellows Fund, GFT Ventures, Lombardstreet Ventures, Ninja Capital | **Amount and valuation [secondary]**: [36Kr](https://eu.36kr.com/en/p/3558501366315912), [Failory](https://newsletter.failory.com/p/the-open-source-robot). The **date conflicts**: 36Kr says Feb 2025, but the Whitepaper cash table shows no multi-million inflow between Oct 2024 and Sep 2025 (Feb 2025 cash-in: $43.1K). The seed money was probably already in the bank before Oct 2024 [my analysis] |
| Add-on | $250K | Nat Friedman and Daniel Gross | **[secondary]**: [36Kr](https://eu.36kr.com/en/p/3558501366315912). Business Insider separately confirms Friedman invested "through the AI Grant program" ([BI](https://www.businessinsider.com/meta-superintelligence-labs-taps-leader-for-hardware-role-2026-4)) |
| Strategic, June 2025 | $2M (agreed) | RevEdge Inc. (Taotao subsidiary) | [Taotao Q&A](https://stock.stockstar.com/IG2025061900004550.shtml). Good. Note: Whitepaper cash-in for June 2025 is only $776.1K, so the $2M may have arrived in tranches or only partly **[unverified]** |
| Series A (sought) | $10–15M ([36Kr](https://eu.36kr.com/en/p/3558501366315912), secondary); **$25M** per the Whitepaper | No lead found | Whitepaper "Capital Requirements"; [letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/) |

### Cash burn (primary: Whitepaper, Table 10)
- Ending balance: **$2.43M (Oct 2024) → $1.13M (Feb 2025) → $625.7K (Apr 2025) → $1.24M (Jun 2025, after the Taotao money) → $550.0K (Sep 2025)**.
- Over those 12 months: **cash out ≈ $3.28M, cash in ≈ $1.31M, average outflow ≈ $273K/month** [my arithmetic on Table 10]. The biggest month was Feb 2025 at $591.5K out.
- At the shutdown: "less than a month of runway" ([letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/)). About **$400K** left in the account **[secondary]** ([36Kr](https://eu.36kr.com/en/p/3558501366315912), [Failory](https://newsletter.failory.com/p/the-open-source-robot)). That is consistent with the Sep 2025 $550K balance.
- A Chain of Thought essay quotes "$164,000 per month" ([source](https://agents.chainofthought.xyz/p/k-scale-the-team-that-tried-to-beat-tesla)). That does not match the Table 10 average. Its "$3+ million outflows vs $1.3M inflows" does match.

### Product pricing and unit economics (primary: Whitepaper, Tables 1–2, 6–7)
| Item | Gen 1 (current K-Bot) | Gen 2 (planned) |
|---|---|---|
| BOM (Bill of Materials) with CNC-machined structure | **$10,430** | — |
| BOM assuming forged structure | $7,130 | $3,830 |
| Tariffs (13% of FOB, i.e. factory price before shipping) | $1,064 | $572 |
| All-in COGS (Cost of Goods Sold, incl. contract-manufacturer margin, freight, Amazon fees) | **$9,850** | $5,473 |
| Target MSRP (list price) | $16,000 | $8,000 |
| Stated gross margin | 38.4% | 31.6% |

- Actual Founder's Edition price: **$8,999** for the first 100 ([RS DesignSpark](https://www.rs-online.com/designspark/k-scale-labs-launches-k-bot-americas-first-open-source-humanoid-robot); [Launch HN](https://news.ycombinator.com/item?id=44456904)). That is **below the $9,850 all-in Gen 1 COGS and far below the $10,430 CNC BOM**. On base hardware alone, each Founder's Edition robot lost money by K-Scale's own numbers [my analysis]. Many buyers added options. Full packages in the raw table total about $16.5K–$18.5K (Whitepaper, Table 17). One of those options, "Full Autonomy", promised free hardware and software upgrades until the robot is fully autonomous ([Launch HN](https://news.ycombinator.com/item?id=44456904)), with a roadmap running to June 2028. That is a multi-year obligation sold for a one-time fee [my analysis].
- The monetisation plan: hardware near commodity margins, profit from aftermarket parts (40–62.5% margin) and a $200/month software subscription at ~93.5% margin (Whitepaper, "Software and AI", Table 7).
- A secondary report says only about 10 K-Bot prototypes were built, "each costing over $100,000" **[unverified; 36Kr only]** ([36Kr](https://eu.36kr.com/en/p/3558501366315912)). The COO gives a concrete cost-control example: without mature supplier relationships, "whether unit cost lands at $800 or $2,400" ([Rui Xu](https://www.therobotreport.com/6-lessons-learned-watching-a-robotics-startup-die-from-the-inside/)).
- Certification alone (UL, FCC, batteries) was budgeted at **$130K–$300K** for a US-only baseline (Whitepaper, Table 4). None of it had been done.

### Pre-orders (primary: Whitepaper "Traction" and Appendix C)
- K-Scale's headline: "130+ pre-orders representing $2M in booked order value… with no marketing spend".
- Deposits: "initially starting at $100 before being raised to $500". (Kalil reports "$200 deposits" ([source](https://mikekalil.com/blog/gradient-robots-k-scale/)), which conflicts.)
- My parse of the raw table: ~150 order rows, ~157 robots, ~$2.15M total order value, **~$102K actually paid** [my arithmetic; approximate, because the PDF table is hard to parse].
- Order dates by month (row count): Feb–Apr 3, May 33, **Jul 102**, Aug 11, Sep 1 [my arithmetic]. Demand spiked at launch, then fell. Part of the drop may be because the second batch "sold out" and orders were paused ([Humanoids Daily](https://www.humanoidsdaily.com/news/k-scale-labs-delivers-first-k-bot-humanoid-sells-out-second-batch)).
- Who bought: US excluding the Bay Area 66.7%, Bay Area 18.7%, the rest in England, Japan, Canada and elsewhere (Whitepaper, Figure 3). The buyer list is dominated by engineers, founders, researchers and a few universities (Table 17).
- 36Kr reports "over 100 pre-orders… exceeding $2 million", including one from OpenAI's robotics head ([36Kr](https://eu.36kr.com/en/p/3558501366315912)). Failory calls it "$2M+ in deposits" ([Failory](https://newsletter.failory.com/p/the-open-source-robot)), which is **wrong** by the company's own data: $2M was bookings, not deposits.

### Headcount
- About 10 people: YC lists team size 10 ([YC](https://www.ycombinator.com/companies/k-scale-labs)); 11 names were on the site in Nov 2024 ([Wayback](https://web.archive.org/web/20241109035543/https://kscale.dev/)); "only about 10 engineers" covering the whole stack **[secondary]** ([36Kr](https://eu.36kr.com/en/p/3558501366315912)).
- The plan was to grow to 14 people in 2026 with a $2.85M payroll (Whitepaper, Table 13).
- At the end: "had to lay off most of the team" ([letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/)).

---

## 3. What the founders and press said (stated reasons, in their words)

**Ben Bolte, CEO (shutdown letter, 2025-11-04)** ([full text](https://mikekalil.com/blog/k-scale-labs-shuts-down/))
- "K-Scale is a seed-stage company that has been operating on a lean budget since our inception – at the time of our launch, we had just a few months of runway in the bank."
- He hoped "to use the demonstrated interest to raise additional funding to finance the required tooling for high-volume production and obtain mass-market regulatory approvals, as well as hire additional engineers. Without being able to finance and amortize these costs, as companies like Unitree, Booster, Engine AI and Noetix have done, the unit economics for our product do not make sense."
- "My view… was predicated on my confidence that American capital markets would be deeper than Chinese capital markets… However, while I was able to raise a small amount of capital, I have not been able to find a lead investor."

**Ben Bolte (interview, 2025-11-07)** ([Humanoids Daily write-up](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch); [video](https://www.youtube.com/watch?v=k1fJgOYc2Tg). I could not pull the video transcript, so quotes come via Humanoids Daily.)
- A VC said that launching K-Bot and getting 100 pre-orders would "no problem" unlock a $20M Series A. "I kind of had bet the farm on the the Kbot launch."
- "That just didn't work for VCs… a lot of the VCs I talked to were just too skeptical." The K-Bot go-to-market needed a redesign for "die casting or cold forging" to make the unit economics work.
- "I think if we had done the Zbot first… we could probably have gotten quite a few more orders because it's much cheaper." He didn't because he "wanted to be like a serious humanoid company" and not "a toy company".
- "Major missteps… that was probably number one… I was overindexing on how easy I thought it would be to get funding."
- On open source: "Android kind of only came out after the iPhone. So maybe it's a bit early."

**Rui Xu, former COO** ([The Robot Report, 2026-03-02](https://www.therobotreport.com/6-lessons-learned-watching-a-robotics-startup-die-from-the-inside/); [his blog](https://ruixu.us/posts/my-time-at-k-scale))
- "We never closed our Series A."
- "Large Model Chauvinism": a long internal debate over whether to add mechanical end stops to joints, because "the AI policy should learn the joint limits".
- "When I joined, there was nothing. No manufacturer relationships, no payment terms, no QC process, no logistics pipeline."
- "The single biggest mistake I saw was getting stuck on locomotion… the fundraising window closed… The GitHub was full of repos… motion without convergence."
- "Our timelines were a running joke. It was always the robot walks next week."
- "Should have been firmer earlier about the organizational problems." On X he also wrote: "No blame to our investors… There were just some behind-the-scenes reasons that made K-Scale a hard bet" ([via Kalil](https://mikekalil.com/blog/gradient-robots-k-scale/)). **What those reasons were is not public.**
- On the culture: fourteen-day sprints with goals "we never actually hit", and a "10–3–7" schedule ([ruixu.us](https://ruixu.us/posts/my-time-at-k-scale)). Bolte confirmed staff were "living in the closets" and working "10:00 a.m. to 3:00 a.m." ([Humanoids Daily](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch)).

**Press and commentators (interpretation, not primary evidence)**
- 36Kr: the Z-Bot → K-Bot switch was the turning point, and the US lacks small-batch factories willing to share risk with startups ([36Kr A](https://eu.36kr.com/en/p/3558501366315912), [36Kr B](https://eu.36kr.com/en/p/3559984314980485)).
- Chain of Thought: "$1M in low-margin hardware revenue likely anchored investor expectations to hardware economics", and "open source is a long-term advantage, not a go-to-market strategy" ([essay](https://agents.chainofthought.xyz/p/k-scale-the-team-that-tried-to-beat-tesla)).
- Failory: "Hardware burn with software expectations" and "open source isn't a business model" ([Failory](https://newsletter.failory.com/p/the-open-source-robot)). Caution: Failory has factual errors. It says "founded 2023", "~$15,000" price, and cash "down to $400,000" by "October 2024", which the Whitepaper contradicts.

---

## 4. Root causes, tested one by one

Verdict scale: **Supported** (primary evidence), **Partly supported**, **Not supported / minor**, **Unknown**.

| # | Hypothesis | Verdict | Evidence | Analysis |
|---|---|---|---|---|
| 1 | **Fundraising failure / no lead investor** | **Supported (proximate cause)** | [Letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/); Whitepaper Table 10; the $25M ask | This is what actually ended the company. Everything below explains *why* the raise failed and why the runway was so short. |
| 2 | **Burn rate vs hardware margins** | **Supported** | ~$273K/month average outflow vs ~$109K/month average inflow [my arithmetic]; the $8,999 base price sits below the $9,850 estimated COGS; tooling and certification unfunded | Selling each unit below cost means more orders only raise the capital requirement. The model only worked after a large raise paid for forging tooling. That is a classic hardware trap. |
| 3 | **Strategy: big K-Bot before cheap Z-Bot** | **Supported (founder's own #1)** | [Interview](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch); the Z-Bot Kickstarter never launched; zeroth-bot is the most-starred original repo (832★) (`REPO-INVENTORY.csv`) | Demand for the cheap bot is suggested but not proven. Stars are not sales, and Z-Bot's $999 price and margins were never tested in market. |
| 4 | **Pre-order / delivery delays** | **Partly supported, but not in the usual way** | First delivery came *before* the promised date; the second batch was cancelled | Deliveries were not the problem. The problem was that the pre-orders funded almost nothing (~5% cash vs bookings [my arithmetic]) while adding refund liability and support load. |
| 5 | **Fundraising climate vs well-funded rivals (Figure, Unitree, 1X, Tesla)** | **Supported (founder-stated)** | [Letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/) names Chinese rivals that financed production; Unitree G1 at ~$16,000 and Unitree pursuing an IPO ([Kalil](https://mikekalil.com/blog/k-scale-labs-shuts-down/)); the top 10 robotics firms took >40% of 2025 funding per Crunchbase **[secondary via 36Kr]** ([36Kr](https://eu.36kr.com/en/p/3558501366315912)) | For K-Scale, the relevant competitors were Chinese vendors on price (a "cost-competitive American humanoid" was the pitch), not Figure or Tesla. Investors could buy exposure to US humanoids through much better-funded leaders. |
| 6 | **Open-source business model / monetisation** | **Partly supported (contributing, not decisive)** | The plan relied on a $200/month subscription and aftermarket parts, none of it yet built (Whitepaper); Bolte: "maybe it's a bit early"; open source helped Tao build the robot "in less than three weeks" (Whitepaper §2.4.4) | Open source *helped* supply-chain partnerships and community (4,100+ Discord members, see `../klabs/HUMANOID-RESEARCH.md`). It also left no moat to show investors while hardware lost money [my analysis; Chain of Thought makes the same argument]. There is no direct evidence an investor declined *because* of open source; Rui Xu's "behind-the-scenes reasons" are unspecified. |
| 7 | **Supply chain / tariffs** | **Partly supported** | Bolte on launch: "tariffs have made it difficult to rely on Chinese suppliers" ([Launch HN](https://news.ycombinator.com/item?id=44456904)); tariffs = $1,064/unit (Whitepaper, Table 2); US CNC shops "refused" to machine the parts ([Optim notes](https://www.optim.vc/a-conversation-with-ben-bolte-on-the-state-of-humanoid-robotics-hardware-intelligence-and-where-the-opportunity-lives/)); COO: supply chain built from zero ([Rui Xu](https://www.therobotreport.com/6-lessons-learned-watching-a-robotics-startup-die-from-the-inside/)) | Tariffs were ~11% of the $9,850 Gen 1 all-in cost ($1,064; 13% of factory price per the whitepaper); they were a headwind, not the killer. The deeper issue was the lack of a mature manufacturing capability. The Texas assembly deal with Tao (see §6) was a smart hedge, but it arrived only months before the money ran out. |
| 8 | **Scope: too many products and repos** | **Supported (contributing)** | 118 original repos: 70 created in 2025, 98 of them with fewer than 10 stars (`REPO-INVENTORY.csv`). Own Rust OS, DSL (Klang), telemetry format (kRec), VLA model, sim framework ([site, Feb 2025](https://web.archive.org/web/20250206161558/https://www.kscale.dev/)). Products: K-Bot, Z-Bot, M-Bot ([Jun 2025](https://web.archive.org/web/20250608221251/https://www.kscale.dev/)), then K-Bot Air and K-Bot Mini ([Oct 2025](https://web.archive.org/web/20251002053407/https://www.kscale.dev/)). Bolte: "we got a bit nerd-sniped… trying to build most of our stack ourselves" ([Launch HN](https://news.ycombinator.com/item?id=44456904)) | For a ~10-person team, owning OS, sim, ML, firmware, mechanical, five products and certification is too much. The COO's "motion without convergence" is the insider's version of this. |
| 9 | **Customer segment (developers/research vs consumer)** | **Partly supported** | Buyers were technical early adopters (Whitepaper, Table 17). Bolte: "I don't know that there are many applications today which humanoids are the best form factor to solve… first real use cases will mostly be entertainment" ([Launch HN](https://news.ycombinator.com/item?id=44456904)). Yet the marketing asked if a robot could "load the dishwasher?" and "fold my laundry?" ([site, Feb 2025](https://web.archive.org/web/20250206161558/https://www.kscale.dev/)) and called K-Bot your "first personal robot" ([K-Bot page, Aug 2025](https://web.archive.org/web/20250801200120/https://www.kscale.dev/kbot)) | The dev/research segment was real but small and one-off. K-Scale's own pre-order curve peaked in the launch month. The consumer promise ("Full Autonomy" to 2028) created obligations the segment couldn't fund [my analysis]. |
| 10 | **Team issues** | **Partly supported** | The COO's "organizational problems" and "Schrödinger's expertise" ([Rui Xu](https://www.therobotreport.com/6-lessons-learned-watching-a-robotics-startup-die-from-the-inside/)). Co-founder departures: Mo in Sep 2025 ([Kalil](https://mikekalil.com/blog/k-scale-labs-shuts-down/)); Budzianowski reportedly left in May 2025 **[unverified; search snippet of his LinkedIn]** and now co-founds Lute ([Lute LinkedIn](https://www.linkedin.com/company/lutecompany)); Freed is listed as a "Former Founder" (date unknown) ([YC](https://www.ycombinator.com/companies/k-scale-labs)). Extreme hours culture ([Humanoids Daily](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch)) | Losing two of three technical co-founders in the final six months, one of whom left with the "core engineering team" ([Kalil](https://mikekalil.com/blog/gradient-robots-k-scale/)), made a rescue raise or acqui-hire harder. Details of internal conflicts are **not public**. |
| 11 | **Technical execution (locomotion, reliability)** | **Supported (insider account)** | "Stuck on locomotion" ([Rui Xu](https://www.therobotreport.com/6-lessons-learned-watching-a-robotics-startup-die-from-the-inside/)); docs say wiring "is still the least reliable part of the robot" (`../klabs/HUMANOID-RESEARCH.md` §1.1) | Slow convergence burned calendar time during the funding window. |

**Bottom line [my analysis]:** K-Scale did not die because the robot didn't work. It walked, it shipped (a few units), and people ordered it. It died because the business plan needed a big raise *before* the hardware could make money, and the company made itself dependent on that raise. The key moves were pricing below cost, taking small deposits, owning an enormous scope with ten people, and pivoting to the most capital-hungry product in order to impress investors. When the raise failed, there was no fallback revenue line.

---

## 5. What the community and customers said

- **Refunds:** the letter promised to return deposits ("I want to make sure we have sufficient capital to return your deposit") ([letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/)). Six Degrees of Robotics says Bolte "announced on Discord that pre-orders would be refunded" **[secondary; this outlet has other factual errors]** ([source](https://sixdegreesofrobotics.com/robot-news/k-scale-labs-shuts-down-amid-fierce-global-price-war)). **I found no public report either confirming that all refunds were paid or complaining that they weren't [unverified].** Deposits were small ($100–$500), which limited the exposure.
- **Reaction:** AI educator Harrison Kinsley (@Sentdex) posted the letter: "I thought all the VCs were excited about US-based robotics, what happen?" ([via Kalil](https://mikekalil.com/blog/k-scale-labs-shuts-down/)). A robotics operator replied publicly that "It hasn't shut down. There's some other news baking" ([Humanoids Daily](https://www.humanoidsdaily.com/news/k-scale-labs-cancels-k-bot-orders-open-sources-all-ip-after-funding-fails)). The "news" appears to have been Gradient Robots [my inference].
- **Community sentiment afterwards:** on HN in Sep 2026, a former community member wrote they were "sad to see it shut down due to the competition with low-cost chinese robots" ([HN comment](https://news.ycombinator.com/item?id=49525480)). Third-party builders still document "the post-K-Scale-shutdown state of the ecosystem" ([Justin-Riekehof/zeroth-01-build](https://github.com/Justin-Riekehof/zeroth-01-build)).
- **Customers who received K-Bots:** I found no public statements from the 2–5 owners about support after the shutdown **[unknown]**.
- **Reddit:** threads exist, e.g. [r/robotics "K-Scale Labs – New Podcast Episode – Your Questions"](https://www.reddit.com/r/robotics/comments/1onps97/kscale_labs_new_podcast_episode_your_questions/), but Reddit blocked my fetches, so I have **not read them**.
- **Discord:** still live with ~4,131 members; the Zeroth Discord has ~1,555 (`../klabs/HUMANOID-RESEARCH.md` §0). Announcements could not be read.

---

## 6. What survived

- **The IP, publicly.** The letter released "all of K-Scale's proprietary IP, including the hardware and software for the K-Bot and Zeroth Bot projects" ([letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/)). GitHub has 146 public repos (133 kscalelabs + 12 zeroth-robotics + 1 community), including 27 forks. These are archived in Software Heritage, and the docs, BOMs and CAD links are preserved (see `PRESERVATION-STATUS.md`). The websites are gone; the Discord and the Onshape CAD remain.
- **Successor company:** **Gradient Robots/Robotics**, founded by co-founding engineer Jingxiang Mo. It launched claiming K-Scale's "core engineering team" and the "open-source Unitree for America" mission ([Kalil](https://mikekalil.com/blog/gradient-robots-k-scale/)). It has since repositioned as "the robot workforce for the data center buildout" ([South Park Commons](https://www.southparkcommons.com/companies/gradient-robotics/); [gradientrobotics.ai](https://gradientrobotics.ai/)). It went from a general-purpose open humanoid to a paying enterprise vertical, which is itself a lesson.
- **Founders and executives:** Bolte joined OpenAI (Mar 2026) and says he'll keep supporting open-source humanoid projects ([Humanoids Daily](https://www.humanoidsdaily.com/news/openai-hardware-leader-caitlin-kalinowski-resigns-over-pentagon-deal-as-benjamin-bolte-joins)). Rui Xu went to Dreamer, then Meta Superintelligence Labs ([BI](https://www.businessinsider.com/meta-superintelligence-labs-taps-leader-for-hardware-role-2026-4)). Paweł Budzianowski co-founded Lute, a Warsaw/Redwood City mobile-manipulation robotics company ([Lute](https://www.linkedin.com/company/lutecompany)).
- **Acquisition:** K-Scale explored a sale to 1X and The Bot Co. ([The Information headline](https://www.theinformation.com/briefings/exclusive-humanoid-robotics-startup-k-scale-shut-exploring-sale-1x-bot-co)). A secondary outlet says both wanted only "a handful of engineers" **[unverified]** ([Six Degrees](https://sixdegreesofrobotics.com/robot-news/k-scale-labs-shuts-down-amid-fierce-global-price-war)). **I found no evidence of any asset or IP acquisition.**
- **Tao Motor / Texas manufacturing:** Tao reached out after the reference design was published. Its US arm (Denago) built K-Bots "in less than three weeks" in a former Dallas newspaper printing plant (Whitepaper §2.4.4; [Chain of Thought](https://agents.chainofthought.xyz/p/k-scale-the-team-that-tried-to-beat-tesla) for the Dallas detail **[secondary]**; Bolte confirmed Tao "bought a big factory in Texas" on [Launch HN](https://news.ycombinator.com/item?id=44456904)). **Whether Tao still has any K-Bot tooling or intends to make them is unknown.** This matters for you in Texas: it may be a local contract-manufacturing lead worth a phone call [my suggestion].

---

## 7. Comparable cases (brief, sourced)

- **Aldebaran (Nao/Pepper), France:** served education and research. It filed for bankruptcy in Feb 2025, went into receivership in June, and Maxvision bought its core assets in July 2025 ([The Robot Report](https://www.therobotreport.com/maxvision-buys-core-robot-assets-including-nao-pepper-aldebaran/)). Its owner, United Robotics Group, had declined to keep funding it ([The Robot Report](https://www.therobotreport.com/rethink-robotics-shuts-down-again/)). Lesson: even a leader in education humanoids, with ~20,000 Nao units sold, couldn't survive without a sustainable funder.
- **Embodied (Moxie), USA:** an $800 kids' companion robot. It closed in Dec 2024 when a lead investor "withdrew" at the last minute. Robots were bricked because core functions needed the cloud, and most buyers got no refunds ([Ars Technica](https://arstechnica.com/gadgets/2024/12/startup-will-brick-800-emotional-support-robot-for-kids-without-refunds/)). Lesson for a kids' product: don't make the device depend on your servers, and don't rely on one lead investor.
- **Rethink Robotics:** raised $150M and went bankrupt in 2018. It was relaunched in 2024 and shut down again in Sep 2025 after "products weren't ready" and investors pulled funding ([The Robot Report](https://www.therobotreport.com/rethink-robotics-shuts-down-again/)).
- **3D Robotics (cited by K-Scale itself):** open-source drone maker that built up inventory, lost to DJI and pivoted to software (Whitepaper §2.2). K-Scale knew this story and still ran out of cash, for different reasons.

---

## 8. Lessons for Russell and Glappy

*Everything in this section is my recommendation [my analysis], grounded in the evidence above. It is not legal or financial advice.*

### 8.1 Which segment to start in
**Start in K-12 education and hobby/after-school programs, with a services-first mix. Do not start with humanoid hardware for developers or research labs.**
- The evidence favours cheap, small robots. The cheapest K-Scale bot has the most community traction (zeroth-bot: 832★ vs kbot: 393★ in `REPO-INVENTORY.csv`). The founder says Z-Bot-first would have sold more ([interview](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch)). And small, low-voltage robots are safe around kids, unlike a 34–37 kg, 48 V K-Bot (`../klabs/HUMANOID-RESEARCH.md` §4.3).
- You already have the unfair advantages K-Scale lacked: you teach kids and you run an IT/AI services company, so you know the buyer and can generate cash now.
- Texas has structured demand. UIL runs official state robotics championships in BEST, FIRST and VEX/RECF divisions ([UIL Robotics](https://www.uiltexas.org/academics/stem/robotics)). Schools buy through cooperatives such as BuyBoard, where vendors must respond to a proposal invitation and be awarded a contract ([BuyBoard vendor registration](https://www.buyboard.com/vendor/how-to-register)). Target these channels for curriculum and kit sales.
- **Avoid for now:** research-lab humanoids (small market, high support cost, competing with Unitree on price) and consumer "home robot" promises (K-Scale's "Full Autonomy" roadmap is a cautionary example).

### 8.2 Hardware vs software/services revenue mix
- **Year 1 target: most revenue from services** (classes, camps, teacher training, school program contracts, custom AI/robotics integration through Glappy). **Hardware is a small, margin-positive add-on.** K-Scale planned to profit from software "later", which never came (Whitepaper §3.8).
- **Never price hardware below fully loaded cost.** Include BOM, yield loss, labour, freight, tariffs, payment fees, returns and support. K-Scale's $8,999 sat below its own $9,850 COGS. Set a floor (e.g. ≥40–50% gross margin on kits) and only discount from there.
- **Sell recurring things schools already budget for:** curriculum licences, per-seat subscriptions, replacement-parts packs, PD (teacher professional-development) days, competition coaching. These are the "aftermarket" K-Scale hoped for, in a market that already buys them.

### 8.3 Pre-order discipline
- **Take pre-orders only for a product whose unit cost you have measured on a pilot batch** (e.g. 10–25 units built by you or a contract manufacturer), not from a spreadsheet.
- **Deposits should cover real cost.** Either 30–50% down with a firm ship date, or full pre-payment with an escrowed refund reserve. K-Scale collected ~5% of bookings in cash [my arithmetic], so its pre-orders proved interest but funded nothing.
- **Keep a refund reserve in a separate account equal to all deposits held.** K-Scale's letter shows the last cash went to refunds.
- **Don't sell multi-year promises for a one-time fee** (like "free upgrades until full autonomy"). If a feature doesn't exist, don't take money for it.
- **Don't launch several products at once.** Ship one, get paid, support it, then add the next.

### 8.4 Open-source strategy
- **Open-source the parts that grow adoption; charge for what saves schools time.** Good candidates to open: lesson plans, sample code, printable parts. Keep paid: packaged curriculum, teacher dashboard, support, certified kits, training.
- **Pick your own license on purpose.** A strongly reciprocal hardware license (CERN-OHL-S) obliges anyone who sells products based on your design to publish their complete source. That protects the commons, but it also applies to you if you build on CERN-OHL-S designs. A permissive license (MIT) lets others, including low-cost manufacturers, copy freely.
- **Open source is not a business model by itself.** Both the founder ("maybe it's a bit early") and critics ([Chain of Thought](https://agents.chainofthought.xyz/p/k-scale-the-team-that-tried-to-beat-tesla)) point to this. Decide your paid product before you publish.

### 8.5 Capital needs
- **Design Glappy Robotics to be default-alive on services revenue.** K-Scale's ~$273K/month average outflow was far beyond its ~$109K/month average inflow [my arithmetic], and one failed raise killed it. Rule of thumb: keep at least 12 months of fixed costs in the bank, and never plan a product that can't ship without a raise that hasn't closed.
- **Budget certification from day one if you sell electronics to schools.** K-Scale estimated $130K–$300K for UL/FCC/battery certification of a full humanoid (Whitepaper, Table 4). A small kit built from already-certified modules (pre-certified radio modules, off-the-shelf chargers and batteries) cuts this drastically. Confirm with a test lab before committing.
- **Use non-dilutive funding and customer money first:** school contracts, grants, teacher-training funding, local manufacturing partners. Raise equity only for a proven, repeatable product.
- **Avoid dependence on one investor or one "if you get X, we'll give you Y" promise.** Both K-Scale and Embodied died when a lead investor didn't come through or backed out ([interview](https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch); [Ars Technica](https://arstechnica.com/gadgets/2024/12/startup-will-brick-800-emotional-support-robot-for-kids-without-refunds/)).

### 8.6 Using the preserved K-Scale designs legally
The licensing is **inconsistent**, so **check every repo and file before reuse, and get a lawyer's sign-off before selling anything based on it.**
- **The shutdown letter** says hardware is under CERN-OHL-S-2.0 and software under MIT, and calls these "non-commercial licenses" ([letter](https://mikekalil.com/blog/k-scale-labs-shuts-down/)). Neither CERN-OHL-S nor MIT is a non-commercial license; both permit commercial use under their conditions (see the license texts: [kbot LICENSE-HW (CERN-OHL-S v2)](https://github.com/kscalelabs/kbot/blob/master/LICENSE-HW), [kbot LICENSE (MIT)](https://github.com/kscalelabs/kbot/blob/master/LICENSE)). **Treat the letter's wording as ambiguous, not as a grant.**
- **The kbot README** says hardware is `CERN-OHL-S` and software `GPL v3` "unless otherwise specified". But the repo's `LICENSE` file is **MIT** and `LICENSE-HW` is CERN-OHL-S v2 ([kbot README](https://github.com/kscalelabs/kbot)). **GPLv3 vs MIT is a real conflict for software you would ship.** Assume the stricter reading (GPL v3) unless a lawyer says otherwise.
- **Of 118 original repos, 75 are MIT, 1 is Apache-2.0 (kteleop) and 42 have no license detected** (`REPO-INVENTORY.csv`). That includes important ones: `kscalelabs/docs` (BOMs, assembly PDFs), `kscalelabs/kos-zbot` and `zeroth-robotics/hardware`. **No license means no permission granted.** Opting out of open-source licenses "doesn't mean you're opting out of copyright law" ([choosealicense.com](https://choosealicense.com/no-permission/)). Don't copy files from those repos into a product.
- **Zeroth-bot** is MIT ([README](https://github.com/zeroth-robotics/zeroth-bot)), but it pulls in submodules and CAD hosted elsewhere (Onshape, Google Docs) whose terms may differ. Check each one.
- **Practical path:**
  1. Use K-Scale designs for learning, teaching and internal prototypes (lowest risk).
  2. For anything you sell, design your own parts inspired by what you learn, or use only files whose license is clearly permissive.
  3. Keep attribution (copyright notice plus license text) in your docs, packaging and repos.
  4. If you use CERN-OHL-S hardware, publish your modified design sources as that license requires.
  5. Keep a per-file log of source URL, license and commit hash.

### 8.7 First 12 months: what to do differently
| Month | Do this | Instead of what K-Scale did |
|---|---|---|
| 0–1 | Write a one-page plan with **one** product, **one** customer (a K-8 or high-school robotics program in Texas) and **one** paid offer (e.g. a 10-week class or club package). Set a cash floor that triggers cuts | Five robot SKUs and 118 repos |
| 0–2 | Build 3–5 Zeroth-class bots **for your own classes** from the preserved docs (see `../klabs/HUMANOID-RESEARCH.md` §4). Log real cost per unit and failure rates | Selling a robot before its cost was known |
| 1–3 | Run paid pilots with 2–3 schools or programs through Glappy. Charge for teaching and support, not just hardware | Relying on an investor's "get 100 orders" promise |
| 2–4 | Price a kit at ≥40–50% gross margin on fully loaded cost. Take pre-orders only with 30–50% deposits and a dated ship window you can hit | $8,999 base price below the $9,850 COGS; $100–$500 deposits |
| 3–6 | Use only pre-certified electronics modules; get a quote from a test lab early; design for kids' safety (low voltage, end stops, pinch guards) | End stops debated away; certification unfunded |
| 3–6 | Pick your own license, and do a per-file license audit of anything reused from K-Scale | Contradictory license statements |
| 4–8 | Line up one Texas contract manufacturer or print farm for small batches (Tao/Denago in Dallas is one lead to ask about) and one backup | Supply chain built from zero, late |
| 6–9 | Apply to be a BuyBoard vendor when a relevant proposal opens; align the curriculum with UIL-sanctioned competitions | No school purchasing channel |
| 6–12 | Add recurring revenue: curriculum subscription, parts packs, teacher training. Keep the device fully functional offline | Planned subscription never built; Moxie-style cloud dependence |
| Every month | Keep ≥12 months of fixed costs in the bank. Review burn vs revenue. Ship something paying customers use | ~$273K/month burn with no fallback revenue |
| 9–12 | Only now consider a second product (e.g. a larger bot) or outside capital, backed by real repeat customers | Pivoting to the hardest product to impress VCs |

---

## 9. Things I could not verify, and conflicts

- **Seed round amount, valuation and date** ($4M at $50M): secondary sources only, and the date conflicts with the Whitepaper cash table.
- **The Nat Friedman / Daniel Gross $250K** and the **Taotao $2M actually received**: the June 2025 cash-in was only $776K.
- **Units delivered:** 2 (Kalil) vs 5 (Whitepaper).
- **Deposit size:** $200 (Kalil) vs $100 then $500 (Whitepaper).
- **Whether all refunds were paid:** no public confirmation or complaints found.
- **"~10 prototypes at >$100K each"** (36Kr only).
- **Why 1X / The Bot Co. did not buy:** The Information is paywalled; the secondary account is unverified.
- **Rui Xu's "behind-the-scenes reasons":** never specified publicly.
- **Co-founder departure dates:** Budzianowski (May 2025 per a LinkedIn search snippet) and Matthew Freed (unknown).
- **Discord announcements and Reddit threads:** not readable from here.
- **The Bolte interview video:** YouTube blocked transcript download, so quotes are via Humanoids Daily's write-up.
- **I found no TechCrunch coverage** of the shutdown in my searches. That does not prove there was none.

---

## 10. Source list

**Primary (company and founders)**
- K-Scale investor whitepaper (PDF, created 2025-11-04): https://web.archive.org/web/20251125215846/https://kscale.ai/whitepaper.pdf (local copy: `artifacts/kscale-investor-whitepaper-2025-11-04.pdf`)
- Bolte shutdown letter (full text): https://mikekalil.com/blog/k-scale-labs-shuts-down/
- kscale.ai farewell page: https://web.archive.org/web/20260129051959/https://kscale.ai/
- Launch HN (Bolte as `codekansas`): https://news.ycombinator.com/item?id=44456904
- YC company page: https://www.ycombinator.com/companies/k-scale-labs
- Rui Xu, The Robot Report: https://www.therobotreport.com/6-lessons-learned-watching-a-robotics-startup-die-from-the-inside/ and https://ruixu.us/posts/my-time-at-k-scale
- Bolte interview write-up: https://www.humanoidsdaily.com/news/watch-k-scale-labs-ceo-explains-shutdown-i-bet-the-farm-on-the-k-bot-launch (video: https://www.youtube.com/watch?v=k1fJgOYc2Tg)
- Bolte Shack15 talk notes: https://www.optim.vc/a-conversation-with-ben-bolte-on-the-state-of-humanoid-robotics-hardware-intelligence-and-where-the-opportunity-lives/
- Taotao investor Q&A: https://stock.stockstar.com/IG2025061900004550.shtml
- Wayback captures of kscale.dev: 2024-11-09, 2025-02-06, 2025-06-08, 2025-08-01 (/kbot), 2025-08-09 (/investors), 2025-09-12, 2025-10-02, 2025-10-06 (/why), 2026-01-19 (links inline above)
- GitHub: https://github.com/kscalelabs, https://github.com/zeroth-robotics (see `REPO-INVENTORY.csv`)

**Press and secondary**
- Humanoids Daily: shutdown https://www.humanoidsdaily.com/news/k-scale-labs-cancels-k-bot-orders-open-sources-all-ip-after-funding-fails · first delivery https://www.humanoidsdaily.com/news/k-scale-labs-delivers-first-k-bot-humanoid-sells-out-second-batch · May 2025 profile https://www.humanoidsdaily.com/news/k-scale-labs-betting-on-open-source-for-the-future-of-humanoid-robotics · Bolte to OpenAI https://www.humanoidsdaily.com/news/openai-hardware-leader-caitlin-kalinowski-resigns-over-pentagon-deal-as-benjamin-bolte-joins
- Mike Kalil: https://mikekalil.com/blog/gradient-robots-k-scale/
- The Information (headline only): https://www.theinformation.com/briefings/exclusive-humanoid-robotics-startup-k-scale-shut-exploring-sale-1x-bot-co
- Business Insider: https://www.businessinsider.com/meta-superintelligence-labs-taps-leader-for-hardware-role-2026-4
- 36Kr: https://eu.36kr.com/en/p/3558501366315912 and https://eu.36kr.com/en/p/3559984314980485
- Chain of Thought: https://agents.chainofthought.xyz/p/k-scale-the-team-that-tried-to-beat-tesla
- Failory (contains errors): https://newsletter.failory.com/p/the-open-source-robot
- Six Degrees of Robotics (contains errors): https://sixdegreesofrobotics.com/robot-news/k-scale-labs-shuts-down-amid-fierce-global-price-war
- Crunchbase: https://www.crunchbase.com/organization/k-scale-labs · Preqin: https://www.preqin.com/data/profile/asset/k-scale-labs/639430
- Gradient Robotics: https://www.southparkcommons.com/companies/gradient-robotics/ · https://gradientrobotics.ai/
- Comparables: https://www.therobotreport.com/maxvision-buys-core-robot-assets-including-nao-pepper-aldebaran/ · https://www.therobotreport.com/rethink-robotics-shuts-down-again/ · https://arstechnica.com/gadgets/2024/12/startup-will-brick-800-emotional-support-robot-for-kids-without-refunds/
- Texas channels: https://www.uiltexas.org/academics/stem/robotics · https://www.buyboard.com/vendor/how-to-register
