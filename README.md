# 📊 Start-Up Investment Analysis Dashboard

An interactive dashboard and exploratory data analysis (EDA) tool built with Python and Streamlit for analyzing start-up funding trends across industries, countries, and years.

## 🚀 Features

- 🧼 **Data Cleaning**: Cleans messy funding amounts (like "17,50,000") and inconsistent date formats.
- 📊 **EDA**: Identifies top industries, countries, and funding trends.
- 🧠 **Interactive Filters**: Country, industry, year, and funding amount filters.
- 📈 **Streamlit Dashboard**: User-friendly, responsive, and filterable interface.
- 📁 **Exportable Clean Data**: Saves cleaned dataset to `cleaned_investments.csv`.

## 📁 Folder Structure

Start-Up/
├── cleaned_investments.csv      # Output from EDA
├── investments_VC.csv           # Raw dataset
├── main.py                      # Script to run EDA and dashboard
├── EDA.py                       # Data cleaning and insights script
├── startup_dashboard.py         # Streamlit interactive dashboard
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation

## ⚙️ Installation

1. Clone the repo:
   
   git clone https://github.com/Monster-78/Start-Up.git
   cd Start-Up
  
2. Install dependencies:
   
   pip install -r requirements.txt
   

## ▶️ Running the Project


python main.py

- First it performs EDA and saves cleaned data.
- Then it launches the Streamlit dashboard automatically.

Alternatively, to run the dashboard alone:

streamlit run startup_dashboard.py


## 🧪 Dashboard Functionality

- Filter by Country, Industry, and Funding Range.
- Visuals:
  - Top 10 funded industries.
  - Country-wise funding distribution.
  - Year-wise total investments.
- Cleaned data preview.

Judges or users can interactively explore and filter data using dropdowns and sliders.

## 💡 Ideas for Future Improvements

- Add ML model to predict successful funding.
- NLP analysis on startup descriptions.
- User login and file upload for custom datasets.
- Compare two industries or countries side-by-side.

## 🙌 Credits

Developed by: Monster-78

If you like this project, ⭐ the repo and share your feedback!

## 📜 License

MIT License

