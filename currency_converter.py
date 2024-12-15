import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Function to fetch exchange rates
def fetch_exchange_rate(api_key, from_currency, to_currency):
    try:
        url = "https://openexchangerates.org/api/latest.json"
        params = {"app_id": api_key}
        response = requests.get(url, params=params)
        data = response.json()

        if "rates" in data:
            from_rate = data["rates"].get(from_currency)
            to_rate = data["rates"].get(to_currency)
            if from_rate and to_rate:
                return to_rate / from_rate
            else:
                raise ValueError("Invalid currency code.")
        else:
            raise ValueError("Invalid response from API.")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch exchange rate: {e}")
        return None

# Function to perform conversion
def convert_currency():
    try:
        amount = float(entry_amount.get())
        from_currency = combo_from_currency.get().upper()
        to_currency = combo_to_currency.get().upper()

        if not amount or not from_currency or not to_currency:
            messagebox.showerror("Input Error", "Please enter all fields correctly.")
            return

        rate = fetch_exchange_rate(API_KEY, from_currency, to_currency)
        if rate:
            converted_amount = amount * rate
            label_result.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid amount.")

# API Key
API_KEY = "YOUR_API"

# GUI Setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x300")
root.resizable(False, False)

# Labels and Input Fields
label_heading = ttk.Label(root, text="Currency Converter", font=("Arial", 16, "bold"))
label_heading.pack(pady=10)

frame = ttk.Frame(root, padding=10)
frame.pack()

ttk.Label(frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
entry_amount = ttk.Entry(frame)
entry_amount.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="From Currency:").grid(row=1, column=0, padx=5, pady=5)
combo_from_currency = ttk.Combobox(frame, values=["USD", "EUR", "GBP", "JPY", "AUD", "CAD"], state="readonly")
combo_from_currency.grid(row=1, column=1, padx=5, pady=5)
combo_from_currency.set("USD")

ttk.Label(frame, text="To Currency:").grid(row=2, column=0, padx=5, pady=5)
combo_to_currency = ttk.Combobox(frame, values=["USD", "EUR", "GBP", "JPY", "AUD", "CAD"], state="readonly")
combo_to_currency.grid(row=2, column=1, padx=5, pady=5)
combo_to_currency.set("EUR")

# Convert Button
btn_convert = ttk.Button(root, text="Convert", command=convert_currency)
btn_convert.pack(pady=10)

# Result Label
label_result = ttk.Label(root, text="", font=("Arial", 12, "bold"), foreground="green")
label_result.pack(pady=10)

# Run the app
root.mainloop()