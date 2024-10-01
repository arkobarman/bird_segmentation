from main import *
import random
import matplotlib.pyplot as plt

def draw_histogram(pairs,  title="Relation between size and species", xlabel="Category_Id", ylabel="Bird size (pixel)"):
    # Create the histogram
    id, frequencies = zip(*pairs)
    plt.bar(id,frequencies, edgecolor='black')
    
    # Add titles and labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Show the plot
    plt.show()
def draw_histogram_with_text(pairs,name_map,  title="Relation between size and species", xlabel="Category_Id", ylabel="Bird size (pixel)"):
    # Create the histogram
    id, frequencies = list(pairs.keys()),list(pairs.values())
    print(id)
    plt.bar(id,frequencies, edgecolor='black')
    for id_number,average in pairs.items():
        plt.text(id_number-0.5, int(average)+20, str(round(average,2)), fontsize=8, color='red')
       # plt.text(id_number-0.5, int(average)-20, str(name_map[id_number]), fontsize=8, color='black')  
    # Add titles and labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # Show the plot
    plt.show()
if __name__=='__main__':
    graph_data=[]
    data=json_loader("CoCoTest.json")
 #   for i in data["annotations"]:
       # graph_data.append(i['category_id'],count_area(i["segmentation"][0]))
 #       graph_data.append((random.randint(1,20),count_area(i["segmentation"][0])))
    averge_pair=[]
    for i in data["annotations"]:
        id=int(random.randint(0,20))
        averge_pair.append([id,count_area(i["segmentation"][0])])
        graph_data.append([id,count_area(i["segmentation"][0])])
    average_map=count_average(averge_pair)
    draw_histogram(graph_data)
    draw_histogram_with_text(average_map)