"""Lists out the race winners per year"""
__author__ = "Arya"

import requests
import json
from typing import Dict
from typing import List

def main() -> None:
    year: int = int(input("enter a year between 1950 and the current year: "))
    race_winners_of_year(year)
    
def race_winners_of_year(year: int) -> None:
    if (year < 1950 or year > 2022):
        raise ValueError("please enter a year after 1950 and upto the current year")
    race_num: int = num_races_in_year(year)
    i: int = 1 # 0 and 1 are both the first race in the data base
    while (i < race_num + 1):
        url: str = "http://ergast.com/api/f1/" + str(year) + "/" + str(i) + "/results.json"
        responce = requests.get(url)
        #print(responce.status_code)  #200 = successful
        data: str = json.dumps(responce.json(), sort_keys=True, indent=4)        #turns the json str into a python str
        #print(data)
        data_one = json.loads(data)
        name: str = data_one["MRData"]["RaceTable"]["Races"][0]["Circuit"]["circuitName"]
        location: str = data_one["MRData"]["RaceTable"]["Races"][0]["Circuit"]["Location"]["country"]
        winner: str = data_one["MRData"]["RaceTable"]["Races"][0]["Results"][0]["Driver"]["familyName"]
        print(winner + " won at the " + name + " in " + location)
        i += 1
    return

def num_races_in_year(year: int) -> int:
    url: str = "http://ergast.com/api/f1/" + str(year) + ".json"
    responce_one = requests.get(url)
    data: str = json.dumps(responce_one.json(), sort_keys=True, indent=4)        #turns the json str into a python str
    data_one = json.loads(data)
    return len(data_one["MRData"]["RaceTable"]["Races"])

def all_winners_ever() -> None:
    i: int = 1950
    while ( i < 2022):
        print("In the " + str(i) + " season: ") 
        race_winners_of_year(i)
        print("")
        i += 1

if __name__ == "__main__":
    main()