import pickle

class Filehelper:
    def file_wr(data,filename):
        #filename = './id_list.txt'
        with open(filename,'wb') as file:
            pickle.dump(data,file)

    def file_get(filename):
        #filename = './id_list.txt'
        with open(filename,'rb') as file:
            data = pickle.load(file)
        return data