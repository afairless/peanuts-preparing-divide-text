#! /usr/bin/env python3


def get_sibling_directory_path(sibling_directory_name):
    '''
    returns path for a specified folder that is in the same parent directory as
        the current working directory
    '''

    import os

    current_path = os.getcwd()
    last_separator_position = current_path.rfind(os.sep)
    parent_directory_path = current_path[0:last_separator_position]
    sibling_directory_path = os.path.join(parent_directory_path,
                                          sibling_directory_name)
    return(sibling_directory_path)


def split_text_by_substring(text, splitter_text):
    '''
    splits 'text' into list of substrings demarcated by 'splitter_text'
    substrings exclude 'splitter_text', specified leading and trailing
        characters in 'start_exclude' and 'end_exclude', and leading and
        trailing whitespaces
    some text descriptions are repeated; in every case, the text
        'dialogue-text' is included in 'text' and demarcates the start of the
        repetition
    '''

    double_marker = 'dialogue-text'
    double_removed = text.split(double_marker)[0]       # excludes repetition
    split_text = double_removed.split(splitter_text)

    cleaned_text = []
    min_len = 4             # minimum length of string for inclusion
    start_exclude = '>)'    # characters to exclude from start of substrings
    end_exclude = '<('      # characters to exclude from end of substrings

    for i in range(len(split_text)):
        inclusion_start = 0
        if len(split_text[i]) >= min_len:
            if split_text[i][0] in start_exclude:
                inclusion_start = 1
            if split_text[i][-1] in end_exclude:
                cleaned_text.append( split_text[i][inclusion_start:-1] )
            else:
                cleaned_text.append( split_text[i][inclusion_start:] )

    # remove leading and trailing whitespace
    for i in range(len(cleaned_text)):
        cleaned_text[i] = cleaned_text[i].strip()

    return(cleaned_text)


def prepare_text(table_filepath):
    '''
    input:  path to the 'csv' file with the names (1st column) and text
        descriptions (2nd column) in a table
    this function cleans the text descriptions by removing repetitions,
        splitting the descriptions by HTML tags that demarcate panels,
        removing extra leading and trailing punctuation and whitespace, and
        saving the original table along with the number of panels (3rd column)
        and cleaned text in a list (4th column) into a new table in a 'csv' file
    '''

    import pandas as pd

    # '^' used as separator because it does not appear in any text descriptions
    table = pd.read_csv(table_filepath, sep='^')

    text_col = 1
    text_by_row = []
    splitter = 'BR'     # HTML tag that demarcates descriptions of each panel
    number_panels = []

    for i in range(len(table)):
        text = table.iloc[i, text_col]
        if not isinstance(text, str):   # error handling for missing description
            text = ''
        text_row = split_text_by_substring(text, splitter)
        text_by_row.append(text_row)
        number_panels.append(len(text_row))

    table['num_panels'] = number_panels
    table['text_by_panels'] = text_by_row
    table.to_csv('table.csv', sep='^', index=False)


def main():
    '''
    Modifies 'csv' file of table of text descriptions (2nd column) and their
        names (1st column) and saves modified table in current working directory
    Table modifications (from 'prepare_text' comments):  cleans the text
        descriptions by removing repetitions, splitting the descriptions by HTML
        tags that demarcate panels, removing extra leading and trailing
        punctuation and whitespace, and saving the original table along with the
        number of panels (3rd column) and cleaned text in a list (4th column)
        into a new table in a 'csv' file
    Some text descriptions are repeated; in every case, the text
        'dialogue-text' is included in the description and demarcates the start
        of the repetition
    '''

    import os

    table_folder = '03_extract_text'
    table_file = 'table.csv'
    table_filepath = os.path.join(get_sibling_directory_path(table_folder),
                                  table_file)

    prepare_text(table_filepath)


if __name__ == '__main__':
    main()
