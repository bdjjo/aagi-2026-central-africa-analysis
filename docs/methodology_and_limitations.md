# Methodology and limitations

## 1. Evidence rule

This analysis uses **only** the two supplied files:

- `AAGI_2026_CentralAfrica_Bainamndi.docx`  The AAGI 2026 Central Africa
  Regional Data Collection Report (comparative scores transcribed from its
  page-2 summary).
- `CopyofAAGI_Data_Collection_centralafricarepublic.xlsx`  The supplied,
  partially completed data-collection workbook.

No external scores or country facts are introduced into the dataset. Report
citations use page numbers; workbook citations use sheet names and row ranges.
(Where the *accompanying articles* add outside context for example continental
policy milestones, that context is explicitly labelled as external and cited
separately. It is never merged into the dataset.)

## 2. The index

The report assesses eight pillars, ten indicators each (80 indicators), on a
0–4 scale:

| Score | Meaning |
|---:|---|
| 0 | No evidence |
| 1 | Nascent |
| 2 | Developing |
| 3 | Established |
| 4 | Advanced |

Stated pillar weights: 15% each for P1 Strategy, P2 Governance, P3
Infrastructure, and P4 Human Capital; 10% each for P5 Innovation, P6 Ethics,
P7 Regional Integration, and P8 Implementation. The **Established** composite
threshold is 3.0.

## 3. The zero-score problem

The report methodology states that a 0 reflects the **absence of findable
primary evidence**, not necessarily the absence of activity. The workbook's
Scoring Guide defines 0 more strongly ("no policy, institution, programme, or
activity exists"). These are not equivalent. Throughout this analysis and the
accompanying articles, low scores are read as **evidence signals**, and the
distinction between *governance status* and *evidence status* is preserved.

## 4. Why comparative analysis uses the report, not the workbook

The workbook is the intended collection instrument, but the supplied copy holds
only 8 populated indicator rows of 80 (S1.1–S1.4 on P1; G2.1–G2.4 on P2), all
for Cameroon. It cannot map the report's 48 country–pillar summary cells (or its
480 country–indicator scores) to source rows. Comparative figures therefore use
the report's page-2 table; workbook figures report completeness only.

## 5. Known reproducibility caveats

1. **Rounding.** Displayed pillar scores are one-decimal; composites are marked
   approximate. Reconstructed composites match the reported values within ±0.05
   for all countries **except Gabon**, where the displayed pillars imply
   ~1.375–1.40 against a reported ~1.5. Most consistent explanation: the report
   computed composites from unrounded underlying scores. The supplied files do
   not resolve this; `code/verify_composites.py` documents the gap.
2. **Provenance.** The workbook filename references CAR while its populated P1
   sheet identifies Cameroon; P2–P8 retain `[Enter]` placeholders. Recorded, not
   corrected.
3. **Small n.** All cross-country statistics use n = 6 and are descriptive. The
   Spearman associations (for example, innovation–implementation ρ ≈ 0.99) are
   reported for pattern description only; they are not inferential and may
   reflect shared evidence across pillars.
4. **No panel data.** The report is a single 2026 cross-section. No trends,
   causal effects, incident rates, investment figures, or public-opinion
   measures can be derived from the supplied material.

## 6. Scope note: six countries, not the full region

This repository's scope is fixed to the **six countries on report page 2**.
Central Africa is variously defined; the Economic Community of Central African
States (ECCAS) has eleven members. Any broader country set (for example, an
extended chapter build covering additional states such as Angola, Burundi,
Equatorial Guinea, São Tomé and Príncipe, or the Indian-Ocean states) is a
**separate dataset with different composites and a different regional mean** and
must not be compared cell-for-cell with the figures here. Keep the two scopes
clearly labelled in any downstream use.

## 7. Regional-facts flag (Malabo Convention)

The report's page-2 summary treats Malabo Convention status as a differentiator
and, for these six countries, describes Gabon, Chad, and the Republic of Congo
as ratifiers and Cameroon, the DRC, and CAR as signed-but-not-ratified. That
count is specific to this six-country subset and to the report's cut-off; it is
**not** the continental total and should not be generalised. When articles cite
continental ratification totals, those come from external sources and are
labelled as such.

## 8. What would strengthen the next release

Completed country workbooks or a normalised indicator-level file; unrounded
scores and the exact composite formula; evidence dates per indicator; explicit
missingness flags; a separate evidence-availability field; and an inter-rater
reliability check across fellows.
