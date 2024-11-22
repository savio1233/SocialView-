# SocialView-
<<<<<<< HEAD
Sentiment Analysis Web App

This project is a sentiment analysis web application built using Python, Django, and SpaCy. It uses a pre-trained machine learning model (sentimental_model.joblib) for sentiment classification.
Prerequisites

Ensure the following are installed on your system:
	•	Python (3.x recommended)
	•	pip (Python package manager)

Initial Setup

	1.	Download the Sentiment Model
Download the sentimental_model.joblib file from this link and copy it into the detect folder of the project.
	2.	Setup the Environment
Run the following commands in your terminal:

python -m venv venv
.\venv\Scripts\activate
python -m spacy download en_core_web_sm

	3.	Database Migrations
Execute the following commands to set up the database:

python ./manage.py makemigrations
python ./manage.py migrate

	4.	Run the Server
Start the development server with:
python ./manage.py runserver
Starting Later On

To resume work later, activate the virtual environment and run the server:

.\venv\Scripts\activate
python ./manage.py runserver
=======
>>>>>>> c2da91f9c35afaef30a02debfbbec0e2b7c76f50
