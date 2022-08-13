# moodbot

## How to run this chat system

First, create a virtual environment using `venv` or `conda`:

```python -m venv <environment name>```

Active the environment:

```<environment name>/bin/activate```

Install the necessary libraries:

```pip install -r requirements.txt```

Finally, chat with the bot:

```python app.py```

## Folder datas

train.txt; test.txt; val.txt | These are datasets for training the emotion classification model.

intents.json | This includes data for training the intent classification model and the response sentences to each intent.

emo_res.json | This includes the sentences respond to each of the 6 emotions. All the sentences are written after researching.

## Folder models

model.h5 | Emotion classification model.

model_chat.h5 | Intent classification model.

## Folder assets

tokenizer.pickle; label_encoder.pickle | Used to predict emotion of input texts.

tokenizer_chat.pickle; label_encoder_chat.pickle | Used to predict intent of input texts.

## Jupyter notebooks

emo_model.ipynb | This is used for training and testing the emotion classification model.

chat_model.ipynb | This is used for training and testing the intent classification model.

chatbot.ipynb | This includes functions used to build the chat application and testing samples of the functions.

## Python files

chatbot.py | This is same as chatbot.ipynb excludes testing samples of the functions.

app.py | This is the GUI to run the chat system.
