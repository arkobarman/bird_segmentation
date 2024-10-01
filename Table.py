from tabulate import tabulate
def draw_table(name_map,input_data,head):
    data=[]
    for key,value in input_data.items():
        data.append([name_map[key],value])
    print(tabulate(data, headers=head, tablefmt="grid"))
def draw_table_hori(name_map,input_data):
    head=[]
    data=[]
    
    for key,value in name_map.items():
        head.append(value)
        data.append(input_data[key])
    print(head)
    print(len(data))
    print(tabulate([head,data] ,tablefmt="grid"))
#if __name__=='__main__':
    