# Heatmap
Graphically view input from mat.


## Setup
Built in Python3 and relies on the SciPy stack. On Windows, the easiest way to use the SciPy
stack is through [Anaconda](https://www.continuum.io/downloads).

1. Install the SciPy stack using your preferred method. The python3 binary with
SciPy installed shall hereon be referred to as `anaconda3`
2. Install virtualenv (it may already be installed) with `anaconda3 -m pip install virtualenv env`
3. Install vitualenv to the `env/` folder using `anaconda3 -m virtualenv env`
4. Activate the env using `env\Scripts\activate` (Windows) or `env/bin/activate` otherwise.
5. With the env activated, install requirements with `pip install -r requirements.txt`

The Arduino Sketch relies on the following libraries:

- ArduinoJson: https://github.com/bblanchon/ArduinoJson


## Run the software
1. Modify the configuration in `serial_com/` for the size of the matt.
2. Use the Arduino IDE to install the sketch to the device.
3. Modify the configuration in `heatmap/__init__.py` for rows and columns and any other config.
4. With the virtualenv activated
    1. To run with random sample data, run `anaconda3 run.py fake`
    2. To get data from serial, run `anaconda3 run.py serial`
