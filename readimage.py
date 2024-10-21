from main import json_loader
from crop import *
import numpy as np
class bird_annotion():
    def __init__(self,annotation):
        self.id=annotation['id']
        self.image_id=annotation['image_id']
        self.segmentation=annotation['segmentation'][0]
        self.bbox=annotation['bbox']
        self.aiclass=annotation['aiclass']
        self.area_size=self.count_area(self.segmentation)
    def count_area(self,vertices):
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
class species():
    def __init__(self,aiclass):
        self.aiclass=aiclass
        self.bird_list=[]
        self.bird_area_list=[]
        self.bird_sum=0
    def add(self,bird):
        if bird.aiclass==self.aiclass:
            self.bird_list.append(bird)
            self.bird_sum+=1
            self.bird_area_list.append(bird.area_size)
    def count_average(self):
        self.bird_size_mean=np.mean(self.bird_area_list)
    def count_outliers_iqr(self,output=1):
        q1 = np.percentile(self.bird_area_list, 25)
        q3 = np.percentile(self.bird_area_list, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        self.outlier_indices = [i for i, x in enumerate(self.bird_area_list) if x < lower_bound or x > upper_bound]#return index list of ourliers
        if output:
            self.outliers=[self.bird_list[i] for i in self.outlier_indices]
        #   return  self.outliers
    def make_non_outliers(self):
        outlier_set = set(self.outlier_indices)
        self.non_outliers = [self.bird_list[i] for i in range(len(self.bird_list)) if i not in outlier_set]

def get_class(annotation_data,attribute):
    index=0
    species_map={}
    for data in annotation_data:
        if data[attribute] not in species_map:
            species_map[data[attribute]]=index
            #species_map[index]=data[attribute]#bidirection map
            index+=1
    return species_map,index
# species_map,species_len= get_class(data_annotations,'aiclass')
# print(species_map)
def restore_image_stuct(image_info):
    image_map={}
    for image in image_info:
        image_map[image['id']]=image
    return image_map
if __name__=='__main__':
    saiclass_map={}
    bird_annotion_list=[]
    data=json_loader("DATASET/Train.json")
    data_annotations=data["annotations"]
    for annotaion in data_annotations:
        bird_annotion_list.append(bird_annotion(annotaion)) #transfer to bird_annoation class

    image_info=data['images']
    image_map=restore_image_stuct(image_info) #transfer structure to key of image_id
    species_map,species_len= get_class(data_annotations,'aiclass')
    species_list=[]
    for species_key in species_map.keys():
        species_list.append(species(species_key))

    for annotaions in bird_annotion_list:
        species_index=species_map[annotaions.aiclass]
        species_list[species_index].add(annotaions)
    
    for each_species in species_list:
        each_species.count_average()
        #print(each_species.bird_size_mean)
        if each_species.bird_sum>=50:
            print(each_species.aiclass)
            each_species.count_outliers_iqr(1)
            print(len(each_species.outliers))
            for birds in each_species.outliers:
                #print(birds.image_id)
                image_to_crop=image_map[birds.image_id]["file_name"]
                #crop_bird(image_to_crop,birds,each_species.bird_size_mean)
            each_species.make_non_outliers()
            for i in range(10):
                picked_normal=each_species.non_outliers[i].image_id
                image_to_crop=image_map[picked_normal]["file_name"]
                crop_bird(image_to_crop,each_species.non_outliers[i],each_species.bird_size_mean,'DATASET/normal/')


    
   
