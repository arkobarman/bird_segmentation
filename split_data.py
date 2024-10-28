from main import json_loader
import readimage
import json
import random
dataset_ratio=[.8,.1,.1]
def split( dataset_ratio,data_list):
    # Calculate the total size
    total_size = len(data_list)
    
    # Calculate sizes for train and validation splits
    train_size = int(dataset_ratio[0] * total_size)
    val_size = int(dataset_ratio[1] * total_size)
    
    # Create train, validation, and test splits
    train_data = data_list[:train_size]
    val_data = data_list[train_size:train_size + val_size]
    test_data = data_list[train_size + val_size:]  # Remaining items go to test
    
    # Ensure all data is accounted for
    assert len(train_data) + len(val_data) + len(test_data) == total_size, "Data split does not match total size."
    
    return train_data, val_data, test_data

def split_dataset(path):
    data=json_loader(path)
    data_annotations=data["annotations"]
    print("total annotations:",len(data_annotations))
    image_info=data['images'] 

    aiclass_map={}
    for annotation in data_annotations:
        if annotation['aiclass'] not in aiclass_map:
            aiclass_map[annotation['aiclass']]=[]
            aiclass_map[annotation['aiclass']].append(annotation)
        else:
            aiclass_map[annotation['aiclass']].append(annotation)
    bird_less=[]
    del_list=[]
    for key,value in aiclass_map.items():
        if len(value)<50:
            bird_less.extend(value)
            del_list.append(key)
    for key in del_list:
        del aiclass_map[key]
    for annotaion in bird_less:
        annotaion['aiclass']='LBird'
    aiclass_map['LBird']=bird_less
    
    for key,value in aiclass_map.items():
            print(key,len(value))
    #shuffle
    train_json={}
    val_json={}
    test_json={}
    train_json['annotations']=[]
    val_json['annotations']=[]
    test_json['annotations']=[]
    
    train_json['images']=image_info
    val_json['images']=image_info
    test_json['images']=image_info
    for key,value in aiclass_map.items():
        random.shuffle(value)
        train,val,test=split(dataset_ratio,value)
        train_json['annotations'].extend(train)
        val_json['annotations'].extend(val)
        test_json['annotations'].extend(test)
    
    with open('DATASET/Train_split.json', 'w') as f:
        json.dump(train_json, f)
    with open('DATASET/Val_split.json', 'w') as f:
        json.dump(val_json, f)
    with open('DATASET/Test_split.json', 'w') as f:
        json.dump(test_json, f)

    print("Data split into train, validation, and test sets successfully!")
def test_split(path):
    print("testing split at", path)
    data=json_loader(path)
    data_annotations=data["annotations"]
    print("total annotations:",len(data_annotations))
    aiclass_map={}
    for annotation in data_annotations:
        if annotation['aiclass'] not in aiclass_map:
            aiclass_map[annotation['aiclass']]=[]
            aiclass_map[annotation['aiclass']].append(annotation)
        else:
            aiclass_map[annotation['aiclass']].append(annotation)
    for key,value in aiclass_map.items():
        print(key,len(value))
if __name__=='__main__':
    split_dataset("DATASET/Train.json")
    test_split("DATASET/Train_split.json")
    test_split("DATASET/Test_split.json")
    test_split("DATASET/Val_split.json")
