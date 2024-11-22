# SocialView-
# Sentiment Analysis Web App

This project is a sentiment analysis web application built using **Python**, **Django**, and **SpaCy**. It leverages a pre-trained machine learning model (`sentimental_model.joblib`) for sentiment classification.

---

## Prerequisites

Ensure the following are installed on your system:
- **Python** (3.x recommended)  
- **pip** (Python package manager)

---

## Initial Setup

1. **Download the Sentiment Model**  
   Download the `sentimental_model.joblib` file from [this link](#) and copy it into the `detect` folder of the project.

2. **Set Up the Environment**  
   Open a terminal and run the following commands:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   python -m spacy download en_core_web_sm

3. **Database Migrations**
    Set up the database by running:

     ```bash
     python ./manage.py makemigrations
     python ./manage.py migrate

4. **Run the Server**
    To start the development server, execute the following command in the terminal:

    ```bash
    python ./manage.py runserver
