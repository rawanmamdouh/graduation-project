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

# Scraping data from 
def scrape_drugbank():
    genes = load_genes('genes.csv')
    fileName = time.ctime(time.time()) + '-DrugBank.csv'
    file = open(fileName, 'a', encoding='utf-8-sig', newline='')
    csvwriter = csv.writer(file, delimiter = ";", quoting=csv.QUOTE_ALL)
    # Write the header
    csvwriter.writerow(['Gene', 'Target', 'Drug Relations'])

    chrome_options = webdriver.ChromeOptions()
    # To hide chrome window
    chrome_options.headless = True
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    for gene in genes:
        print('Start search targets for gene '+gene[0])
        URL = 'https://go.drugbank.com/unearth/q?query=' + gene[0] + '&button=&searcher=bio_entities'
        browser.get(URL)

        items = browser.find_elements(By.XPATH, "/html/body/main/div/div[2]/div[3]/div/div/div")
        for t in items:
            targetName = t.find_element_by_tag_name('a').text
            print('Start scraping Drug Relations from ' + targetName)
            targetUrl = t.find_element_by_tag_name('a').get_attribute('href')

            browser.execute_script("window.open('');")
        
            # Switch to the new window and open new URL
            browser.switch_to.window(browser.window_handles[1])
            browser.get(targetUrl)
            
            num_rows = len (browser.find_elements(by=By.XPATH, value='//*[@id="target-relations"]/tbody/tr'))
            DrugRelations = ''
            
            for t_row in range(1, (num_rows+1)):
                rowXPath = '//*[@id="target-relations"]/tbody/tr['+str(t_row)+']'
                name = browser.find_element(by=By.XPATH, value=rowXPath+'/td[2]').text
                DrugRelations += '/'+name+'/'
            print(DrugRelations)
            
            # Append data to csv file
            csvwriter.writerow([gene[0], targetName, DrugRelations])    
            
            # Closing new_url tab
            browser.close()
            # Switching to old tab
            browser.switch_to.window(browser.window_handles[0])
        
           

def main():
    scrape_drugbank()
    

if __name__ == "__main__":
    main()
