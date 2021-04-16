from solutions import *

# For the sake of time I'm manually testing happy-paths.  I'd use unittest otherwise.

def test_pointify():
    output = DataHelper.pointify(['1, 2, 3.33'])
    expected_result = Point([1, 2, 3.33])

    assert isinstance(output, Point)

    # TODO add edge case handling
    assert output.station_id == expected_result.station_id
    assert output.date == expected_result.date
    assert output.temperature == expected_result.temperature

def test_solution_api():
    station_1_data = [[1, 2000, -10], [1, 2005, 0], [1, 2010, 10]]
    station_2_data = [[2, 2000, -20], [2, 2005, 20], [2, 2010, 25]]
    station_3_data = [[3, 2001, 25], [3, 2006, 20], [3, 2011, 1025]]
    station_4_data = [[4, 2005, 0], [4, 2010, 30], [4, 2000, -20], [4, 2015.3, -273]]

    data_block = []
    data_block.extend(station_2_data)
    data_block.extend(station_1_data)
    data_block.extend(station_4_data)
    data_block.extend(station_3_data)


    for data_point in data_block:
        hq.add_point(Point(data_point))

    # Test the lowest temperature
    assert SolutionsAPI.part_1() == {'Station ID:': 4, 'Date:': 2015.3}

    # Test the highest overall fluctuation
    assert SolutionsAPI.part_2() == 3

    # Test basic happy-path
    assert SolutionsAPI.part_3(1999, 2010) == 2
    assert SolutionsAPI.part_3(2001, 2006) == 3

    # Test inclusive start/end
    assert SolutionsAPI.part_3(2010, 2010) == 4

    # Test the highest overall fluctuation, identical to part_2
    assert SolutionsAPI.part_3(1900, 2022) == 3

    # TODO validate inputs and add handling for error cases

    # Undefined behavior
    assert SolutionsAPI.part_3(0, 200) == None
    assert SolutionsAPI.part_3(2002, 2003) == None

test_pointify()
test_solution_api()
print("All test cases passed!")
