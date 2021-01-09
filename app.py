import os
import io
import requests
from covid import Covid
from flask import Flask, redirect, url_for, render_template
import pandas as pd


app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])

s_url = 'https://www.google.com/'

@app.route('/')
def hello():
    url = 'http://api.ipstack.com/check?access_key=a2acd36ecdb97d72073d65b752df8eb3'
    r = requests.get(url)
    js = r.json()
    strs = js['country_name']
    covid = Covid()
    try:
        data = covid.get_status_by_country_name(strs)
    except:
        data = covid.get_status_by_country_name(js['country_code'])
    
    condition = False
    vac_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/locations.csv'
    s = requests.get(vac_url).content
    c = pd.read_csv(io.StringIO(s.decode('utf-8')))
    count = 0
    for f in c['location']:
        if (f == strs):
            condition = True
            break
        count += 1
    try:
        global s_url 
        s_url = c['source_website'][count]
    except:
        pass
    print('here')
    return render_template("index2.html", country=strs, country_code=js['country_code'], 
    city=js['city'], cases=data["confirmed"], a_cases=data["active"], death_num=data["deaths"], 
    recov=data["recovered"], condition=condition, info_url=c['source_website'][count])

@app.route('/redi')
def redirect_to_data():
    return redirect(s_url)


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    #app.run()
    #print(os.environ['APP_SETTINGS'])
    app.run()