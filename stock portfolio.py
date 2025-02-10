import yfinance as yf
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time

# Initialize portfolio as a dictionary {ticker: quantity}
portfolio = {}

# Function to fetch stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if data.empty:
        return None
    return data['Close'].iloc[-1]

# Function to add a stock to the portfolio
def add_stock():
    ticker = ticker_entry.get().strip().upper()
    quantity = quantity_entry.get().strip()

    if not ticker or not quantity:
        messagebox.showwarning("Input Error", "Please enter both ticker and quantity.")
        return

    # Append .NS for NSE if not already present
    if not ticker.endswith(".NS"):
        ticker += ".NS"

    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Input Error", "Quantity must be a positive integer.")
        return

    price = get_stock_data(ticker)
    if price is None:
        messagebox.showwarning("Invalid Ticker", f"Could not fetch data for {ticker}.")
        return

    portfolio[ticker] = quantity
    update_portfolio_display()
    ticker_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

# Function to update the portfolio display
def update_portfolio_display():
    for row in portfolio_tree.get_children():
        portfolio_tree.delete(row)

    total_investment = 0
    total_value = 0

    for ticker, quantity in portfolio.items():
        price = get_stock_data(ticker)
        if price is None:
            continue
        investment = price * quantity
        total_investment += investment
        total_value += investment
        portfolio_tree.insert("", tk.END, values=(ticker, quantity, f"₹{price:.2f}", f"₹{investment:.2f}"))

    total_value_label.config(text=f"Total Portfolio Value: ₹{total_value:.2f}")

# Function to refresh the portfolio data periodically
def auto_refresh():
    while True:
        update_portfolio_display()
        time.sleep(60)  # Refresh every 60 seconds

# Function to start the auto-refresh thread
def start_auto_refresh():
    refresh_thread = threading.Thread(target=auto_refresh, daemon=True)
    refresh_thread.start()

# Create the main window
root = tk.Tk()
root.title("Indian Stock Portfolio Tracker")
root.geometry("600x400")

# Frame for adding stocks
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(fill=tk.X)

tk.Label(input_frame, text="Ticker:").grid(row=0, column=0, padx=5, pady=5)
ticker_entry = tk.Entry(input_frame, width=10)
ticker_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
quantity_entry = tk.Entry(input_frame, width=10)
quantity_entry.grid(row=0, column=3, padx=5, pady=5)

add_button = tk.Button(input_frame, text="Add Stock", command=add_stock)
add_button.grid(row=0, column=4, padx=5, pady=5)

# Frame for displaying the portfolio
portfolio_frame = tk.Frame(root, padx=10, pady=10)
portfolio_frame.pack(fill=tk.BOTH, expand=True)

columns = ("Ticker", "Quantity", "Price", "Value")
portfolio_tree = ttk.Treeview(portfolio_frame, columns=columns, show="headings")
portfolio_tree.heading("Ticker", text="Ticker")
portfolio_tree.heading("Quantity", text="Quantity")
portfolio_tree.heading("Price", text="Price")
portfolio_tree.heading("Value", text="Value")
portfolio_tree.pack(fill=tk.BOTH, expand=True)

# Label for total portfolio value
total_value_label = tk.Label(root, text="Total Portfolio Value: ₹0.00", font=("Arial", 12), pady=10)
total_value_label.pack()

# Start the auto-refresh thread
start_auto_refresh()

# Run the application
root.mainloop()