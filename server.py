import json
import re
from flask import Flask, Response, request, abort
from database import *

app = Flask(__name__)
wordCounter = {}

def add_one_word(word, old = None, new = None):
    return add(word, old ,new)
    #
    # if wordCounter.get(word):
    #     wordCounter[word] += 1
    #     if old != None:
    #         old +=1
    #
    # else:
    #     wordCounter[word] = 1
    #     if new != None:
    #         new +=1
    #
    # return old,new


@app.route('/sanity', methods=["GET"])
def sanity():
    print("Server up and running")
    return "Created"


@app.route('/words/<word>', methods=["GET"])
def check_word(word):
    for w in wordCounter:
        if w.get(word) == word:
            return json.dumps({"count": w.get(word)})


    return json.dumps({"Count": 0})


@app.route('/words', methods=["POST"])
def add_word():
    old = 0
    new = 0

    word_dict = request.get_json()
    word = None
    sentence = None
    if word_dict.get('word'):
        word = word_dict['word']

    if word_dict.get('sentence'):
        sentence = word_dict['sentence']


    if word:
        add_one_word(word)


    elif sentence:
        cleanString = re.sub('\W+', ' ', sentence)
        cleanString.lower()
        word_list = cleanString.split(" ")
        for w in word_list:
            old , new = add_one_word(w.lower(), old, new)

    return json.dumps({"old words": old, "new words": new })

@app.route('/total', methods=["GET"])
def sum_word():

    return json.dumps({"total count":sum(wordCounter.values())})



@app.route('/popular', methods=["GET"])
def get_most_popular():
    if bool(wordCounter) == False:
        abort(404)
    maximum_word = max(wordCounter, key=wordCounter.get)

    return json.dumps({maximum_word: wordCounter[maximum_word]})

@app.route('/ranking', methods=["GET"])
def get_top_five():

    top_vals = dict(sorted(wordCounter.items(), key=lambda item: item[1], reverse=True))
    if len(top_vals) < 5:
        abort(404)

    first5pairs = {k: top_vals[k] for k in list(top_vals)[:5]}

    return json.dumps({"rank": first5pairs})

@app.route('/delete/<word>', methods=["DELETE"])
def delete_word(word):
    temp = None
    if wordCounter.get(word) !=None:
        temp = wordCounter[word]
        del wordCounter[word]
        return json.dumps({"deleted": word})

    else:
        abort(404)


@app.route('/update/<neword>', methods=["PUT"])
def update_word(neword):
    wordCounter[neword] = wordCounter.pop(neword)



if __name__ == '__main__':
    app.run(port=4000)
