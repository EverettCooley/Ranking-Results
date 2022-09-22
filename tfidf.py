import csv
import math
import sys
class TF_IDF(object):
    def __init__(self, dataFile):

        self.file  = dataFile
        self.f = open(self.file, "r")
        self.reader=csv.reader(self.f)
        self.rows = list(self.reader)
        self.maxDocID = len(self.rows)-2

        self.inverted_index = {}
        with open(self.file, "r") as f:
            reader=csv.reader(f)
            next(reader) # might break if csv is empty
            for row in reader:
                sr = row[1].split(" ")
                words = list(filter(None, sr)) # handle this better maybe drop last if its none
                for word in words:
                    if word in self.inverted_index:
                        self.inverted_index[word].add(row[0])
                    else:
                        self.inverted_index[word] = set(row[0])

    def __del__(self):
        self.f.close()
                
    # example query = ‘hello world’, then the query would have two terms, ‘hello’ and ‘world’`
    # return top k results in decending order
    def tf_idf(self, Q, k):
        relevances = []
        r = self.maxDocID+1
        for i in range(r):
            if i >self.maxDocID:
                break

            rel = [i, self.relevance(i, Q)]
            relevances.append(rel)
        relevances.sort(key=lambda x:x[1])
        for i in range(len(relevances)-1, len(relevances)-k-1, -1):
            if relevances[i][1] == 0.0:
                break
            print(relevances[i])


            
    # d = document id as string ! NEEDS TO BE STRING
    # example query = ‘hello world’, then the query would have two terms, ‘hello’ and ‘world’
    def relevance(self, d, Q):
        sum = 0
        split_Q = Q.split(" ")
        split_Q = list(filter(None, split_Q))
        for word in split_Q:
            tf_value = self.tf(d, word)
            nt = len(self.inverted_index[word])
            sum += tf_value/nt
        return sum


    # d = document id as string ! NEEDS TO BE STRING
    # t = one term
    def tf(self, d, t):
        if (d < 0) or (d >self.maxDocID):
            print(f"d was '{d}' and is out of bounds")
            sys.exit(1)

        split_word_list = self.rows[d+1][1].split(" ")
        split_word_list = list(filter(None, split_word_list))

        ndt = 0
        for word in split_word_list:
            if word == t:
                ndt += 1

        nd = len(split_word_list)
        return math.log(1+(ndt/nd))


    def get_row(self, d):
            rows = list(self.reader)
            return rows[d+1]

if __name__ == "__main__":
    t = TF_IDF("wine.csv")
    t.tf_idf("tremendous tremendous watson", 5)
    # print(t.relevance(73, "tremendous"))
    # print(t.tf(0, "wine"))
    # t.get_row(2)
            
