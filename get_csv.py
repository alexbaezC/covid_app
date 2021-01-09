import io
import requests
from covid import Covid
import pandas as pd



url="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/locations.csv"
s=requests.get(url).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')))

count = 0
for f in c['location']:
    if (f == 'United States'):
        print("found", count)
        break
    count += 1

print(c['source_website'][count])
    