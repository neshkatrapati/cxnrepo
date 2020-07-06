import os
from time import time
import pickle

class Indexer:
    def __init__(self, source_file):
        self.source_file = source_file
        self.source_file_handle = self.check_exists()
        self.index = []
        self.index_file_name = f"{self.source_file}.index"
        self.check_index_exists()
        
    def check_exists(self):
        if os.path.exists(self.source_file):
            return open(self.source_file, errors='ignore')
        return Exception(f"File Not Found, Cannot Index :  {self.source_file}")
    
    def check_index_exists(self):
        #print(self.index_file_name,os.path.exists(self.index_file_name))
        if os.path.exists(self.index_file_name):
            print("Index file found.")
            self.index = pickle.load(open(self.index_file_name,'rb'))
        else:
            print("Index file not found, creating now....")
            s = time()
            self.create_index()
            e = time()
            print(f"{e-s} Seconds")
            #return open(self.index_file_name)
    
    
    def __getitem__(self, i):
        prev = 0 if i == 0 else self.index[i-1]
        self.source_file_handle.seek(prev)
        return self.source_file_handle.read(self.index[i] - prev)
    
    def create_index(self):
        
        byte_number = 0 
        self.index.append([0])
        while True:
            byte = self.source_file_handle.read(1)
            if not byte:
#                 self.index[-1] = byte_number
                 if self.index[-2] > self.index[-1]:
                     del self.index[-1]
                 break
            byte_number += 1
            if byte == '\n':
                self.index[-1] = byte_number
                self.index.append(0)
                
        with open(self.index_file_name, 'wb') as ind:
            pickle.dump(self.index, ind)