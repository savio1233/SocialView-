# SocialView-
Prerequisite:
Python

First time starting
Download ML model (sentimental_model.joblib) from here
Copy that file into the detect folder
Run these commands in the terminal

python -m venv venv
.\venv\Scripts\activate
python -m spacy download en_core_web_sm
python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py runserver

Starting later on
Run these commands in the terminal
.\venv\Scripts\activate
python ./manage.py runserver
