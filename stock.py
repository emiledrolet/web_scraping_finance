from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

#TODO Have one excel only, or can be an option

#TODO Add the corresponding method for each parameter
# Don't forget about we can choose several choices, so gonna have to decompose a little more

class Stock:

    def __init__(self, ticker: str, income_statement:bool = True, balance_sheet:bool = True, cash_flow:bool = True,
                 expand_all: bool = False):
        #Specifics
        self.ticker = ticker

        #Pages
        self.isIncomeStatement = income_statement
        self.isBalanceSheet = balance_sheet
        self.isCashFlow = cash_flow

        #Options
        self.isExpandAll = expand_all

        #Others
        self.driver = None

    def web_scraping(self):
        self.getBrowser()
        self.openNewWindow()
        self.consent()

        #TODO Can do un for loop maybe. Need a list of each option or something like that
        if self.isIncomeStatement:
            self.getFinancialStatement("financials")
            self.openNewWindow()
        if self.isBalanceSheet:
            self.getFinancialStatement("balance-sheet")
            self.openNewWindow()
        if self.isCashFlow:
            self.getFinancialStatement("cash-flow")
            self.openNewWindow()

        self.driver.quit()

    def getBrowser(self):
        # Keep Chrome browser open after program finishes
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option("detach", True)

        # Which browser to choose. This is a class.
        driver = webdriver.Chrome(options=chrome_option)

        self.driver = driver

    def openNewWindow(self):
        # Open a new window (javascript)
        self.driver.execute_script("window.open('', '_blank');")

        # Retrieve all the window
        window_handles = self.driver.window_handles

        # Switch to the last window
        self.driver.switch_to.window(window_handles[-1])

    def consent(self):
        url_consent = 'https://consent.yahoo.com/v2/collectConsent?sessionId=1_cc-session_d6058863-b799-4e26-a4fd-7cc201d915d7'
        self.driver.get(url_consent)
        consent = self.driver.find_element(By.XPATH, value='//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button')
        consent.click()


    #TODO Create .getFinancialStatement to avoid repetition for Income Statement, Balance Sheet, and Cash Flow
    def getFinancialStatement(self,financial_statement):

        self.driver.get(f"https://finance.yahoo.com/quote/{self.ticker}/{financial_statement}?p={self.ticker}")


        # Click on Expand all
        if self.isExpandAll:
            expand = self.driver.find_element(By.XPATH, value='//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button')
            expand.click()

        # Récuperer les data
        financial_data = self.driver.find_elements(By.CSS_SELECTOR,
                                                   value='div[data-test="fin-row"] div[data-test="fin-col"] ')
        names_column = self.driver.find_elements(By.CSS_SELECTOR, value='div[class="D(tbr) C($primaryColor)"] span')
        names_row = self.driver.find_elements(By.CSS_SELECTOR,
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


        tableau.to_excel(f'output_{self.ticker}_{financial_statement}.xlsx', index=False)



