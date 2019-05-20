#!/bin/bash  
#mkdir Working


# python3 -W ignore select_files.py
shopt -s nullglob dotglob     # To include hidden files
files=(./Source/*)
if [ ${#files[@]} -gt 0 ]; 
	then 
	echo "Cleaning and Coping the Temporary Files"
	rm -rf ./Id_verify/data/demo
	rm -rf ./Id_verify/data/results/*
	rm -rf ./Id_verify/data/temp/*
	rm -rf ./Id_verify/ocr/results/*
	rm -rf ./Id_verify/Id_reults/*
	python3 delete_files_already.py
	
	##moving Source files to working
	mv Source/* Working/
	cp -r ./Working ./Id_verify/data/demo #coping the Working files to tensorflow model
	echo "Done"

	cd Id_verify
	echo "Tensorflow Server Starting"
	python3 -W ignore ./ctpn/demo_pb.py
	echo "Text Boxes Detected"
	echo "Tensorflow Server Stopped"

	echo "OCR Extracting Text for Each Text Box"
	python3 -W ignore ./ocr/ocr.py
	echo "Done"

	echo "NLP Techniques for Extracting the Valid Information"
	python3 -W ignore ./ocr/get_inf.py
	echo "DONE"
	cd ..

	#### coping the output by model to output folder 
	cp -r ./Id_verify/Id_result/json ./Output  #json
	cp -r ./Id_verify/Id_result/text ./Output  # text
	mv Working/* Output/pics/              # pics

	rm -rf ./Id_verify/Id_result/text/*
	rm -rf ./Id_verify/Id_result/json/*
	rm -rf ./Id_verify/data/demo
	rm -rf ./Id_verify/data/results/*
	rm -rf ./Id_verify/data/temp/*
	rm -rf ./Id_verify/ocr/results/*
	echo "Go To Id Result Folder for Extracting more Text Inf."; 
else
	echo "Already Up-to_date";
fi
