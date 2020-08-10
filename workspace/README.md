# Disaster Response Pipeline Project

# Table of Contents
1. Overview
2. Components
3. Code Structure
4. Import Package List
5. Instructions

## 1. Overview
This project is to analyze the Disaster Response Messages dataset provided by Figure Eight, after data engineering analysis, it provides a web site to present the result.

## 2. Project Components
There are three components:
### 2.1. ETL Pipeline
Load Messages and Categories csv datasets, after clean data, to save to SQLite database
### 2.2. ML Pipeline
Loads data from the SQLite database, splits datasets, train the data, use GridSearch to find best parameters
finally exports the final model as a pickle file
### 2.3. Flask Web App
A Web application that is built and run using Flask framework.

## 3. Files
+---README.md                   //Project introduction
+---package-list.txt            //conda export package list
+---workspace
    +---README.md
    +---app
    |   +---run.py              //Flask file to run the web application   
    |   +---templates           //contains html file for the web application
    |       +----go.html
    |       +----master.html
    +---data
    |   +---DisasterResponse.db      // output of the ETL pipeline
    |   +---disaster_categories.csv  // datafile of all the categories
    |   +---disaster_messages.csv    // datafile of all the messages
    |   +---process_data.py          //ETL pipeline scripts
    +---models
            train_classifier.py      //machine learning pipeline scripts to train and export a classifier


## 4. Import Package List
All of the requirements are captured in package-list.txt.
`conda create -n myenv --file package-list.txt`

## 5. Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
