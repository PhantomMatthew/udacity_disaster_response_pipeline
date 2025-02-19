import re
import sys, pickle
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sqlalchemy import create_engine

def load_data(database_filepath):
    '''
    To load data

    Args:
        params: database full path

    Returns:
        Features, label, category_names
    '''
    table_name = 'DisasterMessages2'
    engine = create_engine(f"sqlite:///{database_filepath}")
    df = pd.read_sql_table(table_name,engine)
    X = df['message']
    y = df.drop(["message","id","genre","original"], axis=1)
    category_names = y.columns
    return X, y, category_names

def tokenize(text):
    '''
    To tokenize the text messages
    Args:
        params: text need to tokenize
    Returns:
        return cleaned tokens
    '''
    # remove special characters and lowercase
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    clean_tokens = []
    for token in tokens:
        clean_token = lemmatizer.lemmatize(token).lower().strip()
        clean_tokens.append(clean_token)
    return clean_tokens


def build_model():
    '''
    To build model
    Args:
        None

    Returns:
        return grid searched model
    '''
    pipeline = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier()))])
    
    parameters = {
        'tfidf__use_idf': (True, False),
        'clf__estimator__n_estimators': [50, 100, 200],
        'clf__estimator__min_samples_split': [2,3,4]
        } 
    cv = GridSearchCV(pipeline, param_grid=parameters, n_jobs=-1)
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    To print out the accuracy scores

    Args:
        params1: model to evaluate
        params2: Test set
        params3: Test prediction vector
        params4: category names

    Returns:
        None
    '''
    y_pred = model.predict(X_test)
    print(classification_report(y_pred, Y_test.values, target_names=category_names))
    # print raw accuracy score 
    print('Accuracy Score: {}'.format(np.mean(Y_test.values == y_pred)))


def save_model(model, model_filepath):
    '''
    To save model to pickle file format

    Args:
        params1: model to save
        params2: model saved full path
    '''
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()