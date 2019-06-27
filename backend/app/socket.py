import logging
import queue
from threading import Lock

from app import socketio, betfair_client
import utils


logger = logging.getLogger(__name__)


thread = None
thread_lock = Lock()


def send_ladder_stream(ladder_queue: queue.Queue, selection_id: int) -> None:
    """Send the ladder stream information using a socket.

    Args:
        ladder_queue: Betfair market ladder queue.
        selection_id: Selection ID.
    """
    while True:
        try:
            price_update = {}

            market_books = ladder_queue.get()

            if market_books == "Terminate":
                logger.info("Terminating ladder stream.")
                break

            market_book = market_books[0]

            for runner in market_book.runners:
                if runner.selection_id != selection_id:
                    continue

                for back in runner.ex.available_to_back:
                    back_price = utils.odds_str_repr(float(back.price))
                    price_update[back_price] = {
                        "backSize": back.size, "laySize": None
                    }

                for lay in runner.ex.available_to_lay:
                    lay_price = utils.odds_str_repr(float(lay.price))
                    price_update[lay_price] = {
                        "backSize": None, "laySize": lay.size
                    }

                data = {'priceUpdate': price_update}
                logger.info(data)

                socketio.emit('ladder_stream', data, namespace="/market_ladder")

        except KeyboardInterrupt:
            logger.info("Exiting program (Keyboard interrupt)")
            logger.info("Logging out from Betfair")
            betfair_client.logout()


def start_background_ladder_stream(
    ladder_queue: queue.Queue, selection_id: int
) -> None:
    """Start a background task to send the ladder stream information.

    Args:
        ladder_queue: Betfair market ladder queue.
        selection_id: Selection ID.
    """
    global thread

    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(
                send_ladder_stream,
                ladder_queue,
                selection_id
            )
