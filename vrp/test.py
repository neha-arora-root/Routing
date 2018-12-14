file = open("/Users/nehaarora/Desktop/RL/Routing/vrp/data/belgium_50_stations.txt", "r")

data = file.readlines()

print ("[")
for i in range(1, len(data)):
    line = data[i]
    values = line.split(",")
    print("["+values[1]+","+values[2]+"],")
print("]")