import yfinance as yf
import requests
from fuzzywuzzy import fuzz
import csv

f = open('market_cap.csv', 'w')
writer = csv.writer(f)
writer.writerow(['Company', 'Market Cap'])

def company_name_to_ticker(company_name):
    url = f'https://financialmodelingprep.com/api/v3/search?query={company_name}&limit=10&apikey=demo'
    response = requests.get(url).json()
    if len(response) == 0:
        return None
    else:
        try:
            best_match = max(response, key=lambda x: fuzz.token_set_ratio(company_name.lower(), x['name'].lower()))
            get_market_cap(best_match['symbol'])
            return None
        
        except:
            print(f"Error with {company_name}")
            return None




def getCompanies (file_name):
    companies = []
    with open(file_name, newline='') as f:
        data=f.readlines()
        for line in data:
            if line != '\r\n':
                companies.append(company_name_to_ticker(line.replace('\r\n','')))
    return companies



def get_market_cap(company):     
    ticker = yf.Ticker(company)
    market_cap = ticker.info["marketCap"] 
    print(f"{company}: {market_cap}")
    writer.writerow([company, market_cap])


companies = getCompanies("./companies.txt")
f.close()