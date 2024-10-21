import json
import random
from Draw import *
from Table import *
def json_loader(filename):
    """
    Load json data from filename

    Args:
        filename (string): the file name that you want to input.

    Returns:
        data (dictionary): returns a json format dictionary.
    """
    # Read the JSON file
    with open(filename, 'r') as file:
        data = json.load(file)
    return data
def count_area(vertices):
    """
    Count the area of each segmentation.

    Args:
        vertices (list): a list with all pixel space.

    Returns:
        int: area size.
    """
    n = len(vertices)  # Number of vertices
    area = 0

    # Shoelace formula
    for i in range(0,n,2):
        x1, y1 = vertices[i],vertices[i+1]
        x2, y2 = vertices[(i + 2) % n],vertices[(i + 2) % n+1]  # Next vertex (wraps around to the first)
        area += x1 * y2 - y1 * x2
    return abs(area) / 2
def count_sepcies_num(count_id):
    """
    Count the area of each segmentation.

    Args:
        count_id (list[]): number of each species.

    Returns:
        output (map) : species number.
    """
    index=0
    count_id_map={}
    for i in count_id:
        if i!=0:
           # print(saiclass_map[index],i)
            count_id_map[index]=i
            index+=1
    return count_id_map
def count_average(pair):
    """
    Count the area of each segmentation.

    Args:
        pair (list[list[]]): pairs of [id,area size].

    Returns:
        output (map) : area size.
    """
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
    saiclass_map={}
    data=json_loader("DATASET/Train.json")
    data_annotations=data["annotations"]
    averge_pair=[]
    graph_data=[]
    species_number=0
    species_map={}
    count_id=[]
    for i in range(26):
        count_id.append(0)
        graph_data.append([])
    for i in data_annotations:
        #id=int(random.randint(0,20))
        if i['aiclass'] in species_map:
            id=species_map[i['aiclass']]
        else:
            species_map[i['aiclass']]=species_number
            saiclass_map[species_number]=i['aiclass']
            id=species_number
            species_number+=1    
        averge_pair.append([id,count_area(i["segmentation"][0])]) #count area size
        graph_data[id].append(count_area(i["segmentation"][0]))
        count_id[id]+=1
    average_map=count_average(averge_pair) #count average of all id 
    count_id_map=count_sepcies_num(count_id) #count each species number
    #print(count_id_map)
    count_id_map= dict(filter(lambda item: item[1] > 50, count_id_map.items())) #filter out the number >50
    highest_list = [item[0] for item in count_id_map.items() if item[1] > 50] #filter out the average data
    selected_values=[]
    selected_labels=[]
    for i in highest_list:
        for j in graph_data[i]:
            selected_labels.append(i)
            selected_values.append(j)
   #selected_values = [graph_data[i] for i in highest_list]
   # highest_graph_data=graph_data[highest_list]
   # print(average_map)
    #average_map= dict(filter(lambda item: item[0] in count_id_map.keys(), average_map.items()))
    #print(average_map)
    #draws table
    #draw_table( saiclass_map,count_id_map,['Speacies,number'])

    #draw_table_hori(saiclass_map,count_id_map)
    # draw_histogram(graph_data) # draw bar graph that same id stacks
    plot_box(selected_values,selected_labels)
    plot_box()
    #plot_violin(selected_values,selected_labels)
    #draw_histogram_with_text(average_map,saiclass_map, title="Average of each speacies") # draw gar graph with average area size
    #draw_histogram_with_text(count_id_map,saiclass_map, title="Each Species number", xlabel="Category_Id", ylabel="Bird number")
    #print(species_map)
    #draw_table( saiclass_map,count_id_map,['Speacies','id','number'])