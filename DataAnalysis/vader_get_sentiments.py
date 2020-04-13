from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from os import listdir
from os.path import isfile, join
import plotly.graph_objects as go

mypath = "releases2"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

#print(onlyfiles)

positive_releases = 0

negative_releases = 0

for file in onlyfiles:

    path = "releases2/" + file
    with open(path, encoding="utf8") as f:
        data = json.load(f)
    
    analyzer = SentimentIntensityAnalyzer()
    
    for i in range(len(data)):
        sentence = data[i]['content']
        vs = analyzer.polarity_scores(sentence)
        pos = vs['pos']
        neg = vs['neg']
        if pos > neg:
            positive_releases += 1
        else:
            negative_releases += 1
        to_append = {"intent":vs}
        data[i].update(to_append)
    #print(data)
    
    new_path = "releases3_with_sentiment/" + file
    #print(new_path)
    with open(new_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        

press_releases = ['Positive', 'Negative']
fig = go.Figure([go.Bar(x = press_releases, y=[positive_releases, negative_releases], color='lifeExp')])
fig.write_html("file.html")
