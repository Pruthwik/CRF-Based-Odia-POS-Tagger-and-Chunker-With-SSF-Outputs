# Only pass the input folder and the name of the output folder as arguments
# do not put a forward slash (/) at the end of the input folder
input_folder=$1
pos_model_path="odia-pos-tagger.m"
chunk_model_path="odia-chunk-tagger.m"
features_folder=$input_folder"-features"
pos_prediction_folder=$input_folder"-pred-pos"
chunk_prediction_folder=$input_folder"-pred-chunk"
corrected_chunks_folder=$input_folder"-corrected-chunk"
ssf_folder=$input_folder"-POS-Chunk-SSF"
output_folder=$2
if [ ! -d $features_folder ];then
	mkdir $features_folder
fi
if [ ! -d $pos_prediction_folder ];then
	mkdir $pos_prediction_folder
fi
if [ ! -d $chunk_prediction_folder ];then
	mkdir $chunk_prediction_folder
fi
if [ ! -d $corrected_chunks_folder ];then
	mkdir $corrected_chunks_folder
fi
if [ ! -d $ssf_folder ];then
	mkdir $ssf_folder
fi
if [ ! -d $output_folder ];then
	mkdir $output_folder
fi
python3 create_pos_features_for_testing_crf_for_raw_sentences_for_files.py --input $input_folder --output $features_folder
for fl in $(ls $features_folder);do
	file_name=$(echo $fl | sed 's/\_features\_for\_pos\.txt//g')
	echo $file_name
	input_path=$features_folder"/"$fl
	output_pos_path=$pos_prediction_folder"/"$file_name"-features-with-pos.txt" 
	output_chunk_path=$chunk_prediction_folder"/"$file_name"-pos-chunk.txt" 
	token_path=$pos_prediction_folder"/"$file_name"-token.txt" 
	pos_path=$pos_prediction_folder"/"$file_name"-pos.txt"
	pos_chunk_path=$pos_prediction_folder"/"$file_name"-pred-pos-pred-chunk.txt"
	cut -f1 $input_path > $token_path
	crf_test -m $pos_model_path $input_path > $output_pos_path
	cut -f14 $output_pos_path > $pos_path
	crf_test -m $chunk_model_path $pos_path > $pos_chunk_path
	paste $token_path $pos_chunk_path > $output_chunk_path
done
python3 correct_incorrect_chunks.py --input $chunk_prediction_folder --output $corrected_chunks_folder
python3 read_feature_files_and_convert_into_ssf.py --input $corrected_chunks_folder --output $ssf_folder --opr 1
python3 split_sentences_into_files.py --input $ssf_folder --output $output_folder --split 50
rm -rf $features_folder $pos_prediction_folder $chunk_prediction_folder $corrected_chunks_folder $ssf_folder
