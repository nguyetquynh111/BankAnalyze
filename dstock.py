from selenium import webdriver
from tqdm import tqdm
from selenium.webdriver.common.by import By
import pandas as pd
from tqdm import tqdm
from time import sleep
import re
import random as rd
from unidecode import unidecode

STOCK_CRAWL_URLS = """
https://dstock.vndirect.com.vn/tong-quan/ACB
https://dstock.vndirect.com.vn/tong-quan/BID
https://dstock.vndirect.com.vn/tong-quan/CTG
https://dstock.vndirect.com.vn/tong-quan/EIB
https://dstock.vndirect.com.vn/tong-quan/HDB
https://dstock.vndirect.com.vn/tong-quan/LPB
https://dstock.vndirect.com.vn/tong-quan/MBB
https://dstock.vndirect.com.vn/tong-quan/MSB
https://dstock.vndirect.com.vn/tong-quan/OCB
https://dstock.vndirect.com.vn/tong-quan/STB
https://dstock.vndirect.com.vn/tong-quan/SSB
https://dstock.vndirect.com.vn/tong-quan/TCB
https://dstock.vndirect.com.vn/tong-quan/TPB
https://dstock.vndirect.com.vn/tong-quan/VCB
https://dstock.vndirect.com.vn/tong-quan/VIB
https://dstock.vndirect.com.vn/tong-quan/VPB
""".split()
BANKS_CODE = ['ACB', 'BID', 'CTG', 'EIB', 'HDB', 
              'LVB', 'MBB', 'MSB', 'OCB', 'STB', 
              'SSB', 'TCB', 'TPB', 'VCB', 'VIB', 
              'VPB']
LINK_TO_BANK = dict(zip(STOCK_CRAWL_URLS, BANKS_CODE))
REMOVE_PUNCTUATION = ['\(', '\)', '\/']
FEATURES = ['he so an toan von car',
 'von chu so huu  tong tai san',
 'ty le no xau npl',
 'ty le bao no xau',
 'lai du thu  tong tai san',
 'tang truong cho vay gop sv dau ky',
 'cho vay gop  tien gui khach hang',
 'cho vay gop  tong tai san',
 'thu nhap lai  tong thu nhap hd',
 'thu nhap ngoai lai  tong thu nhap hd',
 'ty le lai can bien nim',
 'chi phi tin dung',
 'tang truong lntt sv cung ky',
 'roaa',
 'roae']
driver = webdriver.Firefox()
scraped_table = pd.DataFrame()
def clean_format_text(text: str):
    text = unidecode(text).lower()
    text = re.sub('|'.join(REMOVE_PUNCTUATION),'',text)
    return text
for crawl_url in tqdm(STOCK_CRAWL_URLS):
    sleep(rd.randint(15,30))
    driver.get(crawl_url)
    sleep(rd.randint(15,30))
    driver.execute_script("window.scrollTo(0, 1300)") 
    sleep(rd.randint(15,30))
    xpath_path = """//*[@id="dncb"]/div"""
    element = driver.find_element(By.XPATH, xpath_path)
    text_split = element.text.split('\n')
    years = text_split[2].split()
    format_values = []
    for text in text_split[3:]:
        text = clean_format_text(text)
        format_text = re.sub('|'.join(FEATURES),'',text).strip()
        number_found = format_text.split()
        if len(number_found)==4:
            number_found_format = []
            for i in number_found:
                if i=='na':
                    number_found_format.append(None)
                else:
                    number_found_format.append(i)
            format_values.append(number_found_format)

    data = pd.DataFrame(format_values)
    data.columns = years
    data['feature'] = [i.replace(' ','-') for i in FEATURES]
    data['bank'] = LINK_TO_BANK.get(crawl_url)
    scraped_table = pd.concat([scraped_table, data], axis=0)
driver.close()

transform_table = pd.DataFrame(columns=["year", "value", "group", "bank"])
lastest_year = transform_table['year'].max()
years_found = list(map(int, scraped_table.columns[:4]))
for year in tqdm(years_found):
    if type(lastest_year)==int and year<=lastest_year:
        continue
    else:
        adding_table = scraped_table[[str(year), 'feature',  'bank']]
        adding_table.insert(0,'year_happend',[year]*len(adding_table))
        adding_table.columns = transform_table.columns
        transform_table = pd.concat([transform_table, adding_table],axis=0)
transform_table.to_csv('results/tong-quan.csv', index=False)