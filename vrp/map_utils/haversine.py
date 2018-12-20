import math


def get_haversine_distance(point1, point2, R=6371):
    lat1, lng1 = point1
    lat2, lng2 = point2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)

    delta_lambda = math.radians(lng2 - lng1)
    delta_phi = math.radians(lat2 - lat1)
    a = (math.sin(delta_phi / 2.0)) ** 2 + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0)) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c  # (where R is the radius of the Earth in km)
    return d
