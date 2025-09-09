# IL Trends - Interactive Publication Analysis

An interactive Streamlit application for analyzing research publication trends in ionic liquid research from 1975-2024.

## 🚀 Live Demo

[View the app on Streamlit Community Cloud](https://il-trends.streamlit.app) *(will be available after deployment)*

## 📊 Features

- **Interactive Topic Selection**: Choose from 6 research topics (0-5)
- **Search Strategy Comparison**: Compare Title+Abstract+Keywords (TS), Title Only (TI), and Title+Keywords (KW) search strategies
- **Flexible Time Range**: Analyze any period from 1975-2024
- **Dual Y-Axis Scaling**: Switch between linear and logarithmic scales
- **Professional Presentation Mode**: Clean white background with academic styling
- **Data Export**: Download filtered results as CSV

## 🛠️ Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/clarexie98/IL_trends.git
cd IL_trends
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run streamlit_app_professional.py
```

## 📁 Project Structure

```
├── streamlit_app_professional.py  # Main professional-styled app
├── streamlit_app.py              # Original app version
├── master_database_detailed.csv   # Main dataset (tidy format)
├── master_database_pivot.csv      # Pivot table format
├── master_database_summary.csv    # Summary statistics
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
└── create_master_database.py      # Data processing script
```

## 📈 Data

The analysis is based on publication data covering ionic liquid research from 1975-2024, categorized into 6 main research topics and searchable through different strategies:

- **Topics 0-5**: Various aspects of ionic liquid research
- **Search Strategies**:
  - TS: Title + Abstract + Keywords
  - TI: Title Only
  - KW: Title + Keywords

## 🎯 Usage

1. **Select Topics**: Choose one or more research topics from the left panel
2. **Choose Search Strategies**: Select TS, TI, or KW to compare different search approaches
3. **Set Time Range**: Adjust the analysis period using the year slider
4. **Scale Options**: Toggle between linear and logarithmic y-axis scaling
5. **Export Data**: Download your filtered results for further analysis

## 🚀 Deployment

This app is deployed on Streamlit Community Cloud. To deploy your own version:

1. Fork this repository
2. Connect your GitHub account to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Deploy directly from your GitHub repository

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📧 Contact

For questions about this research or the application, please contact the repository owner.
