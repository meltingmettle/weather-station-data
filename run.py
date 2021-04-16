from solutions import *
import csv

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
