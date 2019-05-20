# Id card Varification OCR

This repository have the tool that takes the raw image as input and returns the basic information that any Id card contain(in json format). In this, first text boxes are detected using the Connectionist Text Proposal Network that is giving the accuracy around 89%. Then comes the OCR Model for converting the image into the text, for this pytesseract is the best toolkit available as the open source of tesseract-OCR thus can be directly used. Last part deals with the Information Extraction in which regex can be used and other Natural Language Technique for extracting the required information. One can update the Inforamtion Extraction part as per your need.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### PIPELINE

Pic Upload --->  Text Boxes detected using CTPN ---> OCR on each text block ---> Format and sorting of text boxes according to dimensions (for getting clear text of id card) ---> Information Extraction.
Note: For Increasing the accuracy one need to only modify the get_info file in ocr folder. This one can improve while testing.

### DATASET

Used for training = [ICDAR 2013 and 2015](http://rrc.cvc.uab.es/?ch=2)  

### NEURAL NETWORK MODEL

1. CTPN - Very deep VGG16 model implemented in Tensorflow.
2. Works reliably on multi-scale and multi- language text without further post-processing, departing from previous bottom-up methods requiring multi-step post-processing.
3. Computationally efficient with 0:14s/image.
4. Not only restricted to id cards, we can use it for any image where there is horizontal data present. Like Pan card, Adhaar card.
5. For detecting the boxes other than horizontal, one need to just change the parameters in the test.yml in cptn folder.
For Further Reading of this network : [Link](https://arxiv.org/abs/1609.03605)

### ACCURACY

Measures for given test data = 0.88 and 0.61 F-measure

### FEATURES USED

1. Fast RCNN (For detecting the text boxes at very high rate)
2. Side Refinement (for detecting the text boxes with greater accuracy)

## Installing

```
git clone https://github.com/Sourav-Markan/Id_verification_OCR.git
cd Id_verification_OCR
mkdir Id_verify/data/results Id_verify/data/temp Id_verify/Id_result 
mkdir Id_verify/Id_result/json Id_verify/Id_result/text 
mkdir Id_verify/ocr/results
sudo pip3 install -r requirements.txt
```
If fresh os system: 
```
export PYTHONPATH=path/to/lib:$PYTHONPATH
chmod +x run.sh
./run.sh
```

### For running it on virtual environment

Follow these command for setting up the virtual environment on the local system 
```
sudo pip3 install virtualenv
virtualenv venv 
```
Creating Environment: You can use any name insted of venv
```
virtualenv -p /usr/bin/python3 venv
```
Active your virtual environment
```
source venv/bin/activate
```
To deactivate- To be done at last
```
deactivate  
```
# PRE-TRAINED Model

The model I am using checkpoints is trained on GTX1070 for 50k iters.
For getting the pre-trianed model- You can directly mail me(sourav.kumar@research.iiit.ac.in)

### Running the tests

1. User image should be of extention user_id.jpg
2. Source Folder Contain the all source files.
3. Output Folders will contain results for images those are proccessed.
4. Algorithm will take care wheather image has been previously processed or not.


## TRAINING:

You may have to do several changes for training this on your system. 
```
cd lib/utils
chmod +x make.sh
./make.sh
```

### Prepare Data
Modify the path and gt_path in prepare_training_data/split_label.py according to your dataset. And run
```
cd lib/prepare_training_data
python split_label.py
```
This will generate the prepared data in current folder, and then run
```
python ToVoc.py
```
To convert the prepared training data into voc format. It will generate a folder named TEXTVOC. move this folder to 
data/ and then run
```
cd ../../data
ln -s TEXTVOC VOCdevkit2007
```
Train
```
python ./ctpn/train_net.py
```
Note: You can modify some hyper parameters in ctpn/text.yml, or just used the parameters used in this repo set.

### PARAMETERS USED

1. USE_GPU_NMS # whether to use nms implemented in cuda or not
2. DETECT_MODE # H represents horizontal mode, O represents oriented mode, default is H
3. checkpoints_path # the model I provided is in checkpoints/, if you train the model by yourself,it will be saved in output/
Note: You may need to modify according to your requirement, you can find them in ctpn/text.yml

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Author

* **Sourav Kumar** - *IIIT Hyderabad (CSD)* 
