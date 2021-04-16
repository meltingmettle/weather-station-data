import csv
import pdb

class SolutionsAPI:
    def part_1():
        return hq.fetch_lowest_temperature_station_date()

    def part_2():
        return hq.fetch_highest_fluctuation_station_id()

    def part_3(start, end):
        # TODO add error handling/input validation
        return hq.fetch_highest_fluctuation_station_id(start, end)

    def part_1_v1():
        return hq.lowest_temperature_oop_solution()

    def part_2_v1():
        return hq.fluctuation_station_oop_solution()

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

        print("The lowest temperature recorded is " + str(lowest_recorded.temperature) + " Celsius, recorded at Station " + str(lowest_recorded.station_id) + " on " + str(lowest_recorded.date))
        return {"Station ID:": lowest_recorded.station_id, "Date:": lowest_recorded.date}

    # Assume that the data is not sorted.
    # I could also have stored the data in sorted arrays but the benefits would be only marginally worth the additional complexity
    def fetch_highest_fluctuation_station_id(self, start=0, end=2022.000):
        highest_fluctuation = Fluctuation(-1, start, end, 0)

        for station in self.stations.values():
            station_fluctuation = station.fluctuation_over_window(start, end)

            if station_fluctuation.is_higher_than(highest_fluctuation) and station_fluctuation.is_over_the_same_window_as(highest_fluctuation):
                highest_fluctuation = station_fluctuation

        if highest_fluctuation.station_id == -1:
            print("No data collected from the time window between " + str(start) + " and " + str(end))
            return None
            
        print("Station " + str(highest_fluctuation.station_id) + " saw the most temperature fluctuation of " + str(highest_fluctuation.value) + " between the dates of " + str(highest_fluctuation.start) + " and " + str(highest_fluctuation.end))
        return highest_fluctuation.station_id

    # Import-based solutions for Part 1 and Part 2 just for fun
    def lowest_temperature_oop_solution(self):
        return DataHelper.lowest_temperature_station_date()

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
        self.station_id           = int(station_id)
        self.station_data         = []
        # Instance attribute for the Part 2's import-based solution
        self.fluctuation          = 0

    def add_data(self, point):
        self.fluctuation += abs(point.temperature)
        self.station_data.append(point)

    def get_station_data(self):
        return self.station_data

    def find_lowest_temperature_and_date(self):
        lowest_recorded_point = Point()

        for point in self.station_data:
            if point.temperature < lowest_recorded_point.temperature:
                lowest_recorded_point = point

        return lowest_recorded_point

    def fluctuation_over_window(self, start, end):
        aggregate_fluctuation = 0

        for point in self.station_data:
            if start < point.date < end:
                aggregate_fluctuation += abs(point.temperature)

        self.windowed_fluctuation = Fluctuation(self.station_id, start, end, aggregate_fluctuation)
        return self.windowed_fluctuation

    def __repr__(self):
        return "Station " + str(int(self.station_id))

    def __str__(self):
        return "Station " + str(int(self.station_id))

class Point:
    def __init__(self, data_point=[-1, -1, float('inf')]):
        self.station_id  =   data_point[0]
        self.date        =   data_point[1]
        self.temperature =   data_point[2]

# This is beyond overkill for what we're doing right now, but it's much more extendable
class Fluctuation:
    def __init__(self, station_id, start, end, value):
        self.station_id = station_id
        self.start      = start
        self.end        = end
        self.value      = value

    def is_higher_than(self, second_fluctuation):
        return self.value > second_fluctuation.value

    def is_over_the_same_window_as(self, second_fluctuation):
        return self.start == second_fluctuation.start and self.end == second_fluctuation.end

class DataHelper:
    lowest_recorded_point = Point()

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
    print("Importing data...")
    for row in csvreader:
        point = DataHelper.pointify(row)

        hq.add_point(point)

        # 'sidecar-consumer' for Part 1's OOP solution
        DataHelper.consider_lowest(point)

print("Ready to go!")


############ FOR TESTING CONVINIENCE, NOT PRODUCTIONIZABLE #####################
while True:
    part = input("Type a number between 1-3 to run the Part's corresponding method:")

    if int(part) == 1:
        SolutionsAPI.part_1()
    elif int(part) == 2:
        SolutionsAPI.part_2()
    elif int(part) == 3:
        start = input("Please input a correctly-formatted start date: ")
        end = input("Please input a correctly-formatted end date: ")
        SolutionsAPI.part_3(float(start), float(end))
