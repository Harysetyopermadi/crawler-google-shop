import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd







def opened_link_chrome(url_search):
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    options.add_argument('--disable-blink-features=AutomationControlled') 
    
    #options.add_argument("start-maximized")

    options.add_argument("disable-infobars")

    options.add_argument("--disable-extensions")
    
    #options.add_argument('--use_subprocess')
    driver = webdriver.Chrome(options=options)
    driver.get(url_search)
    driver.maximize_window()
    #time.sleep(40)
    page=1
    df3=pd.DataFrame()
    while True:
        
        try:
            element_next = driver.find_element(By.ID, 'pnnext')
        #if element_next:
            print("element next ada") 
            content = driver.page_source
            data = BeautifulSoup(content, 'html.parser')
            df2=pd.DataFrame()
            for area in data.find_all('div', class_="sh-dgr__content"):
                try:
                    Judul=area.find('h3', class_="tAxDx").get_text()
                    Judul=Judul.replace('|','')
                except:
                    Judul="Tidak Ada Element Title"
                
                try:
                    detailsingkat=area.find('div', class_="F7Kwhf bzCQNe t5OWfd").get_text()
                    detailsingkat=detailsingkat.replace('|','')
                    
                except:
                    detailsingkat="Tidak Ada Detail Singkat"
                
                try:
                    harga=area.find('span', class_="a8Pemb OFFNJ").get_text()
                    harga=harga.replace('|','')
                    
                except:
                    harga="Tidak Ada Harga"
                
                try:
                    link=area.find('div', class_="aULzUe IuHnof").get_text()
                    link=link.replace('|','')
                    
                except:
                    link="Tidak Ada Link"
                
                try:
                    Pengiriman=area.find('div', class_="vEjMR").get_text()
                    Pengiriman=Pengiriman.replace('|','')
                    
                except:
                    Pengiriman="Tidak Ada Element Pengiriman"
                    
                try:
                    review=area.find('span', class_="QIrs8").get_text()
                    review=review.replace('|','')
                    
                except:
                    review="Tidak Ada Review"
                # print(Judul)
                # print(Pengiriman) 
                # print(harga)
                # print(link)
                # print(detailsingkat)
                df1=pd.DataFrame({"Judul":[Judul],
                                 "Pengiriman":[Pengiriman],
                                 "Harga":[harga],
                                 "Link":[link],
                                 "Detail_Singkat":[detailsingkat],
                                 "Review":[review]                       
                                 })
                df2=df2.append(df1)
            df3=df3.append(df2)
            
            
            #time.sleep(10)
            element_next.click()
            print(str(page))
            page=page+1
            
        except:
            try:
                driver.find_element(By.ID, 'captcha-form')
                print("Ada Capcha")
                time.sleep(5)
            except:
                print(str(page))
                print("element next tidak ada")
                break
            
    df3=df3.replace('[.]','',regex=True)
    df3=df3.replace(',00','',regex=True)
    df3.loc[df3['Review'].str.contains('Rp'), 'Review'] = 'Tidak Ada Review'
    print(df3)
    df3.to_excel("out.xlsx")


    
    