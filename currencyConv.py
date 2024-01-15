import tkinter as tk
from tkinter import ttk, messagebox
import requests

class CurrencyConverter:
    rates = {}

    def __init__(self, url):
        data = requests.get(url).json()
        self.rates = data["rates"]

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]

        amount = round(amount * self.rates[to_currency], 2)
        return initial_amount, from_currency, amount, to_currency

class WelcomeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("400x300")
        # logo = tk.PhotoImage(file="icon.png")
        # logoLabel = tk.Label(root, image=logo)
        # logoLabel.pack()
        ttk.Label(root, text="Welcome to our Currency Converter!",font=("Arial",12)).pack(pady=50)
        ttk.Button(root, text="Continue", command=self.show_login).pack(pady=10)

    def show_login(self):
        self.root.destroy()
        login_root = tk.Tk()
        login_app = LoginWindow(login_root)
        login_root.mainloop()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter-Login")
        self.root.geometry("200x300")

        # inputs
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(root, text="Username:").pack(pady=5)
        ttk.Entry(root, textvariable=self.username_var).pack(padx=5,pady=5)
        ttk.Label(root, text="Password:").pack(pady=5)
        ttk.Entry(root, textvariable=self.password_var, show="*").pack(padx=5,pady=5)
        ttk.Button(root, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        # pre defined users and password
        if username == "sarah" or "yazan" and password == "1234":
            self.root.destroy()
            converter_root = tk.Tk()
            converter_app = ConversionWindow(converter_root)
            converter_root.mainloop()
        else:
            messagebox.showerror("Failed", "Invalid username or password")

class ConversionWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("200x400")

        # Currency converter variables
        self.from_currency_var = tk.StringVar()
        self.to_currency_var = tk.StringVar()
        self.amount_var = tk.DoubleVar()
        self.result_var = tk.StringVar()

        # history
        self.conversion_history = []

        ttk.Label(root, text="From Country:").pack(pady=5)
        ttk.Entry(root, textvariable=self.from_currency_var).pack(padx=5,pady=5)
        ttk.Label(root, text="To Country:").pack(pady=5)
        ttk.Entry(root, textvariable=self.to_currency_var).pack(padx=5,pady=5)
        ttk.Label(root, text="Amount:").pack(pady=5)
        ttk.Entry(root, textvariable=self.amount_var).pack(padx=5,pady=5)
        ttk.Button(root, text="Convert", command=self.convert_currency).pack(pady=10)
        ttk.Button(root, text="History", command=self.show_history).pack(pady=10)
        ttk.Label(root, textvariable=self.result_var).pack(pady=10)

        ttk.Button(root, text="button", command=self.newWindow).pack(pady=10)
        ttk.Label(root, textvariable=self.result_var).pack(pady=10)

    def convert_currency(self):
        from_country = self.from_currency_var.get()
        to_country = self.to_currency_var.get()
        amount = self.amount_var.get()

        initial_amount, from_currency, converted_amount, to_currency = c.convert(from_country, to_country, amount)
        result_str = '{} {} = {} {}'.format(initial_amount, from_currency, converted_amount, to_currency)
        self.result_var.set(result_str)

        # goes to conversion history
        self.conversion_history.append(result_str)
        self.update_history_listbox()
    def show_history(self):
        history_root = tk.Tk()
        history_app = HistoryWindow(history_root, self.conversion_history)
        history_root.mainloop()

    def update_history_listbox(self):
        pass

    def newWindow(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Window")
        ttk.Label(new_window, text="sarah").pack(pady=10)

class HistoryWindow:
    def __init__(self, root, conversion_history):
        self.root = root
        self.root.title("Conversion History")
        self.root.geometry("200x400")

        # inputs
        self.conversion_history = conversion_history

        ttk.Label(root, text="Conversion History").pack(pady=10)
        self.history_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.history_listbox.pack(pady=10)

        # gets history from file
        self.load_history_from_file()

        ttk.Button(root, text="Exit", command=self.show_thank_you).pack(pady=10)

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.conversion_history:
            self.history_listbox.insert(tk.END, item)

    def load_history_from_file(self):
        try:
            with open("conversion_history.txt", "r") as file:
                self.conversion_history = [line.strip() for line in file.readlines()]
                self.update_history_listbox()
        except FileNotFoundError:
            pass

    def save_history_to_file(self):
        with open("conversion_history.txt", "w") as file:
            for item in self.conversion_history:
                file.write(item + "\n")

    def show_thank_you(self):
        self.save_history_to_file()
        messagebox.showinfo("Currency Converter", "Thank you for using our Currency Converter!")
        self.root.destroy()

if __name__ == "__main__":
    url = "http://data.fixer.io/api/latest?access_key=08db15eb4dcdf71d61e8916a413b35c8"
    c = CurrencyConverter(url)
    welcome_root = tk.Tk()
    welcome_app = WelcomeWindow(welcome_root)
    welcome_root.mainloop()
