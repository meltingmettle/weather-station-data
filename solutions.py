from main import *

hq = Headquarters()

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
