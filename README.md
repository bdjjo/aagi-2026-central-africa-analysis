# AAGI Central Africa 2026 - Reproducible Analysis

An evidence-constrained audit and analysis of the supplied **Africa AI
Governance Index (AAGI) 2026 Central Africa Regional Data Collection Report**
and its associated data-collection workbook. The analysis covers the six
countries in the report's page-2 comparative summary: **Cameroon, Gabon, the
Democratic Republic of Congo (DRC), the Republic of Congo, Chad, and the
Central African Republic (CAR).**

> **Research question.** Across these six Central African countries, where does
> reported AI-governance capacity concentrate, and where is the largest gap
> between stated policy and demonstrable delivery?

**➡️ Findings at a glance:** see [`FINDINGS.md`](FINDINGS.md) for all nine charts,
or the live page once GitHub Pages is enabled (see *Publish the display page*
below).

## Key finding (one line)

All six countries score below the index's **Established** composite threshold of
3.0; the region's strongest average pillar is *Strategy and Vision* (~1.53/4)
and its weakest is *Implementation and Impact* (~0.57/4), an implementation
gap, not an absence of policy. *(Report p. 2; descriptive.)*

---

## Scope and the most important limitation

This repository uses **only the two supplied source files**. Two facts govern
everything downstream and are repeated in every figure caption and article:

1. **Comparative scores come from the report's page-2 summary table**, not from
   an indicator-level panel. The report presents composites as *approximate* (~)
   and rounds pillar scores to one decimal.
2. **The supplied workbook is a partially completed country template.** It
   contains **8 populated indicator rows out of 80**. The first four indicators
   of P1 (S1.1–S1.4) and P2 (G2.1–G2.4). It therefore **cannot reproduce** the
   report's six-country results. Workbook figures audit *completeness only*.

The report's own methodology states that a score of **0 means "no findable
primary evidence,"** not proof that no activity exists. The workbook's Scoring
Guide defines 0 more strongly as "no policy, institution, programme, or activity
exists." These are different claims; the analysis treats low scores as evidence
signals, not verdicts. See [`docs/methodology_and_limitations.md`](docs/methodology_and_limitations.md).

---

## Repository structure

```text
AAGI-central-africa-2026/
├── README.md
├── LICENSE                 # MIT — applies to code
├── LICENSE-DATA            # CC BY 4.0 — data, figures, docs; AAGI terms for raw
├── CITATION.cff
├── requirements.txt
├── .gitignore
├── code/
│   ├── aagi_analysis.py            # regenerates processed data + all 9 figures
│   ├── audit_workbook.py           # structural audit of the workbook
│   └── verify_composites.py        # checks composite reproducibility
├── notebooks/
│   └── 01_aagi_reproduction.ipynb  # narrated walk-through of the analysis
├── data/
│   ├── raw/                        # supplied source files, unchanged
│   └── processed/                  # generated CSV exports + audit JSON
├── figures/
│   ├── png/                        # 9 charts (raster)
│   └── svg/                        # 9 charts (vector)
├── docs/
│   ├── methodology_and_limitations.md
│   └── data_dictionary.md
└── articles/
    ├── medium_article.md
    ├── linkedin_posts.md
    └── executive_summary_and_headline_stats.md
```

## Reproduce the analysis

Requires Python 3.11+.

```bash
# 1. (optional) create an isolated environment
python3 -m venv .venv && source .venv/bin/activate

# 2. install dependencies
pip install -r requirements.txt

# 3. regenerate all processed data and figures
python3 code/aagi_analysis.py

# 4. (optional) run the supporting audits
python3 code/audit_workbook.py
python3 code/verify_composites.py
```

All paths are resolved relative to the repository root, so the scripts run from
a fresh clone with no path edits, provided the two source files are present in
`data/raw/`.

## What each output shows

| Figure | Takeaway |
|---|---|
| `01_composite_ranking` | Six composites span CAR 0.2 to a three-country cluster at ~1.5; all below 3.0. |
| `02_pillar_heatmap` | Country profiles differ by pillar, not just by a single average. |
| `03_mean_pillars` | Strategy and governance highest on average; implementation lowest. |
| `04_pillar_spread` | Strategy and regional integration vary most across countries. |
| `05_tier_pillar_comparison` | The lower tier (Chad, CAR) lags most on infrastructure, innovation, implementation. |
| `06_score_distribution` | Most of the 48 country–pillar cells sit between 0 and 2. |
| `07_workbook_completion` | Only 8 of 80 workbook indicator rows are populated. |
| `08_strategy_vs_implementation` | High strategy scores do not translate directly into implementation. |
| `09_six_country_pillar_comparison` | Full pillar profile for all six countries against the 3.0 threshold. |

## Reproducibility notes

- **Composites.** Reported composites reproduce as the unweighted 8-pillar mean
  within ±0.05 for every country **except Gabon** (displayed pillars imply
  ~1.375–1.40 versus a reported ~1.5). This is consistent with the report using
  unrounded underlying scores; the supplied files do not fully resolve it. Run
  `verify_composites.py` to see the reconstruction.
- **Provenance flag.** The workbook filename references the Central African
  Republic, but its only populated sheet (P1) identifies Cameroon. This is
  recorded, not corrected, in the raw file.
- **Descriptive only.** Correlations use n = 6 and are not inferential.

## Suggested future data release

To make the index fully reproducible, a future release should include the six
completed country workbooks (or a normalised indicator-level file), unrounded
scores, the exact composite formula, evidence dates, explicit missingness flags,
and a field that separates *governance status* from *evidence status*.

## Publish the display page (GitHub Pages)

This repository ships a self-contained landing page (`index.html`) plus a
`.nojekyll` marker so GitHub serves the `figures/` folder verbatim. After pushing
the repo, enable Pages in **Settings → Pages → Build and deployment → Source:
Deploy from a branch → Branch: `main` / `/ (root)`**. Within a minute the site is
live at `https://<username>.github.io/<repo-name>/`, showing the executive
summary, headline statistics, and all nine figures. No build step is required.

## Citation

See [`CITATION.cff`](CITATION.cff). Suggested short form:

> Bainamndi, D. J. (2026). *AAGI Central Africa 2026 — Reproducible Analysis.*
> Africa AI Governance Index, Central Africa Chapter.
