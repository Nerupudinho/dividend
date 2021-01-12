import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import re
from datetime import date


file = "https://www1.nseindia.com/corporates/datafiles/CA_ALL_FORTHCOMING.csv"
df = pd.read_csv(file)

pricefile = "https://www1.nseindia.com/products/content/sec_bhavdata_full.csv"
pricedf = pd.read_csv(pricefile)

DivStocks=df[df["Purpose"].str.contains("Div")]
DivStocks["Dividend"]=df["Purpose"]
DivStocks.columns = [x.strip(' ') for x in DivStocks.columns]
DivStocks=DivStocks.reset_index(drop=True)

y=[]
for x in DivStocks["Dividend"] : y.append(re.findall("\d+\.?\d*", x))
DivStocks["Dividend"]=pd.DataFrame.from_records(y)


pricedf.drop_duplicates(subset='SYMBOL', inplace=True, ignore_index=True)
pricedf.columns = [x.strip(' ') for x in pricedf.columns]
pricedf = pricedf[['SYMBOL', 'CLOSE_PRICE']]
DivStocks = pd.merge(left=DivStocks, right=pricedf, left_on='Symbol', right_on='SYMBOL', how='left')
DivStocks=DivStocks[['Symbol','Purpose','Ex-Date','Dividend','CLOSE_PRICE']]
print(DivStocks)
path= "Dividends\Div_" + str(date.today())+".csv"
DivStocks.to_csv(path,  index=None, sep=',')