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


polyline = "}wjiGtdpcNrAlBJZ"
polyline2 = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
geo_points_list = decode_polyline(polyline)
print_geo_points_list(geo_points_list)
print("\n")
test_decode_polyline([polyline, polyline2], [[[43.64175, -79.38651], [43.64133, -79.38706], [43.64127, -79.3872]],
                                             [[38.5, -120.2], [40.7, -120.95], [43.252, -126.453]]])
