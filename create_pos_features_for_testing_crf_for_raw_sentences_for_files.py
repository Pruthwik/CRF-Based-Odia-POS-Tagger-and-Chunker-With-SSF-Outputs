# how to run the code
# python3 create_pos_features_for_testing_crf_for_raw_sentences_for_files.py --input Input_Folder_Path --output Output_Folder_Path
import argparse
import os
from tokenizer_for_all_indian_languages_in_raw_format import *


def read_files_from_folder_find_features_and_write_to_files(input_folder_path, output_folder_path):
    '''
    :param input_folder_path: Input Folder Path containing all the files which you want to tag
    :return features: Features of all tokens for each sentence combined for all the sentences for all the files
    '''
    features_string = ''
    if os.path.isdir(input_folder_path):
        for root, dirs, files in os.walk(input_folder_path):
            for fl in files:
                file_path = os.path.join(root, fl)
                if '_raw' in fl:
                    file_name = fl[: fl.find('_raw.txt')]
                else:
                    file_name = fl[: fl.find('.txt')]
                output_file_name = file_name + '_features_for_pos.txt'
                output_path = os.path.join(output_folder_path, output_file_name)
                features_string = ''
                lines_read = read_file_and_tokenize(file_path, 0)
                features_string = find_features_from_sentences(lines_read)
                write_file(output_path, features_string)
    else:
        lines_read = read_file_and_tokenize(file_path, 0)
        features_string = find_features_from_sentences(lines_read)
        write_file(output_folder_path, features_string)
    return features_string


def find_features_from_sentences(sentences):
    '''
    :param sentences: Sentences read from file
    :return features: Features of all tokens for each sentence combined for all the sentences
    '''
    prefix_len = 4
    suffix_len = 7
    features = ''
    for sentence in sentences:
        sentence_features = ''
        if sentence.strip():
            tokens_split = [token for token in sentence.strip().split() if token.strip()]
            for token in tokens_split:
                sentence_features += token + '\t'
                for i in range(1, prefix_len + 1):
                    sentence_features += affix_feats(token, i, 0) + '\t'
                for i in range(1, suffix_len + 1):
                    sentence_features += affix_feats(token, i, 1) + '\t'
                sentence_features = sentence_features + 'LESS\n' if len(token) <= 4 else sentence_features + 'MORE\n'
        if sentence_features.strip():
            features += sentence_features + '\n'
    return features


def affix_feats(token, length, type_aff):
    '''
    :param line: extract the token and its corresponding suffix list depending on its length
    :param token: the token in the line
    :param length: length of affix
    :param type: 0 for prefix and 1 for suffix
    :return suffix: returns the suffix
    '''
    if len(token) < length:
        return 'NULL'
    else:
        if type_aff == 0:
            return token[:length]
        else:
            return token[len(token) - length:]


def write_file(out_path, data):
    '''
    :param out_path: Enter the path of the output file
    :param data: Enter the token features of sentence separated by a blank line
    :return: None
    '''
    with open(out_path, 'w+', encoding='utf-8') as fout:
        fout.write(data + '\n')


def main():
    '''
    Pass arguments and call functions here.
    :param: None
    :return: None
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp', help="Add the input path from where tokens and its features will be extracted")
    parser.add_argument('--output', dest='out', help="Add the output folder where the features will be saved")
    args = parser.parse_args()
    if os.path.isdir(args.inp) and not os.path.isdir(args.out):
        os.makedirs(args.out)
    read_files_from_folder_find_features_and_write_to_files(args.inp, args.out)


if __name__ == '__main__':
    main()
