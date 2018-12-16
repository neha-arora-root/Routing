import requests
import json

with open('../config/map_config.json', 'r') as f:
    config = json.load(f)


########################################################################################################
# Get the paths between two points in terms of compressed polylines and all the geo points for each path
# Input: source and destination geopoints
# Output: dict of list of polylines and list of geopoints for each polylines
########################################################################################################


def get_paths_between_points(source, destination):
    list_of_polylines = get_polyline(source, destination)
    list_of_decoded_polylines = list()
    for polyline in list_of_polylines:
        list_of_decoded_polylines.append(decode_polyline(polyline))
    return {"polylines": list_of_polylines, "paths": list_of_decoded_polylines}


########################################################################################################
# Extract polylines for given source and destination in geo-points
# Input: tuples: source, destination
# Output: list of strings: a list of all polylines
########################################################################################################


def get_polyline(source, destination):
    source_lat, source_lng = source
    dest_lat, dest_lng = destination

    request_url = "https://" + config["google_maps_apis"]["directions_api_url"]
    request_params = {
        "origin": str(source_lat) + "," + str(source_lng),
        "destination": str(dest_lat) + "," + str(dest_lng),
        "alternatives": "true",
        "key": config["google_maps_apis"]["key"]
    }
    polylines = list()
    try:
        directions_api_response = requests.get(request_url, request_params)
        json_data = json.loads(directions_api_response.text)
        print("Server returned response for " + str(source) + " and destination " + str(destination))
        routes = json_data["routes"]

        if len(routes) > 0:
            for each_route in routes:
                curr_polyline = str(each_route["overview_polyline"]["points"])
                print(curr_polyline)
                polylines.append(curr_polyline)
    except:
        print("Request for (" + source + ") and destination (" + destination + ") unsuccessful!")
    return polylines


########################################################################################################
# Jeffrey Sambell's implementation for decoding a polyline that is output from Google's Directions API
# encoded_polyline: an ASCII string that contains the information of coordinates between source and
# destination
#
# Output: List of tuples of geo-coordinates that lie between source and destination
########################################################################################################


def decode_polyline(encoded_polyline):
    geo_points_list = list()
    index = 0
    encoded_len = len(encoded_polyline)
    lat = 0
    lng = 0

    while index < encoded_len:
        shift, result = 0, 0
        while True:

            b = ord(encoded_polyline[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5

            if b < 0x20:
                break

        if result & 1 != 0:
            dlat = ~(result >> 1)
        else:
            dlat = (result >> 1)
        lat += dlat

        shift, result = 0, 0
        while True:

            b = ord(encoded_polyline[index]) - 63
            index += 1
            result |= (b & 0x1f) << shift
            shift += 5

            if b < 0x20:
                break
        if result & 1 != 0:
            dlng = ~(result >> 1)
        else:
            dlng = (result >> 1)
        lng += dlng

        lat_geo = lat / 1e5
        lng_geo = lng / 1e5

        geo_points_list.append((lat_geo, lng_geo))

    return geo_points_list


def print_geo_points_list(geo_points):
    for i in range(len(geo_points)):
        print("[" + str(geo_points[i][0]) + "," + str(geo_points[i][1]) + "]")


########################################################################################################
# Test the method for decoding polylines: decode_polyline
# Inputs: Polyline, corresponding list of geo-coordinates
# Calls the method decode_polyline to compare the method's output with the expected output
########################################################################################################


def test_decode_polyline(polyline, list_geo_coordinates):
    total_test_cases = len(polyline)
    tests_covered = 0

    for i in range(total_test_cases):
        expected_list = list_geo_coordinates[i]
        output_list = decode_polyline(polyline[i])

        if len(expected_list) != len(output_list):
            print("Test " + str(i + 1) + ": Failed")
            continue
        for j in range(len(expected_list)):
            if expected_list[j][0] != output_list[j][0] or expected_list[j][1] != output_list[j][1]:
                print("Test " + str(i + 1) + ": Failed")
                continue
        tests_covered += 1
        print("Test " + str(i + 1) + ": Passed")

    print("Coverage: " + str(tests_covered / total_test_cases * 100) + "%")
    return tests_covered / total_test_cases


# polyline = "}wjiGtdpcNrAlBJZ"
# polyline2 = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
# geo_points_list = decode_polyline(polyline)
# print_geo_points_list(geo_points_list)
# print("\n")
# test_decode_polyline([polyline, polyline2], [[[43.64175, -79.38651], [43.64133, -79.38706], [43.64127, -79.3872]],
#                                              [[38.5, -120.2], [40.7, -120.95], [43.252, -126.453]]])
#
# paths = get_paths_between_points((43.64175, -79.38651), (43.64127, -79.3872))
# print(paths)
paths = get_paths_between_points((50.7170968, 4.268208), (51.0678307, 3.7290914))
