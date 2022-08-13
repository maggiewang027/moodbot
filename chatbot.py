import numpy as np
import random
import pickle
import json
import requests
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re 
import nltk
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from nltk.stem import WordNetLemmatizer

import warnings
warnings.filterwarnings('ignore')


lb = pickle.load(open('assets/label_encoder.pickle', 'rb'))
tokenizer = pickle.load(open('assets/tokenizer.pickle', 'rb'))
model = load_model('models/model.h5')
emo_res = json.loads(open('data/emo_res.json').read())


lb_chat = pickle.load(open('assets/label_encoder_chat.pickle', 'rb'))
token_chat = pickle.load(open('assets/tokenizer_chat.pickle', 'rb'))
model_chat = load_model('models/model_chat.h5')
int_data = json.loads(open('data/intents.json').read())


def int_clean(sent):
    lemmatizer = WordNetLemmatizer()
    corpus = []
    text = re.sub('[^a-zA-Z]', ' ', sent)  # punctuation removal
    text = text.lower()  # convert to lowercase
    words = text.split()
    words = [lemmatizer.lemmatize(w) for w in words] # lemmatizing
    text = " ".join(words)
    corpus.append(text)
    seq = token_chat.texts_to_sequences(corpus)
    seq_pad = pad_sequences(seq,maxlen=8)
    return seq_pad


def clean(sent):
    lemmatizer = WordNetLemmatizer()
    corpus = []
    text = re.sub('[^a-zA-Z]', ' ', sent) # punctuation removal
    text = text.lower() # convert to lowercase
    words = text.split()
    words = [w for w in words if not w in stop_words] # removing stopwords
    # lemmatizing
    words = [lemmatizer.lemmatize(w) for w in words]
    text = " ".join(words)
    corpus.append(text)
    seq = tokenizer.texts_to_sequences(corpus)
    seq_pad = pad_sequences(seq,maxlen=35)
    return seq_pad


def predict_int(sent):
    sent = int_clean(sent)
    result = lb_chat.inverse_transform(np.argmax(model_chat.predict(sent),axis=1))[0]
    prob =  np.max(model_chat.predict(sent))
    #print(f"{result}: {prob}\n\n")
    return result, prob


def predict(sent):
    sent = clean(sent)
    result = lb.inverse_transform(np.argmax(model.predict(sent),axis=1))[0]
    prob =  np.max(model.predict(sent))
    #print(f"{result}: {prob}\n\n")
    return result, prob


def response(sent):
    result,prob = predict_int(sent)
    result2,prob2 = predict(sent)
    list_of_ints = int_data['intents']
    if prob > 0.75:
        for i in list_of_ints:
            if i['tag'] == result:
                response_result = random.choice(i['responses'])
                return response_result
    if prob <= 0.75:
        if prob2 > 0.75:
            for i in emo_res:
                if i['emotion'] == result2:
                    response_result = random.choice(i['responses'])
                    return response_result
        else:
            response_result = "Sorry, I don't understand, please ask me something else. You can still choose to listen to these songs."
            return response_result


api_key = 'ba7998f08e0326c7b05b501610f442e1'
user = 'maggiewang027'
def lastfm_get(payload):
    # define headers and url from the api
    headers = {'user-agent': user}
    url = 'https://ws.audioscrobbler.com/2.0/'
    # add initial setup
    payload['api_key'] = api_key
    payload['format'] = 'json'
    payload['limit'] = 5
    # get the api request
    response = requests.get(url, headers=headers, params=payload)
    return response


sadness = ['sadness','depression','suffering','disappointment','shame','sympathy']
anger = ['anger','rage','disgust','envy','torment','frustration']
fear = ['fear','horror','fright','shock','panic','worry']
love = ['love','affection','liking','longing','compassion','passion']
surprise = ['surprise','amazement','astonishment']
joy = ['joy','thrill','contentment','optimism','pride','rapture']


def song_get(emo):
    # get the songs based on the emotion detected
    if emo == 'sadness':
        emotion = random.choice(sadness)
    if emo == 'anger':
        emotion = random.choice(anger)
    if emo == 'fear':
        emotion = random.choice(fear)
    if emo == 'love':
        emotion = random.choice(love)
    if emo == 'surprise':
        emotion = random.choice(surprise)
    if emo == 'joy':
        emotion = random.choice(joy)
    r = lastfm_get({'method': 'tag.getTopTracks','tag':emotion})
    payload = r.json()
    l=[]
    artist = payload['tracks']['track'][0]['artist']['name']
    for i in range(0,5):
        song = payload['tracks']['track'][i]['name']
        url = payload['tracks']['track'][i]['url']
        l.append([song,url])
    return l,artist


def similar_get(artist,song):
    r = lastfm_get({'method': 'track.getSimilar','artist':artist,'track':song})
    payload = r.json()
    l=[]
    for i in range(0,5):
        similar_song = payload['similartracks']['track'][i]['name']
        url = payload['similartracks']['track'][i]['url']
        l.append([similar_song,url])
    return l


def recommend(sent):
    result,prob = predict(sent)
    # get songs and url based on the emotion
    song,artist = song_get(result)
    # get similar songs and url based on the first song's name and artist
    songs = similar_get(artist,song[0])
    for i in songs:
        song.append(i)
    return song
