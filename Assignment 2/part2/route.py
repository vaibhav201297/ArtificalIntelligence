#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: IU username here
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#

from math import tanh

def copy_state(state):
    res = []
    for segment in state:
        res.append(segment.copy())
    return res

def get_successors(state, segments):
    res = []
    possible_segments = segments[state[-1][0]]
    for segment in possible_segments:
        new_segment = copy_state(state)
        # city, street_name, length (miles), mph
        new_segment.append([segment[0], segment[3], segment[1], segment[2]])
        res.append(new_segment)
    return res

def compute_final_output(state):
    segments = state[1:]
    route_taken = []
    for segment in segments:
        route_taken.append((segment[0], "{} for {} miles".format(segment[1], segment[2])))

    return {
        "total-segments": len(segments),
        "total-miles": get_distance(state),
        "total-hours": get_hours(state),
        "total-delivery-hours": get_delivery_hours(state),
        "route-taken": route_taken
    }

def get_distance(state):
    dis = 0
    for segment in state[1:]:
        dis += segment[2]
    return dis

def get_hours(state):
    hours = 0
    for segment in state[1:]:
        hours += segment[2] / segment[3]
    return hours

def get_delivery_hours(state):
    hours = 0
    for segment in state[1:]:
        hours += segment[2] / segment[3]
        if segment[3] >= 50:
            p = tanh(segment[2]/1000)
            hours += 2*p*hours
    return hours

# !/usr/bin/env python3
import sys
from copy import deepcopy
from math import sqrt, pow, tanh, dist


def isGoal(state, end):
    return state[1] == end

def get_route(start, end, cost):
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    segments = {}

    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    #
    # return {"total-segments" : len(route_taken),
    #         "total-miles" : 51.,
    #         "total-hours" : 1.07949,
    #         "total-delivery-hours" : 1.1364,
    #         "route-taken" : route_taken}

    # Creating a dictionary for the cities
    city_gps = read_citygps()

    # Creating a dictionary for the routes/paths
    [road_segments, maxDistance, maxspeed] = read_roads_segments()


    # Initial_state = [Cost,Current City,Path, Total Time,Total Delivery hours,Total Distance]
    initial_state = [0, start, [], 0, 0, 0]
    priorityQueue = []

    priorityQueue.append(initial_state)

    visited = []
    while priorityQueue:
        priorityQueue.sort()
        present_state = priorityQueue.pop(0)

        successors = get_successor(road_segments, city_gps,present_state, maxDistance, maxspeed,end, cost)

        for state in priorityQueue:
            visited.append(state[1])

        for successor in successors:
            # check for goal state
            if isGoal(successor, end):
                # format as per the requirements
                path = successor[2]
                route_taken = []
                for nextCityName, miles, speed, highway in road_segments.get(start):
                    if nextCityName == path[0]:
                        route_taken.append((nextCityName, highway + " for " + miles + " miles"))

                for i in range(len(path) - 1):
                    for nextCityName, miles, speed, highway in road_segments.get(path[i]):
                        if nextCityName == path[i + 1]:
                            route_taken.append((nextCityName, highway + " for " + miles + " miles"))

                return {"total-segments": len(route_taken),
                        "total-miles": successor[5],
                        "total-hours": successor[3],
                        "total-delivery-hours": successor[4],
                        "route-taken": route_taken}


            elif successor[1] in visited:
                index = visited.index(visited[1])
                current_cost = priorityQueue[index][0]
                if current_cost > successor[0]:
                    priorityQueue[index] = successor

            else:
                priorityQueue.append(successor)

        visited = []


