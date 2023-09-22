from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from tkinter import *


#TODO Add the corresponding method for each parameter
# Don't forget about we can choose several choices, so gonna have to decompose a little more

class Stock:

    def __init__(self, ticker: str, income_statement:bool = False, balance_sheet:bool= False, cash_flow:bool= False, expand_all:bool= False):
        self.ticker = ticker
        self.isIncomeStatement = income_statement
        self.isBalanceSheet = balance_sheet
        self.isCashFlow = cash_flow
        self.isExpandAll = expand_all
    def getIncomeStatemet(self):
        # Keep Chrome browser open after program finishes
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option("detach", True)

        # Which browser to choose. This is a class.
        driver = webdriver.Chrome(options=chrome_option)


        #Consent
        url_consent = 'https://consent.yahoo.com/v2/collectConsent?sessionId=1_cc-session_b03884c0-5233-499d-9f4d-c8bbfcd66a76'
        driver.get(url_consent)
        consent = driver.find_element(By.XPATH, value='//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button')
        consent.click()

        #Open new window
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(f"https://finance.yahoo.com/quote/{self.ticker}/financials?p={self.ticker}")


        # Click on Expand all
        if self.isExpandAll:
            expand = driver.find_element(By.XPATH, value='//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button')
            expand.click()

        # Récuperer les data
        financial_data = driver.find_elements(By.CSS_SELECTOR,
                                              value='div[data-test="fin-row"] div[data-test="fin-col"] ')
        names_column = driver.find_elements(By.CSS_SELECTOR, value='div[class="D(tbr) C($primaryColor)"] span')
        names_row = driver.find_elements(By.CSS_SELECTOR,
                                         value='div[class="D(tbr) fi-row Bgc($hoverBgColor):h"] span[class="Va(m)"]')

        # Mettre les data dans des listes
        financial_data_list = [data.text for data in financial_data]
        names_column_list = [data.text for data in names_column]
        names_row_list = [data.text for data in names_row]

        NUMBER_OF_COLUMNS = len(names_column_list)

        # Initialisation du tableau
        tableau = pd.DataFrame()

        # Append the tableau
        for i in range(0, NUMBER_OF_COLUMNS):
            if i == 0:
                # Premiere colonne
                tableau[names_column_list[i]] = names_row_list
            else:
                # Autre colonne
                tableau[names_column_list[i]] = financial_data_list[i - 1::NUMBER_OF_COLUMNS - 1]

        # TODO Put the output in your download folder
        tableau.to_excel(f'output_{self.ticker}.xlsx', index=False)

        driver.quit()
