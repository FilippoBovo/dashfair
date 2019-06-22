# DashFair

DashFair is a simple interface, built using Python's [Flask](http://flask.pocoo.org/) and Javascript's [React](https://reactjs.org/), to view the market ladder of a selection in [Betfair](https://www.betfair.com/).

Note that you need to have a Betfair account and a [Betfair API key](https://developer.betfair.com/en/get-started/) with the streaming service enabled.

## Install

Clone the repository.

```shell
git clone https://github.com/FilippoBovo/dashfair.git
cd dashfair
```

Create a Python virtual environment, here using [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/), and Python 3.7, and Install the Python requirements.

```shell
mkvirtualenv --python=python3.7 dashfair
pip install -r backend/requirements.txt
```

Install the Node.js packages.

```
cd frontend
npm install
cd ..
```

##  Set up

Set the environment variables to log in to Betfair using the API key.

```shell
export BETFAIR_USERNAME=...
export BETFAIR_PASSWORD=...
export BETFAIR_APP_KEY=...
export BETFAIR_CERT_FILE=...
export BETFAIR_CERT_KEY_FILE=...
```

Fill the dots using your credentials. For the last two environmental variables, you have to give the path to the respective files stored in your local machine.

## Run

To start DashFair, launch the Flask backend application.

```shell
cd backend
python backend.py
```

Then, open a new terminal, go to the repository folder and start the React frontend.

```shell
cd frontend
npm start
```

