# Bond Butterfly: 2–5–10 Year Yield Curve Analysis

This project analyzes how a bond butterfly responds to changes in the French yield curve. It combines a Python script, an Excel model and a chart of published reference rates.

## Strategy

The portfolio buys theoretical 2-year and 10-year bonds and sells a theoretical 5-year bond. The quantities are calculated so that the initial net value and sensitivity to a small parallel rate movement (net PVBP) are zero. The analysis then focuses on changes in the **shape** of the yield curve.

## Data and tools

The starting yields are the French CNO-TEC rates published on 24 September 2026: **3.594% (2 years), 4.049% (5 years) and 4.669% (10 years)**. These are reference rates; the bond coupons and positions are modelling assumptions.

- **Python:** prices the bonds, calculates duration and PVBP, determines the position sizes and runs yield-shock scenarios.
- **Excel:** displays the inputs, formulas, neutrality checks and scenario results for review.
- **Chart:** compares the published 2-, 5- and 10-year rates on 23 and 24 September 2026.

## Main finding

The position has little first-order exposure to a small parallel rate shift, but remains exposed to changes in slope and curvature. Among the scenarios tested, the curvature shock produces the largest modelled loss. The results are **scenario changes in value, not realised profits or a trading recommendation**.

## Files

- `butterfly_rates.py` — Python code
- `Butterfly_Taux_Sofia_Kammoune.xlsx` — Excel model
- `courbe_TEC_23_24_septembre_2026.png` — yield curve chart
- `Presentation_Projet_Butterfly_Sofia_Kammoune.pdf` — two-page presentation
- `resultats_scenarios.csv` — scenario output

Run the code with `python butterfly_rates.py`.

**Data source:** [Banque de France — Bond indices, 24 September 2026](https://www.banque-france.fr/fr/statistiques/taux-et-cours/indices-obligataires-2026-09-24).
