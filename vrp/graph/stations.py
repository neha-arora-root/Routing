import vrp.map_utils.polyline as poly


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
    def get_stations_data_file(self, filename, num_stations, depot=None):
        f = open(filename, 'r')
        data = f.readlines()
        f.close()

        if depot is None:
            depot = "0,50.7170968,4.268208"

        g = open(filename.strip('.txt') + "_stations.txt", 'w')
        g.write(str(num_stations) + "\n")
        g.write(depot + "\n")
        idx = 1
        for i in range(10, 10 + num_stations):
            curr_line = data[i]
            curr_line_values = curr_line.split(" ")
            geo_coordinates = curr_line_values[1] + ',' + curr_line_values[2]
            g.write(str(idx) + ',' + geo_coordinates + '\n')
            idx += 1
        g.close()

    ###################################################################################################################
    # Find the paths between a point and depot and store in a file in the form of encoded polylines and geo-points
    # Input: set of points, depot (lat, lng)
    # Output: File of above mentioned format
    ###################################################################################################################
    @classmethod
    def write_paths_file(self, stations_filename):
        f = open(stations_filename, 'r')
        data = f.readlines()
        f.close()

        g = open(stations_filename.strip('stations.txt') + "paths.txt", 'w')
        total_stations = int(data[0])
        g.write(str(total_stations) + '\n')
        g.write(data[1])
        depot_id, depot_lat, depot_lng = data[1].split(",")
        depot = (depot_lat, depot_lng)
        for i in range(2, total_stations + 2):
            node, curr_lat, curr_lng = data[i].split(",")
            curr_node = (curr_lat, curr_lng)
            all_paths = poly.get_paths_between_points(curr_node, depot)
            g.write("Node:" + str(node) + '\n')

            paths, polylines = all_paths["paths"], all_paths["polylines"]

            if len(paths) == 0:
                print("Empty response for source: " + str(curr_node) + "and destination: " + str(depot))
                continue
            g.write("Polylines:" + str(len(polylines)) + "\n")
            for j in range(len(polylines)):
                g.write(polylines[j] + '\n')
                g.write(str(paths[j]) + '\n')
        g.close()

    def write_polylines_from_path(self, source_file, dest_file):
        f = open(source_file, 'r')
        data = f.readlines()
        f.close()

        g = open(dest_file, 'w')
        total_stations = int(data[0])
        # depot = data[1]
        node = 1
        line_idx = 2
        while node <= total_stations:
            line_idx += 1
            num_paths = int(data[line_idx].split(":")[1])
            line_idx += 1
            for j in range(num_paths):
                g.write(data[line_idx])
                line_idx += 2
            node += 1
        g.close()

    def write_geopoints_from_path(self, source_file, dest_file):
        f = open(source_file, 'r')
        data = f.readlines()
        f.close()

        g = open(dest_file, 'w')
        total_stations = int(data[0])
        # depot = data[1]
        node = 1
        line_idx = 3
        while node <= total_stations:
            num_paths = int(data[line_idx].split(":")[1])
            line_idx += 2
            for j in range(num_paths):
                g.write(data[line_idx])
                line_idx += 2
            node += 1
        g.close()

    ###################################################################################################################
    # Main method
    # Input: (i) filename that needs to be processed: Has 3 options - belgium_50.txt, belgium_100.txt, belgium_500.txt
    # (ii) num_stations: int that tells the total number of stations apart from depot
    # (iii) process: boolean, whether the file with the processed information should be written or not
    # Output: File of above mentioned format
    ###################################################################################################################
    def __init__(self, filename, num_stations, process=False):
        if process:
            stations_data_file = filename.strip('.txt') + '_stations.txt'
            self.get_stations_data_file(filename, num_stations)

        else:
            stations_data_file = filename
        print("File prepared: " + stations_data_file)


stations_50 = Stations('/Users/nehaarora/Documents/github/Routing/vrp/data/belgium_50.txt', 50, False)
# stations_50.write_paths_file('/Users/nehaarora/Documents/github/Routing/vrp/data/belgium_50_stations.txt')
# stations_50.write_polylines_from_path('/Users/nehaarora/Documents/github/Routing/vrp/data/belgium_50_paths.txt',
#                                       '/Users/nehaarora/Documents/github/Routing/vrp/data/belgium_50_polylines.txt')
stations_50.write_geopoints_from_path('/Users/nehaarora/Documents/github/Routing/vrp/data/belgium_50_paths.txt',
                                      '/Users/nehaarora/Documents/github/Routing/vrp/data/belgium_50_geopoints.txt')
