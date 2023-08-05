Steps to train this model
=========================

1. Get ADS version: [b05a40a] https://github.com/neuropoly/axondeepseg/commit/b05a40aa03979a83313fe8704ee389672ed26ed7 
2. Get the data: https://osf.io/vrdpe/?action=download&version=1
3. Run the notebook "guide_dataset_building.ipynb" to perform a split into training and validation set. 
4. Go to "training_guideline.ipynb" notebook and make necessary changes required in paths, URL’s and config. Finally run all the cells of the notebook.
5. After successfully running all the cells, the trained model file will be saved under the directory: AxonDeepSeg/axondeepseg/models/

Upload on OSF
=============
Add this README.txt file along with the model and zip the folder. 
Model is saved in OSF under the models/ directory. Example:
AxonDeepSeg/models/default_SEM_model.zip