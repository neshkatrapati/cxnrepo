from indexer import Indexer
import os
import random


class Dataset:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.index_file = Indexer(self.dataset_path)
        self.rows = list(range(len(self.index_file.index)))
        
    
    def __getitem__(self, i):
        return self.index_file[self.rows[i]]
    
    
    def shuffle(self):
        random.shuffle(self.rows)
        
    
    def partition(self, percentages, shuffle=False):
        if shuffle:
            self.shuffle()
        
        if sum(percentages) != 1.0:
            raise Exception("Percentages do not sum to 1.0")
            
        
        partitions = []
        index_len = len(self.index_file.index)
        current = 0
        pts = [current]
        for i, partition in enumerate(percentages):
            pt = Dataset(self.dataset_path)
            nxt = current + int((partition * index_len))
            if i == len(percentages) - 1:
                nxt = index_len 
            pt.rows =  self.rows[current:nxt]
            current = nxt 
            pts.append(nxt)
            partitions.append(pt)
        #print(pts)
        return tuple(partitions)
        
        