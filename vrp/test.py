file = open('/Users/nehaarora/Documents/github/Routing/vrp/data/belgium_50_neighbors_polylines.txt', "r")

data = file.readlines()
print("[")
for line in data:
    print('"' + line.strip("\n") + '",')
print("]")


#     for char in curr_line:
#         if char in " []()":
#             curr_line.replace(char, '')
#     all_points = curr_line.split(",")
#     print(all_points[0:10])
#     pairs = "["
#     for i in range(0, 2, 2):
#         px = all_points[i].strip("[").strip("(").strip(")").strip("]")
#         if px[0] == " ":
#             px = px[1:]
#         if px[0] == "(":
#             px = px[1:]
#         py = all_points[i + 1].strip("[").strip("(").strip(")").strip("]")
#         pairs = pairs + "{lat:" + str(px) + ",lng:" + str(py) + "},"
#     px = all_points[i]
#     py = all_points[i + 1]
#     pairs = pairs + "{lat:" + str(px) + ",lng:" + str(py) + "}],"
#     print(pairs)
# print("]")

