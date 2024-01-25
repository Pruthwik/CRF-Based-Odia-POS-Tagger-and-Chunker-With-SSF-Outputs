# CRF Based POS Tagger and Chunker on raw sentences
- This shell script runs following programs
  1. create_pos_features_for_testing_crf_for_raw_sentences_for_files.py - This program tokenizes raw sentences and create features for POS tagging using BIS annotation scheme
  2. Predictions using CRF based models for Odia POS Tagger and Chunker
  3. correct_incorrect_chunks.py - Correct the incorrect chunk predictions - If you need outputs in the CONLL format, comment the codes below it.
  4. read_feature_files_and_convert_into_ssf.py - Convert the CONLL POS and Chunk predictions into SSF format.
  5. split_sentences_into_files.py - Split each file into files of 50 sentences each
