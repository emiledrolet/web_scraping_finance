from tkinter import *
from stock import Stock

# TODO Add widget for each option

def process(stock):
    ticker = Stock(stock, income_statement=income_clicked, balance_sheet=feature_balance, cash_flow=feature_cash,
                   expand_all=feature_expand_all)
    ticker.web_scraping()

    window_enter = Toplevel(window)
    center_window(window_enter)
    window_enter.minsize(width=300, height=200)
    window_enter.title("Confirmation")
    confirmation_label = Label(window_enter, text="Le telechargement est pret")
    confirmation_label.grid()
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")
def button_clicked():
    stock = stock_input.get()
    process(stock)
def income_clicked():
    global feature_income
    if isIncomeStatement.get() == 1:
        feature_income = True
def balance_clicked():
    global feature_balance
    if isBalanceSheet.get() == 1:
        feature_balance = True
def cash_clicked():
    global  feature_cash
    if isCashFlow.get() == 1:
        feature_cash = True



#TODO Humm should not use Global variable,as little as possible

# Initialisiton Global Variable
feature_income = False
feature_balance = False
feature_cash = False
feature_expand_all = True


window = Tk()
window.title("Web Scraping Financial Data")
window.eval('tk::PlaceWindow . center')
window.minsize(width=500, height=300)
center_window(window)

# Label Logo
my_label_logo = Label(text="Logo")
my_label_logo.grid(column=0, row=0)

# Label Stock
my_label_stock = Label(text="stock")
my_label_stock.grid(column=0, row=1)

# Button
button_enter = Button(text="Enter", command=button_clicked)
button_enter.grid(column=0, row=3)

# Entry for stock
stock_input = Entry(width=10)
stock_input.grid(column=1, row=1)

# Check Box - Income Statement
isIncomeStatement = IntVar()
checkIncomeStatement = Checkbutton(variable=isIncomeStatement, onvalue=1, offvalue=0, command=income_clicked)
checkIncomeStatement.grid(column=0, row=4)

# Label Income Statement
my_label_income= Label(text="income statement")
my_label_income.grid(column=1, row=4)

# Check Box - Balance Sheet
isBalanceSheet = IntVar()
checkBalanceSheet = Checkbutton(variable=isBalanceSheet, onvalue=1, offvalue=0, command=balance_clicked)
checkBalanceSheet.grid(column=0, row=5)

# Label Balance Sheet
my_label_balance= Label(text="balance sheet")
my_label_balance.grid(column=1, row=5)

# Check Box - Cash Flow
isCashFlow = IntVar()
checkCashFlow = Checkbutton(variable=isCashFlow, onvalue=1, offvalue=0, command=cash_clicked)
checkCashFlow.grid(column=0, row=6)

# Label Cash Flow
my_label_cash= Label(text="cash flow")
my_label_cash.grid(column=1, row=6)



window.mainloop()
