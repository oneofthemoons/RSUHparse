from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome("/Users/RSUH/drivers/chromedriver" ,chrome_options=chrome_options)
driver.get('https://www.rsuh.ru/raspis/')

srok = Select(driver.find_element_by_name('srok'))
srok.select_by_index(1)

driver.find_element_by_id("filters").click()

caf = Select(driver.find_element_by_name('caf'))
caf.select_by_index(62)

driver.find_element_by_name('potokbut2').click()

soup = BeautifulSoup(driver.page_source)

data = []
table = soup.find('table', attrs={'cellpadding':'3', 'border':'0'})
table_body = table.find('tbody')

rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])

print(data)

driver.quit()

being = { 'ПН': False, 'ВТ': False, 'СР': False, 'ЧТ': False, 'ПТ': False, 'СБ': False }

with open('/var/www/html/index.html', 'w', encoding='utf-8') as file:
    isEnglish = False;
    for i in range(1, len(data)):
        if 'ПН' in data[i][0] or 'ВТ' in data[i][0] or 'СР' in data[i][0] or 'ЧТ' in data[i][0] or 'ПТ' in data[i][0] or\
           'СБ' in data[i][0]:
            if being[data[i][0][-2:]]:
                break
            being[data[i][0][-2:]] = True
            file.write(data[i][0].split()[1] + '\t')
            file.write(
                data[i][1] + '\t' + data[i][2] + '\t' + data[i][3] + '\t' + data[i][4] + '\t' + data[i][5] + '\t' +
                data[i][6] + '\t')
        else:
            if not isEnglish:
                if data[i - 1][4] == 'Английский язык':
                    file.write(
                        data[i - 1][0] + '\t' + data[i - 1][1] + '\t' + data[i - 1][2] + '\t' + data[i][0] + '\t' +
                        data[i][1] + '\t' + data[i][2] + '\t')
                    isEnglish = True
                else:
                    file.write(data[i][0] + '\t' + data[i][1] + '\t' + data[i][2] + '\t' + data[i][3] + '\t' + data[i][
                        4] + '\t' + data[i][5] + '\t')
                    isEnglish = False;
            else:
                file.write(
                    data[i][0] + '\t' + data[i][1] + '\t' + data[i][2] + '\t' + data[i][3] + '\t' + data[i][4] + '\t' +
                    data[i][5] + '\t')
                isEnglish = False;

time.sleep(5)
