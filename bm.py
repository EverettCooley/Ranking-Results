import csv
import math

class BM_25(object):
    def __init__(self, dataFile):
        self.K1 = 1.2
        self.B = 0.75
        self.K2 = 500
        with open(dataFile, "r") as f:
            reader=csv.reader(f)
            self.ROWS = list(reader)[1:]
        self.MAX_DOC_ID = len(self.ROWS)-1
        self.N_OF_DOCS = self.MAX_DOC_ID+1
        self.AVERAGE_DOC_LENGTH = self.average_length_of_rows()
        self.INVERTED_INDEX = self.create_inverted_index()

    
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


    def length_of_row(self, docID):
        row = self.ROWS[docID][1].split(" ")
        row = list(filter(None, row))
        return len(row)


    def average_length_of_rows(self):
        sum = 0
        for i in range(self.N_OF_DOCS):
            sum += self.length_of_row(i)
            # print("sum", sum)
            # print(i)
        return sum/self.N_OF_DOCS


    def bm25(self, query, k):
        query_list = list(filter(None, query.split(" ")))
        relevances = []

        for i in range(self.N_OF_DOCS):
            relevances.append([i, self.bm25_single_doc(query_list, i)])

        relevances.sort(key=lambda x:x[1])
        result = []
        for i in range(len(relevances)-1, len(relevances)-k-1, -1):
            if relevances[i][1] == 0.0:
                break
            result.append((relevances[i][0], relevances[i][1]))
        return result


    def bm25_single_doc(self, query_list, docID):
        sum = 0
        for term in query_list:
            print("term: ",term)
            inverted_doc = self.inverted_doc_freq(term)
            term_f = self.term_freq(docID, term)
            qtf =  self.query_term_frequency(query_list, term)
            sum += inverted_doc * term_f * qtf
            print("sum",sum)
            print()
        return sum


    def inverted_doc_freq(self, t):
        n = self.N_OF_DOCS
        if t in self.INVERTED_INDEX:
            df_t = len(self.INVERTED_INDEX[t])
        else:
            df_t=0
        print("n = ", n)
        print("df_t = ", df_t)
        return math.log(n-df_t+.5) - math.log(df_t+.5)
    

    def query_term_frequency(self, query_list, t):
        count = query_list.count(t)
        print("qf_t = ", count)
        return (((self.K2+1)*count)/(self.K2+count))


    def term_freq(self, docID, t):
        row = list(filter(None, self.ROWS[docID][1].split(" ")))
        count = row.count(t)
        print("f_t = ",count)
        print("average_doc_length = ",self.AVERAGE_DOC_LENGTH)
        print("len_of_doc = ", len(row))
        top = (self.K1 + 1)*count
        bot_inside = (1-self.B)+(self.B*(len(row)/self.AVERAGE_DOC_LENGTH))
        bot = (self.K1*bot_inside)+count
        return top / bot


if __name__ == "__main__":
    bm = BM_25("wine.csv")
    # print(bm.INVERTED_INDEX)
    # print(bm.AVERAGE_DOC_LENGTH)
    # print(bm.MAX_DOC_ID)
    # print(bm.N_OF_DOCS)
    # print(bm.ROWS)
    # print(bm.bm25("tremendous tremendous watson", 5))
    print(bm.bm25_single_doc(["tremendous", "tremendous", "watson"], 71))
    # print(bm.average_length_of_rows())
    # print(bm.inverted_doc_freq("there"))


    # print(bm.query_term_frequency("tremendous tremendous watson", "tremendous"))
    # print(bm.term_freq(2, "watson"))

# Use k1 = 1.2,
# k2 = 500, and b = 0.75
# 
