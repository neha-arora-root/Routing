import json


class Stations:

    @staticmethod
    def get_geo_coordinates_tuple(string_geo_coordinates):
        geo_x, geo_y = string_geo_coordinates.split(',').strip()
        geo_tuple = (float(geo_x), float(geo_y))
        return geo_tuple

    #############################################################
    # Converting raw data file to the following format:
    # total stations
    # each station as tuple containing (id, lat, lng)
    #############################################################
    @classmethod
    def get_stations_data_file(self, filename, num_stations):
        f = open(filename, 'r')
        data = f.readlines()
        f.close()

        g = open(filename.strip('.txt') + "_stations.txt", 'w')
        g.write(str(num_stations) + "\n")
        idx = 1
        for i in range(10, 10 + num_stations):
            curr_line = data[i]
            curr_line_values = curr_line.split(" ")
            geo_coordinates = curr_line_values[1] + ',' + curr_line_values[2]
            g.write(str(idx) + ',' + geo_coordinates + '\n')
            idx += 1
        g.close()

    def __init__(self, filename, num_stations, process=False):
        if process:
            stations_data_file = filename.strip('.txt') + '_stations.txt'
            self.get_stations_data_file(filename, num_stations)

        else:
            stations_data_file = filename

        f = open(stations_data_file, 'r')
        data = f.readlines()

        self.nV = int(data[0])
        self.nE = int(data[1])
        self.depot = self.get_geo_coordinates_tuple(data[2])
        self.V = list()
        for i in range(self.nV):
            self.V.append(self.get_geo_coordinates_tuple(data[2 + i]))


stations_50 = Stations('/Users/nehaarora/Desktop/RL/VRP/data/belgium_50.txt', 50, False)