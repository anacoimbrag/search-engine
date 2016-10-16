from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

queries_file = open("WT10g.queries")
f = open("results.search", "w")


def search(q):
    res = es.search(q=q)
    return res


for line in queries_file.readlines():
    query = line.strip().split("|")
    if len(query) > 1:
        docs = search(query[1])
        f = open("results.search", 'a')
        try:
            docs = docs["hits"]["hits"]
            rank = 1
            for doc in docs:
                doc_score = float(doc["_score"])
                query_words = query[1].strip().split(" ")
                for word in query_words:
                    if str(doc["_source"]["title"]).find(word) > 0:
                        doc_score = doc_score * 2
                    for h1 in doc["_source"]["h1"]:
                        if h1.find(word) > 0:
                            doc_score = doc_score * 1.5
                    for h2 in doc["_source"]["h2"]:
                        if h2.find(word) > 0:
                            doc_score = doc_score * 1.35
                    for h3 in doc["_source"]["h3"]:
                        if h3.find(word) > 0:
                            doc_score = doc_score * 1.2
                
                print(str(doc["_score"]) + "-" + str(doc_score))
                # f.write(query[0] + "\t" + "Q0" + "\t" + str(doc["_id"]).upper() + "\t" + str(rank) + "\t" +
                #     str(doc["_score"]) + "\t" + "srfiletop10" + '\n')
                f.write(query[0] + "\t" + "Q0" + "\t" + str(doc["_id"]).upper() + "\t" + str(rank) + "\t" +
                    str(doc_score) + "\t" + "srfiletop10" + "\n")
                rank += 1
        except KeyError:
                pass
