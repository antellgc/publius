from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib

import pandas as pd
pd.set_option('chained_assignment',None)

# global variables
train_data_path = "../processed_data/train_blocks.csv"
test_data_path = "../processed_data/test_blocks.csv"

def standardize_text(dataframe, text_field):
    """
    Standardizes text fields by replacing characters.
    Parameters:
        dataframe: a dataframe containing a column with text
        text_field: the column to standardize
    Returns:
        dataframe: the same dataframe corrected
    """
    dataframe[text_field] = dataframe[text_field].str.replace(r"http\S+", "")
    dataframe[text_field] = dataframe[text_field].str.replace(r"http", "")
    dataframe[text_field] = dataframe[text_field].str.replace(r"@\S+", "")
    dataframe[text_field] = dataframe[text_field].str.replace(r"[^A-Za-z0-9(),!?@\'\`\"\_\n]", " ")
    dataframe[text_field] = dataframe[text_field].str.replace(r"@", "at")
    dataframe[text_field] = dataframe[text_field].str.lower()
    return dataframe

def bag_of_words_processing(X_train, X_test):
    # intialize vectorizer
    bow_vectorizer = CountVectorizer()
    # bag of words
    X_train_bow = bow_vectorizer.fit_transform(X_train)
    X_test_bow = bow_vectorizer.transform(X_test)
    return X_train_bow, X_test_bow

def model_train(X_train_bow, y_train):
    # model fitting
    model = LogisticRegression(
        solver='saga',
        multi_class='auto',
        class_weight='balanced',
        penalty='l2',
        C=0.135,
        max_iter=1000)
    model.fit(X_train_bow, y_train)
    return model

def evaluate_model(y_test, y_test_predicted):
    report = classification_report(y_test, y_test_predicted, digits=3, output_dict=True)
    weighted_f1 = report['weighted avg']['f1-score']
    return weighted_f1

def main(train_data_path, test_data_path):
    # reads in data
    df_train_block = pd.read_csv(train_data_path)
    df_test_block = pd.read_csv(test_data_path)
    # standardizes text
    df_train_block_clean = standardize_text(df_train_block, "Text Block")
    df_test_block_clean = standardize_text(df_test_block, "Text Block")
    # select data fields
    X_train, X_test = df_train_block_clean['Text Block'], df_test_block_clean['Text Block']
    y_train, y_test = df_train_block_clean['Author'], df_test_block_clean['Author']
    # bag of words
    X_train_bow, X_test_bow = bag_of_words_processing(X_train, X_test)
    # logistic regression model train
    lr_model = model_train(X_train_bow, y_train)
    y_test_predicted = lr_model.predict(X_test_bow)
    weighted_f1 = evaluate_model(y_test, y_test_predicted)
    print(weighted_f1)
    #save model
    joblib.dump(lr_model, "../models/lr_bow_model.pkl")

if __name__ == "__main__":
    main(train_data_path, test_data_path)
