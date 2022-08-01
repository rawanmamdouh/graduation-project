from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import csv
import time

# Load genes from CSV file
def load_genes(fileName):
    file = open(fileName, 'r', encoding='utf-8-sig', newline='')
    csvreader = csv.reader(file)
    # escape the headers
    next(csvreader)
    rows = []
    for row in csvreader:
            rows.append(row)
    file.close()
    return rows

# Scraping data from genecards
def scrape_genecards():
    genes = load_genes('genes.csv')
    fileName = time.ctime(time.time()) + 'genecards.csv'
    file = open(fileName, 'a', encoding='utf-8-sig', newline='')
    csvwriter = csv.writer(file, delimiter = ";", quoting=csv.QUOTE_ALL)
    # Write the header
    csvwriter.writerow(['Summarizes Of Gene', 'Protein name', 'Drugs names', 'Protein Expression', 'Pathway', 'Gene Function'])

    chrome_options = webdriver.ChromeOptions()
    # To hide chrome window
    chrome_options.headless = True
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    for gene in genes:
        
        URL = 'https://www.genecards.org/cgi-bin/carddisp.pl?gene=' + gene[0]
        browser.get(URL)

        try:
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/h1'))).text
            continue
        except:
            print('Scraping data from genecard for ' + gene[0])
                                                                                                
        try: 
            summarizesOfGene = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/main/div[2]/div/div/section[2]/div[2]/p'))).text
        except:
            try: 
                summarizesOfGene = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/main/div[2]/div/div/section[2]/div[3]/p'))).text
            except:
                summarizesOfGene = 'None'
        #print(summarizesOfGene)
        try:
            recommendedName = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/main/div[4]/div/div/section[1]/div[2]/div[1]/ul/li/div[1]/div[2]/dl[1]/dd[2]'))).text
        except:
            recommendedName = 'None'

        #print(recommendedName)

        # Get size of Drugs & Compounds table
        num_rows = len (browser.find_elements(by=By.XPATH, value='/html/body/div[1]/div[3]/div/div/main/div[7]/div/div/section/div[3]/div[2]/div/div[2]/div/table/tbody/tr'))
        names = ''
        for t_row in range(1, (num_rows), 2):
            rowXPath = '/html/body/div[1]/div[3]/div/div/main/div[7]/div/div/section/div[3]/div[2]/div/div[2]/div/table/tbody/tr['+str(t_row)+']'
            name = browser.find_element(by=By.XPATH, value=rowXPath+'/td[2]').text
            names += '/'+name+'/'
        #print(names)
        # Get size of superPathWay table
        num_rows_superPathWay = len (browser.find_elements(by=By.XPATH, value='/html/body/div[1]/div[3]/div/div/main/div[6]/div/div/section/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr'))+1
        SuperPathway = ''
        for t_row in range(1, (num_rows_superPathWay), 1):
            rowXPath = '/html/body/div[1]/div[3]/div/div/main/div[6]/div/div/section/div[1]/div[2]/div[2]/div/div[2]/div/table/tbody/tr['+str(t_row)+']'
            name = browser.find_element(by=By.XPATH, value=rowXPath+'/td[2]').text
            SuperPathway += '/'+name+'/'

        # Get size of qualifiedGo table
        num_rows_GO = len (browser.find_elements(by=By.XPATH, value='/html/body/div[1]/div[3]/div/div/main/div[5]/div/div/section[1]/div[2]/div[3]/div[2]/div/div/div[2]/div/table/tbody/tr'))+1
        qualifiedGo = ''
        for t_row in range(1, (num_rows_GO), 1):
            rowXPath = '/html/body/div[1]/div[3]/div/div/main/div[5]/div/div/section[1]/div[2]/div[3]/div[2]/div/div/div[2]/div/table/tbody/tr['+str(t_row)+']'
            name = browser.find_element(by=By.XPATH, value=rowXPath+'/td[2]').text
            qualifiedGo += '/'+name+'/'
        
        try:
            proteinExpression = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div/main/div[9]/div/div/section[1]/div[2]/div[2]/div[2]/figure/div[1]/img'))).get_attribute('src')
        except:
            proteinExpression = 'None'
        #print(proteinExpression)
        # Append data to csv file



        csvwriter.writerow([summarizesOfGene, recommendedName, names, proteinExpression, SuperPathway, qualifiedGo])


def main():
    scrape_genecards()

if __name__ == "__main__":
    main()
