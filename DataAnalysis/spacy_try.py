import spacy 
import json
from os import listdir
from os.path import isfile, join
  
# Load English tokenizer, tagger,  
# parser, NER and word vectors 
nlp = spacy.load("en_core_web_sm")

mypath = "releases2"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

print(onlyfiles)

for file in onlyfiles:

    path = "releases2/" + file
    with open(path, encoding="utf8") as f:
        data = json.load(f)
    
    for i in range(len(data)):
        sentence = data[i]['content']
        doc = nlp(sentence) 
  
        # Token and Tag 
        for token in doc: 
          print(token, token.pos_) 
          
        # You want list of Verb tokens 
        print("Verbs:", [token.text for token in doc if token.pos_ == "VERB"]) 