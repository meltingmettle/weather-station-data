import csv
import pdb

class Headquarters:
    def __init__(self):
        self.stations = {}

    def get_station(self, station_id):
        return self.stations[station_id]

    def already_has(self, station_id):
        return station_id in self.stations

    ############### SCREENING QUESTION METHODS ###############



    ############### SETUP METHODS ###############

    def add_station(self, station_id, data_point):
        new_station = Station(station_id)
        self.stations[station_id] = new_station
        return new_station

    def add_data(self, station_id, data_point):
        self.get_station(station_id).add_data(data_point)

class Station:
    def __init__(self, station_id):
        self.station_id = int(station_id)
        self.station_data = []

    def add_data(self, data_point):
        self.station_data.append(data_point)

    def __repr__(self):
        return "Station " + str(int(self.station_id))

    def __str__(self):
        return "Station " + str(int(self.station_id))

class DataHelper:
    def station_id(data_point):
        return data_point[0]

hq = Headquarters()

with open('data.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    next(csvreader)
    for row in csvreader:
        for data_point in row:
            data_point = data_point.split(',')
            data_point = list(map(lambda item: float(item), data_point))

            station_id = DataHelper.station_id(data_point)

            if hq.already_has(station_id):
                hq.add_data(station_id, data_point)
            else:
                new_station = hq.add_station(station_id, data_point)
                new_station.add_data(data_point)

print("Ready to go!")
