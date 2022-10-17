# Ecommerce API with Flask

## What is it?
This project is an web API for an ecommerce website built with Flask. The rule of routes used in this app can be found [here](https://shopping-cart-api-195.herokuapp.com/docs/#/). This app is designed to run with a fronted app, which can be found [here](https://github.com/Huy1996/react_shopping_cart).
### App Demo:
Homepage:

<img width="700" alt="Picture1" src="https://user-images.githubusercontent.com/78382696/196267165-25b00905-715d-42fc-b1cf-83a3e5572b30.png">

Checkout page:

<img width="681" alt="Picture2" src="https://user-images.githubusercontent.com/78382696/196267389-fc89a683-b9ab-4e3a-b887-f1468d72209d.png">

## Features
After connecting with the frontend, the whole app provides its customers a fully functional ecommerce website.

## Installation and Usage
 1. Install Python at: https://www.python.org/downloads/. Install pip at: https://pip.pypa.io/en/stable/installation/
 2. Download the zip file or clone the project with Git by using the command:
    ```sh
    git clone https://github.com/thuyluu9595/ecommerce-api-flask.git
    ```
 3. Unzip if the file if downloading the zip file. In the project directory, run the command to install dependencies:
    ```sh
    # Python3
    pip3 install -r requirements.txt
    ```
    or
    ```sh
    # Python2
    pip install -r requirements.txt
    ```
4. Run the following commands to set up the app:
    
    - On Windows:
    ```sh
    set FLASK_APP=run.py
    ```
    - On MAC and Linux:
    ```sh
    export FLASK_APP=run.py
    ```
5. Run the app:
    ```sh
    flask run
    ```
