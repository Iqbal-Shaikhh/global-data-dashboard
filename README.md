# 🌍 Global Socio-Economic & Microfinance Dashboard

An interactive, data-driven web application built with **Streamlit** and **Python** to explore macroeconomic indicators, socio-economic correlations, and the technological landscape impacting global microfinance.

This dashboard transforms raw United Nations and Kiva datasets into actionable, visual insights, complete with an automated PDF reporting engine.

## ✨ Features

* 📈 **Socio-Economic Correlations:** Discover how variables like government expenditure on health and education correlate with GDP growth and life expectancy. Features interactive scatter plots with OLS trendlines and a dynamic correlation heatmap.
* 📱 **Microfinance Technology Impact:** Explore the relationship between digital infrastructure (internet/mobile penetration) and key microfinance targets (like agricultural employment and unemployment rates).
* ⚖️ **Side-by-Side Country Comparison:** Select any two countries to instantly compare key metrics via data tables and interactive Radar (Spider) charts breaking down their economic structure (Agriculture vs. Industry vs. Services).
* 📄 **Automated PDF Reports:** Generate and download beautifully styled, multi-page PDF reports containing the interactive charts seamlessly converted to high-resolution images.

## 🛠️ Tech Stack

* **Frontend & Framework:** [Streamlit](https://streamlit.io/)
* **Data Manipulation:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
* **Data Visualization:** [Plotly Express & Graph Objects](https://plotly.com/python/)
* **Statistical Analysis:** [Statsmodels](https://www.statsmodels.org/)
* **PDF Generation:** [FPDF2](https://pyfpdf.github.io/fpdf2/)
* **Image Export Engine:** [Kaleido](https://github.com/plotly/Kaleido) & Chromium

## 📂 Project Structure

```text
global-data-dashboard/
│
├── app.py                            # Main Streamlit application
├── report_generator.py               # FPDF2 class for custom PDF styling
├── requirements.txt                  # Python library dependencies
├── packages.txt                      # Linux system dependencies (Chromium)
├── country_profile_variables.csv     # UN Country Statistics dataset
├── kiva_country_profile_variables.csv# Kiva regional macro-dataset
└── README.md                         # Project documentation

```

## 💻 Local Installation & Usage

To run this dashboard on your local machine:

**1. Clone the repository or download the files:**
Ensure all project files are located in the same directory.

**2. Create a virtual environment (Recommended):**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

**3. Install dependencies:**

```bash
pip install -r requirements.txt

```

**4. Run the application:**

```bash
streamlit run app.py

```

*The app will automatically open in your default web browser at `http://localhost:8501`.*

## ☁️ Deployment on Streamlit Community Cloud

This app is optimized for seamless deployment on Streamlit Community Cloud.

**Important Note on PDF Generation:**
Because this app converts interactive Plotly charts into static PNGs for the PDF report, the server requires a headless web browser.

* **`packages.txt`**: This file contains the word `chromium`. Streamlit Cloud reads this and automatically installs the required browser engine before booting the app.
* **`requirements.txt`**: Contains `kaleido`, which acts as the bridge between Plotly and Chromium to snap the pictures.

**Deployment Steps:**

1. Upload all project files to a public GitHub repository.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app** and select your repository, branch (`main`), and main file path (`app.py`).
4. Click **Deploy!**

## 📊 Data Sources

* **UN Country Profiles:** Comprehensive macroeconomic and demographic indicators.
* **Kiva Profiles:** Regional data tailored toward assessing microfinance landscapes.
*(Missing values in the raw CSVs encoded as `-99` are automatically handled and cleaned by the app's data loader).*
