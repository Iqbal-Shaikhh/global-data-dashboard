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

*The app will automatically open in your default web browser at 'http://localhost:8501'.*

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


### 1. The Core Infrastructure

* **Streamlit Framework:** We used Streamlit to handle the entire frontend. It creates the webpage, the sidebar navigation, and the layout without needing to write any HTML or CSS.
* **Smart Data Loading:** We used the `@st.cache_data` decorator. This means the app only reads and cleans the heavy CSV files once when it boots up, making the dashboard lightning-fast as the user clicks around.
* **Automated Data Cleaning:** We wrote logic to instantly find all the `-99` values (which represent missing data in the UN datasets) and convert them to `NaN` so they don't ruin your statistical calculations.

### 2. Three Interactive Modules

We split the app into three distinct "pages" using a sidebar menu to answer your specific research questions:

* **Socio-Economic Correlations:** Allows users to pick specific health/education metrics and plot them against GDP. We added an OLS (Ordinary Least Squares) trendline to show statistical relationships, and a beautifully styled Red-to-Blue **Correlation Heatmap** to show how all macro-indicators interact at once.
* **Microfinance Impact:** Focuses on the Kiva dataset, allowing users to see how technological infrastructure (like internet and mobile access) correlates with regional employment metrics—key indicators for microfinance success.
* **Country Comparison:** A tool that lets a user select any two countries from a dropdown. It instantly pulls their data, builds a side-by-side comparison table, and generates an interactive **Radar (Spider) Chart** to visualize the shape of their economies (Agriculture vs. Industry vs. Services).

### 3. Professional Visual Styling

Instead of default charts, we upgraded the visuals to impress your professors:

* We used `template="plotly_white"` to remove the ugly gray backgrounds.
* We applied professional color palettes (`px.colors.qualitative.Bold` and `Prism`) to easily distinguish different global regions.
* We thickened the markers and trendlines so they look sharp and authoritative.

### 4. The PDF Export Engine

This is the most advanced feature of the app. We built a bridge between the interactive web frontend and a static PDF generator:

* When the user clicks **"Generate PDF Report"**, the app uses the `Kaleido` engine (powered by the hidden Chromium browser we set up) to take high-resolution "screenshots" of your live Plotly charts.
* It passes those images, along with the current data state, to your custom `report_generator.py` script.
* That script dynamically builds a styled PDF with headers, footers, and alternating-color data tables, then hands it back to the web app for the user to download.

**In short:** You started with raw, messy tabular data and ended up with an interactive, beautifully styled, statistically rigorous application that can automatically write its own reports!
