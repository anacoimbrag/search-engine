import json

from elasticsearch import Elasticsearch

articles = ["a", "the", "an"]
pronouns = ["i", "you", "we", "it", "they", "he", "she", "my", "mine", "their", "theirs", "his",
            "her", "that", "this", "us", "me", "him"]
connectives = ["in", "s", "d", "t", "by", "of", "out", "and", "or", "to", "as", "for", "on", "as", "so",
               "also", "though", "but", "not", "may", "who"]
verbs = ["is", "are", "been", "have", "do", "does"]
accents = [".", "-","_", "\\", "~", "/" ]
es = Elasticsearch(['http://localhost:9200'])


def delete_index():
    es.indices.delete(index="foo")


def create_index():
    es.indices.create(index="foo")


def setup_index():
    es.indices.close(index="foo")
    es.indices.put_settings(body={
        "settings": {
            "index.codec": "best_compression",
            "index": {
                "analysis": {
                    "filter": {
                        "synonyms_filter": {
                            "type": "synonym",
                            "synonyms_path": "synonyms.txt"
                        }
                    },
                    "analyzer": {
                        "analyzer_keyword": {
                            "type": "whitespace",
                            "tokenizer": ["keyword", "whitespace"],
                            "filter": [
                                "lowercase",
                                "synonyms_filter"
                            ],
                            "stop_words": articles + connectives + verbs + pronouns
                        }
                    }
                }
            }
        },
        "mappings": {
            "t": {
                "properties": {
                    "title": {
                        "similarity": "BM25",
                        "analyzer": "analyzer_keyword",
                        "type": "string"
                    },
                    "h1": {
                        "similarity": "BM25",
                        "analyzer": "analyzer_keyword",
                        "type": "string"
                    },
                    "h2": {
                        "similarity": "BM25",
                        "analyzer": "analyzer_keyword",
                        "type": "string"
                    },
                    "h3": {
                        "similarity": "BM25",
                        "analyzer": "analyzer_keyword",
                        "type": "string"
                    },
                    "content": {
                        "similarity": "BM25",
                        "analyzer": "analyzer_keyword",
                        "type": "string"
                    }
                }
            }
        }
    }, index="foo")
    es.indices.open(index="foo")


def index(doc):
    json_doc = json.dumps(doc.__dict__)
    f = open("parser.json", "a")
    print(doc.id)
    f.write(json_doc + "\n")
    f.close()


def search(query):
    res = es.search(q=query, filter_path=['hits.hits._id'])
    print(res)
