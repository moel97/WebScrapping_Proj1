from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib
import pandas as pd
import openpyxl

#gets infos about the products from the prduct's page
def getInfos(sPageLink):
    print(f'link : {sPageLink}')
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",  'accept-language': 'de'}
    page = requests.get(sPageLink, headers=headers)                                                                                                 #get the page in html
    soup1 = BeautifulSoup(page.content,"html.parser")                                                                                               #gets the html code
    soup2 = BeautifulSoup(soup1.prettify(),"html.parser")                                                                                           #prettify the html code
    try:
        title = soup2.find(id= "productTitle").get_text().strip()                                                                                       #get title
        price = soup2.find(class_="a-offscreen").get_text().strip()                                                                                     #get price
        seperator = soup2.find(class_="a-price-decimal").get_text().strip()
        price = price.replace("€", "")
        if seperator == ",":
            price = price.replace(",", ".")
        else:
            price = price.replace(",", "")
        print(price)
        price = float(price)
        traderName = soup2.find(id= "bylineInfo").get_text().strip()                                                                                    #get trader/Brand name
    except:
        title= "not found try the link"
        price = 00
        traderName = ""
    infos = [title,price,traderName]
    return infos

#gets all the links of products in the search page of amazon
def getlinks(sPageLink):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
    page = requests.get(sPageLink, headers=headers)  # get the page in html
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")
    href = soup2.find_all('a',class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal",href=True)
    links=[]
    for link in href:
       links.append("https://www.amazon.de"+link['href'])
    print(links)
    return (links)

#takes a data frame and filters it to get only what's between 300 and 500 €
def filtering(df):
    df = df[(df["price"]>300) & (df["price"]<500)]
    return df


#____________________________________________________________________________  MAIN


while(True):
    sSearchPage = "https://www.amazon.de/s?k=e+scooter+mit+stra%C3%9Fenzulassung&crid=22B9GN2PQ1669&sprefix=e+scootermit+%2Caps%2C479&ref=nb_sb_ss_ts-doa-p_1_13"
    links = getlinks(sSearchPage)
    df = pd.DataFrame()
    for link in links:
        infos = getInfos(link)
        infos.append(link)
        df = df._append(pd.DataFrame([infos], columns=["name", "price", "Trader/Brand", "Webpage"]), ignore_index=True)
        print(df)

    df = filtering(df)
    print(df)
    with pd.ExcelWriter(
            "EscootersToDay.xlsx") as writer:                                                                                                            # write the data frame to exceltable
        df.to_excel(writer, sheet_name="today's info")
    time.sleep(86400)



