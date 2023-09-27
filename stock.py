from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


# TODO Have one excel only, or can be an option

# TODO Add the corresponding method for each parameter

# TODO Problem with consent(), put exception somehting like that. There is 2 cases.

class Stock:

    def __init__(self, ticker: str, income_statement: bool, balance_sheet: bool, cash_flow: bool,
                 expand_all: bool, summary: bool):
        # Summary
        self.ticker = ticker

        # Pages chose
        self.isIncomeStatement = income_statement
        self.isBalanceSheet = balance_sheet
        self.isCashFlow = cash_flow
        self.isSummary = summary

        # Options
        self.isExpandAll = expand_all

        # Others
        self.driver = None
        self.oneTime = 0

    def web_scraping(self):
        self.getBrowser()
        self.openNewWindow()
        # self.consent()

        # TODO Can do un for loop maybe. Need a list of each option or something like that
        if self.isIncomeStatement:
            self.getFinancialStatement("financials")
            self.openNewWindow()
        if self.isBalanceSheet:
            self.getFinancialStatement("balance-sheet")
            self.openNewWindow()
        if self.isCashFlow:
            self.getFinancialStatement("cash-flow")
            self.openNewWindow()
        if self.isSummary:
            self.getSummary()
            self.openNewWindow()

        self.driver.quit()

    def getSummary(self):
        self.driver.get(f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}")

        if self.oneTime == 0:
            self.consent()
            self.oneTime += 1

        summary_titles = self.driver.find_elements(By.CSS_SELECTOR, value='td[class="C($primaryColor) W(51%)"] span ')
        summary_data = self.driver.find_elements(By.CSS_SELECTOR, value='td[class="Ta(end) Fw(600) Lh(14px)"]')

        summary_title_list = [title.text for title in summary_titles]
        summary_data_list = [x.text for x in summary_data]
        name_columns = ["Title", "Value"]

        tableau = pd.DataFrame()

        tableau[name_columns[0]] = summary_title_list
        tableau[name_columns[1]] = summary_data_list

        tableau.to_excel(f'output_{self.ticker}_summary.xlsx', index=False)

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
        # url_consent = 'https://consent.yahoo.com/v2/collectConsent?sessionId=1_cc-session_d6058863-b799-4e26-a4fd-7cc201d915d7'
        # self.driver.get(url_consent)
        consent = self.driver.find_element(By.XPATH,
                                           value='//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button')
        consent.click()

    def getFinancialStatement(self, financial_statement):

        self.driver.get(f"https://finance.yahoo.com/quote/{self.ticker}/{financial_statement}?p={self.ticker}")

        if self.oneTime == 0:
            self.consent()
            self.oneTime += 1

        # Click on Expand all
        if self.isExpandAll:
            expand = self.driver.find_element(By.XPATH,
                                              value='//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button')
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
