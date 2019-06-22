import logging
import sys

from flask_cors import CORS

from app import app, socketio


if __name__ == "__main__":
    logging.basicConfig(
        format='%(levelname)-8s | %(asctime)s | %(name)s:  %(message)s',
        level=logging.INFO,
        stream=sys.stdout
    )

    CORS(app)

    socketio.run(app)
