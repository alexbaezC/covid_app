from covid import Covid
from tqdm import tqdm
import requests
from prettytable import PrettyTable
import os
import sys
import time,sys

def typer_style(str):
    for c in str:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

#ip = '186.7.54.50'
os.system('cls' if os.name=='nt' else 'clear')
print("             ██████  ██████  ██    ██ ██ ██████              ")
print("            ██      ██    ██ ██    ██ ██ ██   ██             ")
print("            ██      ██    ██ ██    ██ ██ ██   ██             ")
print("            ██      ██    ██  ██  ██  ██ ██   ██             ")
print("             ██████  ██████    ████   ██ ██████              ")
print("                                                             ")
print("                                                             ")
print("████████ ██████   █████   ██████ ██   ██ ███████ ██████      ")
print("   ██    ██   ██ ██   ██ ██      ██  ██  ██      ██   ██     ")
print("   ██    ██████  ███████ ██      █████   █████   ██████      ")
print("   ██    ██   ██ ██   ██ ██      ██  ██  ██      ██   ██     ")
print("   ██    ██   ██ ██   ██  ██████ ██   ██ ███████ ██   ██     ")
print("                                                             ")
print("                                                             ")
url = 'http://api.ipstack.com/check?access_key=a2acd36ecdb97d72073d65b752df8eb3'
#ip+'?access_key=a2acd36ecdb97d72073d65b752df8eb3'
r = requests.get(url)
js = r.json()
c1 = "Current Country code: " + js['country_code'] + '\n'
typer_style(c1)
c2 = "Current Country name: " + js['country_name'] + '\n'
typer_style(c2)
c3 = "Current City name: " + js['city'] + '\n'
typer_style(c3)
print('\a')
name = js['country_name']

table = PrettyTable(["Country", "Confirmed", "Active", "Deaths", "Recovered"])
covid = Covid()

countries = covid.list_countries()
num = len(countries)
count = 0

try:
    data = covid.get_status_by_country_name(name)
except:
    data = covid.get_status_by_country_name(js['country_code'])

table.add_row([name, data["confirmed"], data["active"], data["deaths"], data["recovered"]])

print(table)
command_list = PrettyTable(["Commands", "Function"])
command_list.add_row(["help", "Prints the list of commands"])
command_list.add_row(["quit", "Quits the program"])
command_list.add_row(["info", "Prints Covid informarion in the current country"])
command_list.add_row(["list", "Prints a list of countries starting"])
command_list.add_row(["check", "Presents Covid 19 information about a country"])
print(command_list)
while(True):
    command = input("> ")
    if command == "help":
        print(command_list)
    
    if command == "quit":
        break 

    if command == "info":
        h = PrettyTable(["Country", "Confirmed", "Active", "Deaths", "Recovered"])
        data = covid.get_status_by_country_name(name)
        h.add_row([name, data["confirmed"], data["active"], data["deaths"], data["recovered"]])
        print(h)
    
    if command == "list":
        country_name = input("Countries that start with: ")
        t = PrettyTable(["Country"])
        for c in countries:
            if c['name'].startswith(country_name):
                t.add_row([c['name']])
        
        print(t)
        
    if command == "check":
        country_name = input("Country: ")
        t = PrettyTable(["Country", "Confirmed", "Active", "Deaths", "Recovered"])
        data_check = covid.get_status_by_country_name(country_name)
        t.add_row([country_name, data_check["confirmed"], data_check["active"], data_check["deaths"], data_check["recovered"]])
        print(t)
