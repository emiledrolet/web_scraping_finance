from tkinter import *
from stock import Stock


# import os
# os.environ("NAME_OF_THE_VARIABLE")

def traitement(stock):

    test = Stock(stock, expand_all=True)
    test.getIncomeStatemet()

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
    traitement(stock)

window = Tk()
window.title("Web Scraping Financial Data")
window.eval('tk::PlaceWindow . center')
window.minsize(width=500, height=300)
center_window(window)

#Label Logo
my_label_logo = Label(text="Logo")
my_label_logo.grid(column=0, row=0)

#Label Stock
my_label_stock = Label(text="stock")
my_label_stock.grid(column=0, row=1)

#Button
button_enter = Button(text="Enter", command=button_clicked)
button_enter.grid(column=0, row=3)

#Entry
stock_input = Entry(width=10)
stock_input.grid(column=1, row=1)

#TODO Add checkbox (something like that) for each parameter
# The parameters are:
# Income Statement
# Balanche Sheet
# CashFlow
# Expand All



window.mainloop()