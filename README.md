# Heatmap
Graphically view input from mat.


## Setup
Built in Python3 and relies on the SciPy stack. On Windows, the easiest way to use the SciPy
stack is through [Anaconda](https://www.continuum.io/downloads).

1. Install the SciPy stack using your preferred method.
2. Install virtualenv (it may already be installed) with `python -m pip install virtualenv`
3. Install virtualenv to the `env/` folder using `python -m virtualenv env`
4. Activate the env using `env\Scripts\activate` (Windows) or `env/bin/activate` otherwise.
5. With the env activated, install requirements with `pip install -r requirements.txt`


## Run the software
1. Modify the configuration in `serial_com/` for the size of the matt.
2. Use the Arduino IDE to install the sketch to the device.
3. Modify the configuration in `heatmap/__init__.py` for rows and columns and any other config.
4. Activate the env using `env\Scripts\activate` (Windows) or `env/bin/activate` otherwise.
5. Run configurations:
    1. To run with random sample data, run `python run.py fake`
    2. To get data from serial, run `python run.py serial`
    3. To save the data after you quit, add a filename to the command, i.e. `python run.py serial push_up`
       to save the session to `data/push_up_TIMESTAMP.json'`
        - While running, press Enter to save a new section in the data.
    4. To replay saved data, run `python run.py replay FILENAME.json`
        - you can also request a single frame by adding arguments, i.e. `python run.py replay FILANAME 3 22`
          will grab index 22 from section 3 of FILENAME.


## Analysis

1. Install TensorFlow: https://www.tensorflow.org/install/
2. To convert saved data into digestible formats, run `python model.py create`
    - results can be previewed as images by running `python model.py preview`
3. To train the model, run `python model.py train`
    - To train on top of a prior model, run `python model.py train r`