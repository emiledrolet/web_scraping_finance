from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tkinter import *

# import os
# os.environ("NAME_OF_THE_VARIABLE")

#TODO Transform the code in the OOP Form
#class FinancialDataStock():

#   getIncomeStatement()
#   getBalanceSheet()
#   getCashFlow()


def traitement(stock):
    # Keep Chrome browser open after program finishes
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_experimental_option("detach", True)

    # Which browser to choose. This is a class.
    driver = webdriver.Chrome(options=chrome_option)

    driver.get(f"https://finance.yahoo.com/quote/{stock}/financials?p={stock}")

    # Click on Expand all
    expand = driver.find_element(By.XPATH, value='//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button')
    expand.click()

    # Recuperer les data
    financial_data = driver.find_elements(By.CSS_SELECTOR, value='div[data-test="fin-row"] div[data-test="fin-col"] ')
    names_column = driver.find_elements(By.CSS_SELECTOR, value='div[class="D(tbr) C($primaryColor)"] span')
    names_row = driver.find_elements(By.CSS_SELECTOR, value='div[class="D(tbr) fi-row Bgc($hoverBgColor):h"] span[class="Va(m)"]')

    #Mettre les data dans des listes
    financial_data_list = [data.text for data in financial_data]
    names_column_list = [data.text for data in names_column]
    names_row_list = [data.text for data in names_row]


    NUMBER_OF_COLUMNS = len(names_column_list)


    #Initialisation du tableau
    tableau = pd.DataFrame()

    #Append the tableau
    for i in range(0, NUMBER_OF_COLUMNS):
        if i == 0:
            #Premiere colonne
            tableau[names_column_list[i]] = names_row_list
        else:
            #Autre colonne
            tableau[names_column_list[i]] = financial_data_list[i-1::NUMBER_OF_COLUMNS - 1]

    # TODO Put the ouput in your download folder
    tableau.to_excel(f'output_{stock}.xlsx', index=False)

    driver.quit()

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

window.mainloop()