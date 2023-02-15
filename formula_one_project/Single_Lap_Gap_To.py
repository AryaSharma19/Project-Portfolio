"""Calculates the Gap over a single to either the leader or to a specific driver"""
__author__ = "Arya"

import requests, json, time, math, datetime
from typing import Dict, List
import matplotlib.pyplot as plt
import numpy as np

def main() -> None:
    #should prob start positions all race with grid position, should be availble the same query as num_laps_in_race
    #positions_all_race and gaps_all_race should be called no more than twice an hour to avoid the 24 hr lock out
    gaps: Dict[str, List[float]] = gaps_all_race(2020, 4)
    plot(gaps)
    #get_lap(2022, 2, 10)


def gap_to_driver(year: int, round: int, lap: int, total_time: Dict[str, float], normalized_driver: str) -> Dict[str, float]:
    url: str = "http://ergast.com/api/f1/" + str(year) + "/" + str(round) + "/laps/" +str(lap) + ".json"
    responce = requests.get(url)
    #print(responce.status_code)  #200 = successful
    data: str = json.dumps(responce.json(), sort_keys=True, indent=4)        #turns the json str into a python str
    #print(data)
    data_one = json.loads(data)
    gap: Dict[str, float] = {}
    for i in data_one["MRData"]["RaceTable"]["Races"][0]["Laps"][0]["Timings"]:
        gap[i["driverId"]] = str_time_to_float_secs(i["time"])
    if normalized_driver == "first_lap" or normalized_driver == "last_lap":
        for i in gap:
            gap[i] = 0
        return gap
    for i in gap:
        total_time[i] += gap[i]
    for i in gap:
        gap[i] = total_time[next(iter(gap))] - total_time[i]        #flipped this might need to change it back #changed total_time[normalized_driver]
    for i in gap:
        gap[i] = math.floor(gap[i] * 1000 ) / 1000
    return gap

def gaps_all_race(year: int, round: int, selected: List[str] = [], selected_out: List[str] = []) -> Dict[str, List[float]]:
    """Takes in year, round, lap, [driverId] selected drivers (optional), [driverID] selected out drivers (optional).
    use get lap of the first lap to get driverIDs as needed"""
    total_gap: Dict[str, List[float]] = {}
    total_time: Dict[str, float] = gap_to_driver(year, round, 1, {}, "first_lap")
    time.sleep(1)
    num_laps: int = int (num_laps_in_race(year, round))
    normalized_driver: str = next(iter(gap_to_driver(year, round, num_laps, {}, "last_lap"))) #returns the driver key of the winning driver
    time.sleep(1)
    i: int = 1
    while i <= num_laps:
        time.sleep(0.4)
        print("Estimated time untill results: " + str(math.floor(num_laps - i) / 0.4) + " Seconds")
        gaps: Dict[str, float] = gap_to_driver(year, round, i, total_time, normalized_driver)
        for driver in gaps:
            if not driver in total_gap:
                total_gap[driver] = []
                total_gap[driver].append(gaps[driver])
            else:
                total_gap[driver].append(gaps[driver])
        i += 1
    if selected != []:
        results: Dict[str, List[float]] = {}
        for key in selected:
            try:
                results[key] = total_gap.pop(key)
            except KeyError:
                print("the following driverID is incorrect or the driver did not drive past the first lap of the race: " + key)
        return results
    if selected_out != []:
        for key in selected_out:        
            try:
                total_gap.pop(key)
            except KeyError:
                print("the following driverID is incorrect or the driver did not drive past the first lap of the race: " + key)
    return total_gap

def position(year: int, round: int, lap: int) -> Dict[str, int]:
    """Returns the positions for the given lap of the given round and year. Accepts laps and rounds starting at 1."""
    url: str = "http://ergast.com/api/f1/" + str(year) + "/" + str(round) + "/laps/" +str(lap) + ".json"
    responce = requests.get(url)
    #print(responce.status_code)  #200 = successful
    data: str = json.dumps(responce.json(), sort_keys=True, indent=4)        #turns the json str into a python str
    #print(data)
    data_one = json.loads(data)
    lap_position: Dict[str, int] = {}
    #print(data_one["MRData"]["RaceTable"]["Races"][0]["Laps"][0]["Timings"])
    for i in data_one["MRData"]["RaceTable"]["Races"][0]["Laps"][0]["Timings"]:
        lap_position[i["driverId"]] = i["position"]
    #print(lap_position)
    return lap_position

def positions_all_race(year: int, round: int) -> Dict[str, List[int]]:
    total_positions: Dict[str, List[int]] = {}
    first_lap_positions: Dict[str, int] = position(year, round, 1)    #function should work without this, test this later
    for driver in first_lap_positions:   #function should work without this, test this later
        total_positions[driver] = []
        total_positions[driver].append(first_lap_positions[driver])
    i: int = 2
    time.sleep(1)
    num_laps: int = int (num_laps_in_race(year, round))
    while i <= num_laps:
        time.sleep(0.4)
        print("Estimated time untill results: " + str(math.floor(num_laps - i) / 0.4) + " Seconds")
        positions: Dict[str, int] = position(year, round, i)
        for driver in positions:
            if not driver in total_positions:
                total_positions[driver] = []
                total_positions[driver].append(positions[driver])
            else:
                total_positions[driver].append(positions[driver])
        i +=1
    return total_positions

def num_laps_in_race(year: int, round: int) -> int:
    """Gives the number of laps for the race in the given year and round. Actually returns the # of completed laps by the race winner"""
    url: str = "http://ergast.com/api/f1/" + str(year) + "/" + str(round) + "/results.json"
    responce = requests.get(url)
    #print(responce.status_code)  #200 = successful
    data: str = json.dumps(responce.json(), sort_keys=True, indent=4)        #turns the json str into a python str
    data_one = json.loads(data)
    num_laps: int = data_one["MRData"]["RaceTable"]["Races"][0]["Results"][0]["laps"]
    return num_laps

def str_time_to_float_secs(time: str) -> float:
    """Takes in "MIN:SEC.MiLLISEC" returns total seconds as a float"""
    date_time = datetime.datetime.strptime(time, "%M:%S.%f")
    a_timedelta = date_time - datetime.datetime(1900, 1, 1)
    seconds: float = a_timedelta.total_seconds()
    return seconds

def x_values(num: int) -> List[float]:
    i: int = 1
    list: List[float] = []
    while i <= num:
        list.append(float(i))
        i += 1
    return list 

def plot(data: Dict[str, List[float]]) -> None:
    for key in data:
        xpoints = np.array(x_values(len(data[key])))
        ypoints = np.array(data[key])
        plt.plot(xpoints, ypoints, label= key)
    plt.legend(loc="lower left")
    plt.xlabel("lap")
    plt.ylabel("gap to leader")
    plt.show()
    return

def get_lap(year: int, round: int, lap: int) -> None:
    url: str = "http://ergast.com/api/f1/" + str(year) + "/" + str(round) + "/laps/" +str(lap) + ".json"
    responce = requests.get(url)
    #print(responce.status_code)  #200 = successful
    data: str = json.dumps(responce.json(), sort_keys=True, indent=4)        #turns the json str into a python str
    #print(data)
    data_one = json.loads(data)
    for i in data_one["MRData"]["RaceTable"]["Races"][0]["Laps"][0]["Timings"]:
        print(i["driverId"] + " : " + i["time"])

if __name__ == "__main__":
    main()