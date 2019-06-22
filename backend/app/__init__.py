from flask import Flask
from flask_socketio import SocketIO

from config import Config
import betfair


app = Flask(__name__)
app.config.from_object(obj=Config)
socketio = SocketIO(app)

betfair_client = betfair.Betfair()


from app import socket
from app.routes import betfair
