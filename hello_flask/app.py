from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import textdistance
import re
from collections import Counter

app = Flask(__name__)

words = []
file_path = r'C:\Users\Premier East Africa\Desktop\Capstone\text\sample2.txt'
with open(file_path, 'r' , encoding="utf8") as f:
    file_name_data = f.read()
    file_name_data=file_name_data.lower()
    words = re.findall(r'\w+',file_name_data)

# This is our vocabulary
V = set(words)
#print("Top ten words in the text are:", words[0:10])
#print("Total Unique words are: ", len(V))

word_freq = {}  
word_freq = Counter(words)
print(word_freq.most_common()[0:10])

probs = {}     
Total = sum(word_freq.values())    
for k in word_freq.keys():
    probs[k] = word_freq[k]/Total

# Define a function to correct each word in a sentence
def my_autocorrect3(sentence):
    # Convert the sentence to lowercase and extract all the words
    words = re.findall(r'\w+', sentence.lower())
    corrected_words = []
    for word in words:
        if word in V:
            # The word is already in our vocabulary
            corrected_words.append(word)
        else:
            # Calculate the similarity between the word and all the words in the vocabulary
            sim = [1 - (textdistance.Jaccard(qval=2).distance(v, word)) for v in word_freq.keys()]
            # Create a dataframe with the word probabilities and similarities
            df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
            df = df.rename(columns={'index':'Word', 0:'Prob'})
            df['Similarity'] = sim
            # Sort the dataframe by similarity and probability
            df = df.sort_values(['Similarity', 'Prob'], ascending=False)
            # Add the corrected word to the list of corrected words
            corrected_words.append(df.iloc[0, 0])
    # Return the top 3 corrected words for the sentence
    return " ".join(corrected_words[:3])

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/correct', methods=['POST'])
# def correct():
#     input_text = request.form['input_text']
#     corrected_text = my_autocorrect3(input_text)
#     return jsonify({'corrected_text': corrected_text})

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user_text = request.form.get("msg")
        bot_text = my_autocorrect3(user_text)
        return bot_text

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
