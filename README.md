# UK Exec Pay Explorer

A Streamlit web app for exploring CEO compensation data from FTSE 100 annual remuneration reports.

---

## Problem statement

Reward analysts, journalists, and investors who want to examine UK executive pay currently face a poor set of options: buy an expensive ISS or Glass Lewis subscription, manually comb through dozens of PDF annual reports, or rely on incomplete press coverage. This tool pulls that data into one place and makes it explorable without specialist software or a data team.

---

## Screenshots

_Screenshots will be added after the first public deployment._

---

## Data sources

All figures are sourced manually from publicly available Directors' Remuneration Reports, which UK-listed companies are required to publish under the Companies Act 2006 (Schedule 8). Annual reports are freely downloadable from each company's investor relations page or from Companies House.

The five rows in `data/ceo_pay_2024.csv` are illustrative template figures used for development and testing. Replace them with verified figures from published reports before drawing or sharing conclusions.

---

## Methodology

**Total single figure** is calculated as:

```
base_salary_gbp
+ annual_bonus_gbp
+ ltip_vested_gbp
+ pension_benefits_gbp
+ other_gbp
= total_single_figure_gbp
```

This follows the single figure of total remuneration framework mandated by the Large and Medium-sized Companies and Groups (Accounts and Reports) Regulations 2008 (Schedule 8, as amended).

Key points:
- LTIP values reflect the market value of awards that vested during the financial year, using the year-end share price or the average price over the final quarter (per the company's stated methodology).
- Pension figures represent the value of company pension contributions or cash supplements in lieu.
- Pay ratios compare the CEO total single figure to median UK employee total pay, as disclosed in the remuneration report.
- All figures are in GBP and relate to the stated financial year end.

---

## Limitations

- Data entry is manual for this MVP. Each row requires reading and interpreting a remuneration report.
- This version covers a single financial year (2024) and a subset of the FTSE 100.
- Figures are not yet independently verified against source documents.
- The dataset does not currently cover the FTSE 250 or smaller listed companies.
- Comparability across companies is imperfect: LTIP vesting schedules, pension structures, and benefit valuations differ.

---

## Roadmap

- **PDF auto-extraction** - use a document AI pipeline to extract single-figure tables directly from annual report PDFs, reducing manual effort
- **Historical time series** - add multiple financial years to show pay trajectory over time
- **Peer group analysis** - allow users to define a custom comparator group and benchmark against it
- **Pay vs. performance regression** - plot total compensation against TSR, EPS, and revenue growth
- **FTSE 250 expansion** - extend coverage beyond the FTSE 100
- **Download to CSV** - let users export the filtered dataset

---

## Local setup

**Requirements:** Python 3.11+

```bash
# Clone the repo
git clone https://github.com/ghourigan123/UK-exec-pay-explorer.git
cd uk-exec-pay-explorer

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deployment - Streamlit Community Cloud

1. Push the repository to GitHub (ensure `data/ceo_pay_2024.csv` is committed).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select your repo, set the main file path to `app.py`, and click **Deploy**.
4. No additional secrets or environment variables are required for the CSV-backed MVP.

---

## Project structure

```
uk-exec-pay-explorer/
- app.py                      # Streamlit entry point (thin orchestration layer)
- requirements.txt
- README.md
- .gitignore
- .streamlit/
  - config.toml               # Custom theme
- data/
  - ceo_pay_2024.csv          # CEO pay data (manual entry)
- src/
  - data_loader.py            # load_data() with st.cache_data
  - transforms.py             # Filtering and percentage calculations
  - charts.py                 # Plotly chart functions
```

---

## Licence

MIT. Data is derived from publicly available regulatory filings - see each company's annual report for full attribution.