# Successor function
def get_successor(road_segments, city_gps, current_state, max_distance, max_speed, destination, cost_value):
    #get a list of possible successor states

    successors = []

    current_city = current_state[1]
    current_path = current_state[2]
    totalDeliveryTime = 0


    for next_city, miles, speed, highway in road_segments.get(current_city):
        curr_seg_length = float(miles)
        curr_speed = float(speed)

        if next_city not in current_path:
            next_cost = 0
            nextPath = deepcopy(current_path)
            nextPath.append(next_city)

            # cost calculation
            t_trip = current_state[3]
            t_road = curr_seg_length / curr_speed

            # total time
            totalPath = len(nextPath)
            totalTime = current_state[3] + t_road
            totalDistance = current_state[5] + curr_seg_length
            totalDeliveryTime = current_state[4] + mistake_probability(t_road,t_trip,curr_speed,curr_seg_length)

            #get nextCost based on cost value

            if cost_value == "distance":
                heuristic_cost = manhatten_dist(city_gps, next_city, destination)
                next_cost = totalDistance + heuristic_cost

            # Finding f(time) = g(total time travelled till now) + h( time to be travelled from current state till end)
            elif cost_value == "time":
                heuristic_cost = euclidean_dist(city_gps, next_city, destination) / max_speed
                next_cost = totalTime + heuristic_cost

            # Finding f(segments) = g(total segments travelled till now) + h( segments to be travelled from current state till end)
            elif cost_value == "segments":
                heuristic_cost = euclidean_dist(city_gps, next_city, destination) / max_distance
                next_cost = totalPath + heuristic_cost

            # Finding the delivery
            elif cost_value == "delivery":
                heuristic_cost = euclidean_dist(city_gps, next_city, destination) / max_speed
                next_cost = totalDeliveryTime + heuristic_cost

            # nextCost = getCost(cityDict, costFunction, maxDistanceBetweenCities, maxSpeed, nextCity,
            #                    totalPath, end, totalTime, totalAccidentFactor, totalDistance)

            successors.append([next_cost, next_city, nextPath,
                               totalTime, totalDeliveryTime,totalDistance])

    return successors


# Finding the manhattan distance between the given 2 cities
def manhatten_dist(city_gps, current_city, destination):
    # for initial state
    if city_gps.get(current_city) is None:
        return 0
    else:
        current_latitude, current_longitude = city_gps.get(current_city)
        destination_latitude, destination_longitude = city_gps.get(destination)
        return abs(float(current_latitude) - float(destination_latitude)) + abs(
            float(current_longitude) - float(destination_longitude))


# Finding the euclidian distances between the given 2 cities
def euclidean_dist(city_gps, current_city, destination):
    # for initial state
    if city_gps.get(current_city) is None:
        return 0
    else:
        current_latitude, current_longitude = city_gps.get(current_city)
        destination_latitude, destination_longitude = city_gps.get(destination)
        return sqrt(pow(float(current_latitude) - float(destination_latitude), 2) + pow( float(current_longitude) - float(destination_longitude), 2 ))


# Get the probability of this mistake happening
def mistake_probability(t_road,t_trip, speed,distance):
    if speed >= 50:
        probab  = tanh(distance/1000)
    else:
        probab = 0

    return (t_road + (probab * 2 * (t_road+t_trip)))

# Reading the file city_gps.txt into a dictionary
def read_citygps():
    city_gps = {}
    with open("city-gps.txt", "r") as file:
        for line in file:
            values = line.split()
            if len(values) == 3:
                city_gps[values[0]] = (values[1], values[2])
    return city_gps


# Reading file road_segments.txt into a dictionary
def read_roads_segments():
    road_segments = {}
    max_distance = 0
    max_speed = 0
    with open("road-segments.txt", 'r') as file:
        for line in file:
            values = line.split()
            if len(values) == 5:
                #cityA->cityB
                city_entry_map(road_segments, values[0], values[1], values[2], values[3], values[4])
                # cityB->cityA
                city_entry_map(road_segments, values[1], values[0], values[2], values[3], values[4])

                # Get maximum distance between any city  existing in file
                max_distance = float(values[2]) if max_distance < float(values[2]) else max_distance
                # if max_distance < float(values[2]):
                #     max_distance = float(values[2])

                # get maximum speed in the file
                max_speed = float(values[3]) if max_speed < float(values[3]) else max_speed
                # if max_speed < float(values[3]):
                #     max_speed = float(values[3])

    return [road_segments, max_distance, max_speed]

# Creating a city map of cityA->cityB in Road-Segments.txt in the dictionary as cityA->cityB and cityB->cityA
def city_entry_map(road_segments, cityA, cityB, road_length, speed, highway):
    road_mapping = road_segments.get(cityA)

    if road_mapping == None:
        road_segments[cityA] = [(cityB, road_length, speed, highway)]
    else:
        road_mapping.append((cityB, road_length, speed, highway))
        # road_segments[cityA] = road_mapping
     # return road_segments


# Please don't modify anything below this line
#
if __name__ == "__main__":

    print("Hello World")

    if len(sys.argv) != 4:
        raise (Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise (Exception("Error: invalid cost function"))

    print("before result")
    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])

