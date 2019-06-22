from flask import jsonify, request

from app import app, betfair_client
from app import socket
from app.errors import bad_request


@app.route('/betfair', methods=['POST'])
def set_market_selection():
    data = request.get_json() or {}

    # Check request parameters
    if 'market_id' not in data or 'selection_id' not in data:
        return bad_request('Both Market ID and Selection ID must be given.')

    market_id = data['market_id']
    selection_id = data['selection_id']

    if market_id == '' or selection_id is None:
        return bad_request(
            'Both Market ID and Selection ID must be given a value.'
        )

    if betfair_client.stream is not None:
        betfair_client.stop_betfair_ladder_stream()

    ladder_queue = betfair_client.start_betfair_ladder_stream(
            market_id, period=1.
    )

    socket.start_background_ladder_stream(ladder_queue, selection_id, period=1.)

    # Get event, market and selection information
    event_type, event, competition = betfair_client.get_event_info(market_id)
    market_name, market_start_time, selections = \
        betfair_client.get_market_info(market_id)
    selection_name = selections[selection_id]

    response = jsonify(
        {
            'event_type': event_type,
            'event_name': event,
            'competition_name': competition,
            'market_name': market_name,
            'market_start_time': market_start_time,
            'selection_name': selection_name
        }
    )

    return response
