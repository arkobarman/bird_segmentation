import json
def json_loader(filename):
    # Read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def count_area(vertices):
    n = len(vertices)  # Number of vertices
    area = 0

    # Shoelace formula
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]  # Next vertex (wraps around to the first)
        area += x1 * y2 - y1 * x2
    return abs(area) / 2

if __name__=='__main__':
    json_loader("CoCoTest.json")
    count_area()