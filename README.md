# Data Analysis Tool

This is a lightweight, GUI-based data analysis and forecasting tool originally developed for internal use at M&Z UK Ltd, now released as an open-source solution.  
It performs data ingestion, summary statistics, sales trend visualization, and product sales forecasting using linear regression.  
**Note:** The program structure has been simplified for public release. The original dataset is real but sensitive.

---

## Features

- Upload and analyze CSV files containing sales data
- Store and query data using SQLite
- View:
  - Top 10 customers by total spend
  - Monthly sales trends
  - Top 10 products sold (all time and most recent month)
- Predict future sales for a selected product using linear regression
- GUI built with Tkinter for ease of use

---

## Technologies Used

- Python
- Pandas
- SQLite3
- Seaborn / Matplotlib
- scikit-learn (Linear Regression)
- Tkinter (GUI)

---

## Requirements

Install required libraries:

```bash
pip install -r Req.txt
```

Contents of `Req.txt`:

```
pandas
sqlite3
matplotlib
seaborn
```

---

## Usage

1. Run the application:

```bash
python Run.py
```

2. Use the GUI to:
   - Select and load a CSV file
   - Perform automatic database setup and summary analysis
   - View charts or make predictions by entering a product code

3. Output:
   - Visual analysis of sales trends, top items, and customer behavior
   - Forecast of next-month sales and estimated income per product

---

## Dataset

Please extract the dataset separately (not included in public version).  
The dataset is real but stripped of sensitive or identifying company details.

---

## Disclaimer

This program is provided as-is for educational and demonstration purposes.  
It was originally built under NDA and parts of the source have been removed for compliance.

---

## Author

**Khurrum Arif**  
[KhurrumArif02@gmail.com](mailto:KhurrumArif02@gmail.com)  
[LinkedIn](https://www.linkedin.com/in/khurrum-arif-uol)  
[GitHub](https://github.com/KhurrumA)
