import pickle
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for
from flask import jsonify

app = Flask(__name__)
with open('ml_models/vectorizer-ngram_1_2.pickle', 'rb') as vec_file:
    vectorizer = pickle.load(vec_file)

with open('ml_models/kmeans-pp-model.pickle', 'rb') as kmeans_file:
    model = pickle.load(kmeans_file)


@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/')
def index():
    return render_template('classifier/index.html')

@app.route('/predict', methods=['POST'])
def predict():
    tweet_text = request.form['tweet']
    tweet_text = [tweet_text]
    processed_tweet = vectorizer.transform(tweet_text)

    prediction = model.predict(processed_tweet)
    return render_template('classifier/index.html', prediction_result=prediction)

if __name__ == '__main__':
    app.run()
