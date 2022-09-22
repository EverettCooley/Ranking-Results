import csv
import math
import sys
class TF_IDF(object):
    def __init__(self, dataFile):
        with open(dataFile, "r") as f:
            reader=csv.reader(f)
            self.ROWS = list(reader)[1:]
        self.MAX_DOC_ID = len(self.ROWS)-1
        self.N_OF_DOCS = self.MAX_DOC_ID+1
        self.INVERTED_INDEX = self.create_inverted_index()


    # creates the inverted index from dataFile
    # returned as a dictionary
    def create_inverted_index(self):
        inverted_index = {}
        for row in self.ROWS:
            words = list(filter(None, row[1].split(" ")))
            for word in words:
                if word in inverted_index:
                    inverted_index[word].add(row[0])
                else:
                    inverted_index[word] = set(row[0])
        return inverted_index
                

    # given a query and k (as an int)
    # returns a list of the top k relevant documents
    def tf_idf(self, Q, k):
        if k>self.N_OF_DOCS:
            print("Try a k less than the number of documents")
            sys.exit(1)
            
        relevances = []
        for i in range(self.N_OF_DOCS):
            rel = [i, self.relevance(i, Q)]
            relevances.append(rel)

        relevances.sort(key=lambda x:x[1])
        result = []
        for i in range(len(relevances)-1, len(relevances)-k-1, -1):
            if relevances[i][1] == 0.0:
                break
            result.append((str(relevances[i][0]), relevances[i][1]))
        return result

    
    # given a docID and query
    # returns the relevance of a doc with a given query
    def relevance(self, d, Q):
        split_Q = list(filter(None, Q.split(" ")))
        sum = 0
        for term in split_Q:
            tf_value = self.tf(str(d), term)
            nt = len(self.INVERTED_INDEX[term])
            sum += tf_value/nt
        return sum

    # given a docID and term
    # returns the tf score of the term in docID
    def tf(self, d, t):
        split_word_list = list(filter(None, self.ROWS[int(d)][1].split(" ")))
        ndt = split_word_list.count(t)
        nd = len(split_word_list)
        return math.log(1+(ndt/nd))


def main():
    t = TF_IDF("wine.csv")
    print(t.tf_idf("tremendous tremendous watson", 5))


if __name__ == "__main__":
    main()
