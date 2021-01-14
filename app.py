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
    
    return render_template("index.html", country=strs, country_code=js['country_code'], 
    city=js['city'], cases=data["confirmed"], a_cases=data["active"], death_num=data["deaths"], 
    recov=data["recovered"], condition=condition, info_url=s_url)

@app.route('/all')
def all_countries():
    covid = Covid()
    #tabl = ""
    countries = covid.list_countries()
    
    headings = ("Country", "Confirmed Cases", "Active Cases", "Deaths", "Recovered")
    info = []
    row = []
    count = 0
    for c in countries:
        if count != 0:
            if count % 4 == 0:
                info.append(row)
                row = []

            row.append(c['name'])
        else:
            row.append(c['name'])
        
        count += 1
    
    if len(row) != 0:
        info.append(row)
        row = []

    # for c in countries:
    #     print(c)
    #     #data = covid.get_status_by_country_name(c['name'])
    #     # row = (c['name'], str(data["confirmed"]), str(data["active"]), str(data["deaths"]), str(data["recovered"]))
    #     row = c['name']
    #     info.append(row)
    #     print(row)
    #     #tabl = tabl + row

    return render_template("all.html", info=info)

@app.route('/redi')
def redirect_to_data():
    return redirect(s_url)


@app.route('/<name>')
def hello_name(name):
    
    covid = Covid()
    try:
        data = covid.get_status_by_country_name(name)
    except:
        pass
    
    condition = False
    vac_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/locations.csv'
    s = requests.get(vac_url).content
    c = pd.read_csv(io.StringIO(s.decode('utf-8')))
    count = 0
    if name == 'US':
        for f in c['location']:
            if (f == 'United States'):
                condition = True
                break
            count += 1
        
        try:
            global s_url 
            s_url = c['source_website'][count]
        except:
            pass

        return render_template("name.html", country='United States', cases=data["confirmed"], a_cases=data["active"], death_num=data["deaths"], 
        recov=data["recovered"], condition=condition, info_url=s_url)
    else:
        for f in c['location']:
            if (f == name):
                condition = True
                break
            count += 1
        
        try:
            #global s_url 
            s_url = c['source_website'][count]
        except:
            pass

        return render_template("name.html", country=name, cases=data["confirmed"], a_cases=data["active"], death_num=data["deaths"], 
        recov=data["recovered"], condition=condition, info_url=s_url)
   
    
    
    
    return "Hello {}!".format(name)

if __name__ == '__main__':
    #app.run()
    #print(os.environ['APP_SETTINGS'])
    app.run()