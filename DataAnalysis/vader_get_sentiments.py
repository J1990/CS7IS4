from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from os import listdir
from os.path import isfile, join

mypath = "releases2"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

print(onlyfiles)

for file in onlyfiles:

    path = "releases2/" + file
    with open(path, encoding="utf8") as f:
        data = json.load(f)
    
    analyzer = SentimentIntensityAnalyzer()
    
    for i in range(len(data)):
        sentence = data[i]['content']
        vs = analyzer.polarity_scores(sentence)
        to_append = {"intent":vs}
        data[i].update(to_append)
    print(data)
    
    new_path = "releases3_with_sentiment/" + file
    print(new_path)
    with open(new_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)