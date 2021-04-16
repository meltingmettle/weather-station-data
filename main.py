import csv
import pdb

class Headquarters:
    def __init__(self):
        self.stations = {}

    def get_station(self, station_id):
        return self.stations[station_id]

    ############### SCREENING QUESTION METHODS #################################

    def fetch_lowest_temperature_station_date(self):
        lowest_recorded = Point([-1, -1, float('inf')])

        for station_id in self.stations:
            station = self.get_station(station_id)

            station_lowest = station.find_lowest_temperature_and_date()

            if station_lowest.temperature < lowest_recorded.temperature:
                lowest_recorded = station_lowest

        return {"Station ID:": lowest_recorded.station_id, "Date:":lowest_recorded.date}

    # OOP solutions

    # A simple solution which measures the lowest temperature as data is imported
    def lowest_temperature_oop_solution(self):
        return DataHelper.lowest_temperature_station_date()

    # Another OOP solution
    def fluctuation_station_oop_solution(self):
        highest_station = Station(-1)

        for station in self.stations.values():
            if station.fluctuation > highest_station.fluctuation:
                highest_station = station

        print("Station " + str(highest_station.station_id) + " recorded the highest fluctuation of " + str(highest_station.fluctuation))
        return highest_station.station_id

    ############### IMPORT METHODS ##############################################

    def add_point(self, point):
        station_id = point.station_id
        if self.already_has(station_id):
            self.add_data(station_id, point)
        else:
            new_station = self.add_station(station_id, point)
            new_station.add_data(point)

    def already_has(self, station_id):
        return station_id in self.stations

    def add_station(self, station_id, point):
        new_station = Station(station_id)
        self.stations[station_id] = new_station
        new_station.add_data(point)

        return new_station

    def add_data(self, station_id, point):
        self.get_station(station_id).add_data(point)

class Station:
    def __init__(self, station_id):
        self.station_id     = int(station_id)
        self.station_data   = []
        self.fluctuation    = 0

    def add_data(self, point):
        self.fluctuation += abs(point.temperature)
        self.station_data.append(point)

    def get_station_data(self):
        return self.station_data

    def find_lowest_temperature_and_date(self):
        lowest_recorded_point = Point([-1, -1, float('inf')])

        for point in self.station_data:
            if point.temperature < lowest_recorded_point.temperature:
                lowest_recorded_point = point

        return lowest_recorded_point

    def __repr__(self):
        return "Station " + str(int(self.station_id))

    def __str__(self):
        return "Station " + str(int(self.station_id))

class Point:
    def __init__(self, data_point):
        self.station_id  =   data_point[0]
        self.date        =   data_point[1]
        self.temperature =   data_point[2]


class DataHelper:
    lowest_recorded_point = Point([-1, -1, float('inf')])

    def pointify(row):
        row = row[0].split(',')
        row = list(map(lambda item: float(item), row))

        return Point(row)

    def consider_lowest(point):
        if point.temperature < DataHelper.lowest_recorded_point.temperature:
            DataHelper.lowest_recorded_point = point

    def lowest_temperature_station_date():
        lowest_point = DataHelper.lowest_recorded_point

        station_id =    lowest_point.station_id
        date =          lowest_point.date
        temperature_c = lowest_point.temperature

        print("The lowest temperature recorded is " + str(temperature_c) + " Celsius, recorded at Station " + str(station_id) + " on " + str(date))
        return {"Station ID:": station_id, "Date:": date}

################################################################################

hq = Headquarters()

with open('data.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    next(csvreader)
    for row in csvreader:
        point = DataHelper.pointify(row)

        hq.add_point(point)

        # 'sidecar-consumer' for Part 1's OOP solution
        DataHelper.consider_lowest(point)


print(hq.fetch_lowest_temperature_station_date())
print("OOP Solutions")
print(hq.lowest_temperature_oop_solution())
print(hq.fluctuation_station_oop_solution())

print("Ready to go!")
