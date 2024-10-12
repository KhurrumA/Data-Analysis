import pandas as pd
import seaborn as sb
import sqlite3
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog, messagebox, Entry, StringVar, Frame, Toplevel
from sklearn.linear_model import LinearRegression

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path, encoding="ISO-8859-1")
        print("Data Loaded:\n", data.head())
        return data
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV file:\n{str(e)}")
        return None

def setup_database(data, db_name):
    try:
        data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'], errors='coerce')
        data.dropna(subset=['InvoiceDate'], inplace=True)

        con = sqlite3.connect(db_name)
        cursor = con.cursor()

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS orders (
            InvoiceNo TEXT,
            StockCode TEXT,
            Description TEXT,
            Quantity INTEGER,
            InvoiceDate TEXT,
            UnitPrice REAL,
            CustomerID REAL,
            Country TEXT
        )
        '''

        cursor.execute(create_table_query)
        con.commit()

        data.to_sql('orders', con, if_exists='replace', index=False)
        con.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to set up database:\n{str(e)}")

def analysis(db_name):
    con = sqlite3.connect(db_name)

    q_top_spenders = '''
    SELECT CustomerID, SUM(UnitPrice * Quantity) AS TotalSpent
    FROM orders
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
    ORDER BY TotalSpent DESC
    LIMIT 10
    '''
    top_spenders = pd.read_sql(q_top_spenders, con)
    
    query_sales_trend = '''
    SELECT strftime('%Y-%m', InvoiceDate) AS Month, SUM(UnitPrice * Quantity) AS MonthlySales
    FROM orders
    GROUP BY Month
    ORDER BY Month
    '''
    sales_trends = pd.read_sql(query_sales_trend, con)

    query_top_items_all_time = '''
    SELECT StockCode, SUM(Quantity) AS TotalSold
    FROM orders
    GROUP BY StockCode
    ORDER BY TotalSold DESC
    LIMIT 10
    '''
    top_items_all_time = pd.read_sql(query_top_items_all_time, con)

    
    recent_month_query = '''
    SELECT strftime('%Y-%m', MAX(InvoiceDate)) AS RecentMonth
    FROM orders
    '''
    recent_month = pd.read_sql(recent_month_query, con)['RecentMonth'].values[0]

    query_top_items_month = f'''
    SELECT StockCode, SUM(Quantity) AS TotalSold
    FROM orders
    WHERE strftime('%Y-%m', InvoiceDate) = ?
    GROUP BY StockCode
    ORDER BY TotalSold DESC
    LIMIT 10
    '''
    top_items_month = pd.read_sql(query_top_items_month, con, params=(recent_month,))

    con.close()
    
    return top_spenders, sales_trends, top_items_all_time, top_items_month

def visualize_top_spenders(top_spenders):
    plt.figure(figsize=(10, 6))
    sb.barplot(x='CustomerID', y='TotalSpent', data=top_spenders, palette='viridis')
    plt.title('Top 10 Customers by Total Spend')
    plt.xlabel('Customer ID')
    plt.ylabel('Total Spend')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def visualize_sales_trends(sales_trends):
    if sales_trends.empty:
        messagebox.showinfo("Information", "No sales trends data to visualize.")
        return
    
    plt.figure(figsize=(10, 6))
    sb.lineplot(x='Month', y='MonthlySales', data=sales_trends, marker='o')
    plt.title('Monthly Sales Trends')
    plt.xlabel('Month')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def visualize_top_items(top_items, title):
    plt.figure(figsize=(10, 6))
    sb.barplot(x='StockCode', y='TotalSold', data=top_items, palette='magma')
    plt.title(title)
    plt.xlabel('Stock Code')
    plt.ylabel('Total Sold')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_analysis_options(top_spenders, sales_trends, top_items_all_time, top_items_month):
    analysis_window = Toplevel()
    analysis_window.title("Analysis Options")
    analysis_window.geometry("300x300")

    button_top_spenders = Button(analysis_window, text="Show Top Customers", command=lambda: visualize_top_spenders(top_spenders), padx=20, pady=10)
    button_top_spenders.pack(pady=10)

    button_monthly_sales = Button(analysis_window, text="Show Monthly Sales Trends", command=lambda: visualize_sales_trends(sales_trends), padx=20, pady=10)
    button_monthly_sales.pack(pady=10)

    button_top_items_all_time = Button(analysis_window, text="Show Top Items (All Time)", command=lambda: visualize_top_items(top_items_all_time, "Top 10 Items by Total Sales (All Time)"), padx=20, pady=10)
    button_top_items_all_time.pack(pady=10)

    button_top_items_month = Button(analysis_window, text="Show Top Items (This Month)", command=lambda: visualize_top_items(top_items_month, "Top 10 Items by Total Sales (This Month)"), padx=20, pady=10)
    button_top_items_month.pack(pady=10)

def run_analysis():
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    
    if not file_path:
        messagebox.showwarning("Warning", "No file selected.")
        return
    
    db_name = 'database.db'
    
    data = load_csv(file_path)
    if data is None:
        return  
    
    setup_database(data, db_name)
    
    top_spenders, sales_trends, top_items_all_time, top_items_month = analysis(db_name)
    
    show_analysis_options(top_spenders, sales_trends, top_items_all_time, top_items_month)

def search_and_predict():
    product_code = product_code_var.get()
    if not product_code:
        messagebox.showwarning("Warning", "Please enter a product code.")
        return

    con = sqlite3.connect('database.db')

    query = '''
    SELECT strftime('%Y-%m', InvoiceDate) AS Month, SUM(Quantity) AS TotalSales, AVG(UnitPrice) AS AveragePrice
    FROM orders
    WHERE StockCode = ?
    GROUP BY Month
    ORDER BY Month
    '''
    product_sales = pd.read_sql(query, con, params=(product_code,))

    if product_sales.empty:
        messagebox.showinfo("Information", f"No sales data found for product: {product_code}")
        return

    product_sales['Month'] = pd.to_datetime(product_sales['Month'])
    product_sales['MonthIndex'] = product_sales['Month'].dt.month + 12 * product_sales['Month'].dt.year  # Convert to a continuous index for regression
    X = product_sales['MonthIndex'].values.reshape(-1, 1)
    y = product_sales['TotalSales'].values

   
    if len(X) < 2: #Is there enough data for regression?
        messagebox.showinfo("Information", "Not enough data for regression.")
        return

    model = LinearRegression()
    model.fit(X, y)

    next_month_index = X[-1][0] + 1  
    predicted_sales = model.predict([[next_month_index]])

    average_price = product_sales['AveragePrice'].iloc[-1]  
    estimated_income = predicted_sales[0] * average_price

    messagebox.showinfo("Prediction Result",
                        f"Estimated Sales for '{product_code}': {predicted_sales[0]:.2f}\nEstimated Total Income: ${estimated_income:.2f}")

    con.close()

def create_gui():
    root = Tk()
    root.title("Data Analytics App")
    root.geometry("400x300")  
    root.configure(bg="#f0f0f0")  

    global product_code_var
    product_code_var = StringVar()
    
 
    title_label = Label(root, text="Data Analytics Application", font=("Arial", 16, "bold"), bg="#f0f0f0")
    title_label.pack(pady=10)


    button_frame = Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=10)


    button_load = Button(button_frame, text="Load CSV and Analyze Data", command=run_analysis, padx=20, pady=10, bg="#4CAF50", fg="white", font=("Arial", 12))
    button_load.pack(pady=5)

    search_label = Label(root, text="Enter Product Code for Prediction:", bg="#f0f0f0", font=("Arial", 12))
    search_label.pack(pady=5)

    product_code_entry = Entry(root, textvariable=product_code_var, width=20, font=("Arial", 12))
    product_code_entry.pack(pady=5)

    button_predict = Button(root, text="Predict Sales", command=search_and_predict, padx=20, pady=10, bg="#2196F3", fg="white", font=("Arial", 12))
    button_predict.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
