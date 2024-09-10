import json
import random
from Draw import *
def json_loader(filename):
    # Read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def count_area(vertices):
    n = len(vertices)  # Number of vertices
    area = 0

    # Shoelace formula
    for i in range(0,n,2):
        x1, y1 = vertices[i],vertices[i+1]
        x2, y2 = vertices[(i + 2) % n],vertices[(i + 2) % n+1]  # Next vertex (wraps around to the first)
        area += x1 * y2 - y1 * x2
    return abs(area) / 2
def count_average(pair):
    total={}
    numbers={}
    output={}
    for ID_area_pair in pair:
        if ID_area_pair[0] in total:
            total[ID_area_pair[0]]+=ID_area_pair[1]
            numbers[ID_area_pair[0]]+=1
        else:
            numbers[ID_area_pair[0]]=1
            total[ID_area_pair[0]]=ID_area_pair[1]
        for key,value in total.items():
            output[key]=value/numbers[key]
    return output
if __name__=='__main__':
    data=json_loader("CoCoTest.json") #loadin data
    averge_pair=[]
    graph_data=[]
    for i in data["annotations"]:
        id=int(random.randint(0,20))
        averge_pair.append([id,count_area(i["segmentation"][0])])
        graph_data.append([id,count_area(i["segmentation"][0])])
        #print(i['category_id'],count_area(i["segmentation"][0]))
    average_map=count_average(averge_pair)
    for i,j in average_map.items():
        print(i,j)
    draw_histogram(graph_data)
    draw_histogram_with_text(average_map)