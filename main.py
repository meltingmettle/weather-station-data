import csv
import pdb

class Headquarters:
    def __init__(self):
        self.stations = {}

    def get_station(self, station_id):
        return self.stations[station_id]

    def already_has(self, station_id):
        return station_id in self.stations

    ############### SCREENING QUESTION METHODS #################################

    def lowest_temperature(self):
        lowest_temperature_station_id = None
        lowest_temperature_date = -1
        lowest_temperature = float('inf')

        for station_id in self.stations:
            station = self.get_station(station_id)
            local_lowest, local_date = station.find_lowest_temperature_and_date()
            if local_lowest < lowest_temperature:
                lowest_temperature = local_lowest
                lowest_temperature_date = local_date
                lowest_temperature_station_id = station_id

        print("The lowest temperature recorded is " + str(lowest_temperature) + " Celsius, recorded at Station " + str(lowest_temperature_station_id) + " on " + str(lowest_temperature_date))
        return {"Station ID:": lowest_temperature_station_id, "Date:": lowest_temperature_date}


    # OOP solutions just for fun

    # A simple solution which measures the lowest temperature as data is imported
    def lowest_temperature_oop_solution(self):
        return DataHelper.lowest_temperature()

    # Another solution which I re-implemented later as this one was trivially easy
    def fluctuation_station_oop_solution(self):
        highest_fluctuating_station_id = 68
        highest_fluctation = 0

        for station_id in self.stations:
            station_fluctuation = self.get_station(station_id).get_fluctuation()
            if station_fluctuation > highest_fluctation:
                highest_fluctuating_station_id = station_id
                highest_fluctation = station_fluctuation
        print("Station " + str(highest_fluctuating_station_id) + " recorded the highest fluctuation of " + str(highest_fluctation))
        return highest_fluctuating_station_id
    ############### SETUP METHODS ##############################################

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
        self.fluctuation = 0

    def add_data(self, data_point):
        self.fluctuation += abs(DataHelper.temperature(data_point))
        self.station_data.append(data_point)

    def get_station_data(self):
        return self.station_data

    def get_fluctuation(self):
        return self.fluctuation

    def find_lowest_temperature_and_date(self):
        lowest_temperature = float('inf')
        lowest_temperature_date = 0

        for data_point in self.station_data:
            data_temperature = DataHelper.temperature(data_point)
            if data_temperature < lowest_temperature:
                lowest_temperature = data_temperature
                lowest_temperature_date = DataHelper.date(data_point)
        return lowest_temperature, lowest_temperature_date

    def __repr__(self):
        return "Station " + str(int(self.station_id))

    def __str__(self):
        return "Station " + str(int(self.station_id))

class DataHelper:
    lowest_recorded_temperature = [-1, -1, float('inf')]

    def station_id(data_point):
        return int(data_point[0])

    def date(data_point):
        return data_point[1]

    def temperature(data_point):
        return data_point[2]

    def parse(row):
        # >>> row = ['2, 2020.123, 4']
        # >>> parse(row)
        # [2, 2020.123, 4]

        row = row[0].split(',')
        row = list(map(lambda item: float(item), row))

        return row

    def consider_lowest(data_point):
        if DataHelper.temperature(data_point) < DataHelper.temperature(DataHelper.lowest_recorded_temperature):
            DataHelper.lowest_recorded_temperature = data_point

    def lowest_temperature():
        station_id = DataHelper.station_id(DataHelper.lowest_recorded_temperature)
        date = DataHelper.date(DataHelper.lowest_recorded_temperature)
        temperature_c = DataHelper.temperature(DataHelper.lowest_recorded_temperature)

        print("The lowest temperature recorded is " + str(temperature_c) + " Celsius, recorded at Station " + str(station_id) + " on " + str(date))
        return {"Station ID:": station_id, "Date:": date}

################################################################################

hq = Headquarters()

with open('data.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    next(csvreader)
    for row in csvreader:
        data_point = DataHelper.parse(row)
        station_id = DataHelper.station_id(data_point)

        DataHelper.consider_lowest(data_point)

        if hq.already_has(station_id):
            hq.add_data(station_id, data_point)
        else:
            new_station = hq.add_station(station_id, data_point)
            new_station.add_data(data_point)


print(hq.lowest_temperature())
print("OOP Solutions")
print(hq.lowest_temperature_oop_solution())
print(hq.fluctuation_station_oop_solution())

print("Ready to go!")
