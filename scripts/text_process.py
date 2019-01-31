from nltk import tokenize
from collections import Counter
import pandas as pd

def convert_to_text_blocks(dataframe, block_size):
    """
    Splits documents into blocks of sentences and returns as a dataframe.
    Parameters:
        dataframe: a dataframe containing document-level text
        block_size: the number of consecutive sentences per block
    Returns:
        dataframe_text_blocks: a new dataframe containing text at
        the level of blocks of text rather than document-level
    """
    # initialize output data dictionary
    block_dict = {'No.':[], 'Author':[], 'Text Block':[]}
    #iterate through all documents
    for i in range(dataframe.shape[0]):
        author = dataframe['Author'][i]
        no = dataframe['No.'][i]
        sentence_list = tokenize.sent_tokenize(dataframe['Text'][i])
        sentence_count = len(sentence_list)
        # iterate through sentences in each document and create blocks
        for j in range(0, sentence_count, block_size):
            idx1 = j
            idx2 = j + block_size
            if idx2 <= sentence_count:
                doc_block_list = sentence_list[idx1:idx2]
                doc_block = ' '.join(doc_block_list)
                #collect information
                block_dict['No.'].append(no)
                block_dict['Author'].append(author)
                block_dict['Text Block'].append(doc_block)
    # create output dataframe
    dataframe_text_blocks = pd.DataFrame(block_dict)
    return dataframe_text_blocks

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

