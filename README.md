# moodbot

I tried to package the project, but the final packaged executable was not runnable and was particularly large (over 2GB). So, there is no executable program, meaning that the chatbot has to be run in the terminal.

## How to run this chat system

First, create a virtual environment using `venv` or `conda`:

```python -m venv <environment name>```

Active the environment:

```<environment name>/bin/activate```

Install the necessary libraries:

```pip install -r requirements.txt```

Finally, chat with the bot:

```python app.py```

## Folder data

train.txt; test.txt; val.txt | These are datasets for training the emotion classification model.

intents.json | This includes data for training the intention classification model and the response sentences to each intention.

emo_res.json | This includes the sentences that respond to each of the 6 emotions. All the sentences are written after researching.

## Folder models

model.h5 | Emotion classification model.

model_chat.h5 | Intention classification model.

## Folder assets

tokenizer.pickle; label_encoder.pickle | Used to predict the emotion of input texts.

tokenizer_chat.pickle; label_encoder_chat.pickle | Used to predict the intention of input texts.

## Jupyter notebooks

emo_model.ipynb | This is used for building the emotion classification model.

chat_model.ipynb | This is used for building the intention classification model.

chatbot.ipynb | This includes functions used to build the chat application and testing samples of the functions.

## Python files

chatbot.py | This includes functions used to build the chatbot.

tkHyperlinkManager.py | Borrowed from https://github.com/GregDMeyer/PWman/blob/master/tkHyperlinkManager.py to achieve a purpose that clicking the name of the music can open and listen to the music in the browser.

app.py | This is the final GUI to run the chat system.

## Folder evaluation

demographic.csv; demographic.ipynb | These 2 files include the merged demographic data from participants and the results for analysis.

eval.csv; evaluation.ipynb | These 2 files include the merged PANAS scores and CUQ scores from participants and the results for analysis.
