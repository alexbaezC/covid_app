from covid import Covid
from prettytable import PrettyTable


table = PrettyTable(["Country", "Confirmed", "Active", "Deaths", "Recovered"])
covid = Covid()

countries = covid.list_countries()
num = len(countries)
count = 0

for c in countries:
    name = c["name"]
    data = covid.get_status_by_country_name(name)
    table.add_row([name, data["confirmed"], data["active"], data["deaths"], data["recovered"]])
    count += 1
    print("Download ", (count/num)*100, "%")
print(table)
