import requests
import json

f = open("WT10g.queries")
output = open("elasticsearch-2.3.4/config/synonyms.txt", 'a')

for line in f.readlines():
    words = line[line.find("|") + 1:].strip().split(" ")
    for word in words:
        response = requests \
            .get("http://thesaurus.altervista.org/thesaurus/v1?word=" + word +
                 "&key=EVRJ7KHMfj5zaCQmi4aN&language=en_US&output=json")
        parsed = json.loads(response.text)
        synonyms = []
        try:
            for resp in parsed["response"]:
                synonym = (resp["list"]["synonyms"])
                start = synonym.find('(')
                end = synonym.find(')')
                if start != -1 and end != -1:
                    synonym = synonym[:start - 1]

                synonyms = synonyms + (synonym.split("|"))
        except KeyError:
            pass

        if len(synonyms) > 0:
            output.write(word)
            for s in synonyms:
                output.write(", " + s)
            output.write("\n")


output.close()
f.close()
