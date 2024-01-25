"""Split sentences in a file in SSF format into a fixed number of sentences into multiple files."""
import argparse
import re
import os


def read_content_from_files_and_split(input_folder_path, n, output_folder_path):
    '''
    :param input_folder_path: Folder Path containing SSF files
    :param n: n is the split point in this case it is 50
    :param output_folder_path: Folder path of the output folder
    :return: None
    '''
    for root, dirs, files in os.walk(input_folder_path):
        files.sort()
        for fl in files:
            file_name = fl[: fl.rfind('.')]
            input_path = os.path.join(root, fl)
            text = read_file(input_path)
            sentences = find_sentences(text)
            start = 0
            end = 0
            split_points = []
            for index, sentence in enumerate(sentences):
                if (index + 1) % n == 0:
                    if len(split_points) > 0 and len(sentences) - (index + 1) > 10:
                        split_points.append(index + 1)
                    if len(split_points) == 0:
                        split_points.append(index + 1)
            if len(split_points) == 1 and len(sentences) - split_points[-1] <= 10:
                split_points[-1] = len(sentences)
            out_file_name = file_name
            if len(split_points) > 0:
                for j in split_points:
                    end = j
                    output_path = os.path.join(output_folder_path, out_file_name + '-' + str(start + 1) + '-' + str(end) + '.txt')
                    file_out = open(output_path, 'w', encoding='utf-8')
                    file_out.write('\n\n'.join(sentences[start: end]) + "\n\n")
                    file_out.close()
                    start = end
                end = len(sentences)
                print(end, start)
                if end - start > 0:
                    if len(split_points) == 1 and len(sentences) - split_points[-1] <= 10:
                        continue
                    output_path = os.path.join(output_folder_path, out_file_name + '-' + str(start + 1) + '-' + str(end) + '.txt')
                    file_out = open(output_path, 'w', encoding='utf-8')
                    file_out.write('\n\n'.join(sentences[start: end]) + "\n\n")
                    file_out.close()
            else:
                end = len(sentences)
                output_path = os.path.join(output_folder_path, out_file_name + '-' + str(start + 1) + '-' + str(end) + '.txt')
                file_out = open(output_path, 'w', encoding='utf-8')    
                file_out.write('\n\n'.join(sentences[start: end]) + "\n\n")
                file_out.close()


def read_file(input_path):
    '''
    :param input_path: Path of the file
    :return text: Text read from the SSF file
    '''
    with open(input_path, 'r', encoding='utf-8') as input_file:
        text = input_file.read().strip()
        input_file.close()
    return text


def find_sentences(text):
    '''
    :param text: Text read from file
    :return sentences: Sentences found from the SSF file
    '''
    return re.findall('<Sentence id=.*?>.*?</Sentence>', text, re.S)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp', help="Add the input path from where tokens and its features will be extracted")
    parser.add_argument('--split', dest='n', help="Enter the split point here it is 50", type=int)
    parser.add_argument('--output', dest='out', help="Enter the output folder path")
    args = parser.parse_args()
    if not os.path.isdir(args.out):
        os.makedirs(args.out)
    read_content_from_files_and_split(args.inp, args.n, args.out)
