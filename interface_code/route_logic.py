# This code is part of the route logic for finding routes between two stations.
# It implements a breadth-first search (BFS) algorithm to find the optimal route between two train stations.

import pandas as pd
from collections import defaultdict, deque

# Load data
train_schedule = pd.read_csv('cleaned_dataset/cleaned_train_schedule.csv')
train_info = pd.read_csv('cleaned_dataset/cleaned_train_info.csv')

# Preprocess
train_schedule['Train_No'] = train_schedule['Train_No'].astype(str)
train_info['Train_No'] = train_info['Train_No'].astype(str)

# Build station-to-train and train-to-station maps
station_to_trains = defaultdict(set)
train_to_stations = defaultdict(list)

for _, row in train_schedule.iterrows():
    station = row['Station_Code']
    train_no = row['Train_No']
    station_to_trains[station].add(train_no)
    train_to_stations[train_no].append(station)

# Reverse lookup: Train number to name
train_no_to_name = dict(zip(train_info['Train_No'], train_info['Train_Name']))


def find_optimal_route(source, destination):
    source = source.upper()
    destination = destination.upper()

    if source == destination:
        return {
            "min_trains": 0,
            "route": []
        }

    visited_trains = set()
    visited_stations = set()
    queue = deque()

    # Initialize queue with all trains from source
    for train_no in station_to_trains.get(source, []):
        path = [(train_no, source)]
        queue.append((train_no, source, path, 1))

    while queue:
        train_no, current_station, path, train_changes = queue.popleft()

        if current_station == destination:
            # Process the path to extract meaningful train legs
            route_legs = []
            prev_train, start_station = path[0]
            for i in range(1, len(path)):
                curr_train, curr_station = path[i]
                if curr_train != prev_train:
                    # Train changed — end previous leg
                    route_legs.append({
                        "Train_No": prev_train,
                        "From": start_station,
                        "To": path[i - 1][1]
                    })
                    # Start new leg
                    prev_train = curr_train
                    start_station = curr_station
            # Append final leg
            route_legs.append({
                "Train_No": prev_train,
                "From": start_station,
                "To": destination
            })

            return {
                "min_trains": train_changes,
                "route": route_legs
            }

        visited_trains.add(train_no)
        visited_stations.add(current_station)

        stations_in_train = train_to_stations.get(train_no, [])
        try:
            idx = stations_in_train.index(current_station)
            next_stations = stations_in_train[idx + 1:]
        except ValueError:
            next_stations = []

        for next_station in next_stations:
            if next_station not in visited_stations:
                queue.appendleft((train_no, next_station, path + [(train_no, next_station)], train_changes))
                visited_stations.add(next_station)

        # Consider changing trains at current station
        for next_train in station_to_trains.get(current_station, []):
            if next_train not in visited_trains:
                queue.append((next_train, current_station, path + [(next_train, current_station)], train_changes + 1))
                visited_trains.add(next_train)

    return None  # No path found
