from datetime import datetime
import logging
import queue
from typing import Dict, Tuple, Union

import betfairlightweight
from betfairlightweight.filters import (
    market_filter,
    streaming_market_filter,
    streaming_market_data_filter,
)

from config import BetfairConfig


logger = logging.getLogger(__name__)


class Betfair:
    """Betfair interface."""
    def __init__(self):
        logger.info("Initialising Betfair client.")
        self._client = betfairlightweight.APIClient(
            username=BetfairConfig.USERNAME,
            password=BetfairConfig.PASSWORD,
            app_key=BetfairConfig.APP_KEY,
            cert_files=[BetfairConfig.CERT_FILE, BetfairConfig.CERT_KEY_FILE]
        )

        logger.info("Logging in to Betfair.")
        self._client.login()

        self.stream: Union[
            None, betfairlightweight.streaming.betfairstream.BetfairStream
        ] = None

    def get_event_info(self, market_id: str) -> Tuple[str, str, str]:
        """Get the event information for a Betfair market ID.

        Args:
            market_id: Betfair market ID.

        Returns:
            Event type, event name and competition name.
        """
        market_filter_ = market_filter(market_ids=[market_id])

        event_type = (
            self._client
            .betting
            .list_event_types(filter=market_filter_)[0]
            .event_type
            .name
        )

        event = (
            self._client
            .betting
            .list_events(filter=market_filter_)[0]
            .event
            .name
        )

        competition = (
            self._client
            .betting
            .list_competitions(filter=market_filter_)[0]
            .competition
            .name
        )

        return event_type, event, competition

    def get_market_info(
            self, market_id: str
    ) -> Tuple[str, datetime, Dict[int, str]]:
        """Get the market information from a Betfair market ID.

        Args:
            market_id: Betfair market ID.

        Returns:
            Market name, market start time (that is, when the event starts),
            market selections mapping from ID to name.
        """
        market_filter_ = market_filter(market_ids=[market_id])

        market = (
            self._client
            .betting
            .list_market_catalogue(
                filter=market_filter_,
                market_projection=['MARKET_START_TIME', 'RUNNER_DESCRIPTION']
            )[0]
        )

        market_name = market.market_name
        market_start_time = market.market_start_time

        selections = {}
        for runner in market.runners:
            selections[runner.selection_id] = runner.runner_name

        return market_name, market_start_time, selections

    def start_betfair_ladder_stream(
            self, market_id: str, conflate_ms: float
    ) -> queue.Queue:
        """Start the Betfair ladder stream.

        Args:
            market_id: Betfair market ID.
            conflate_ms: Conflation rate in milliseconds.

        Returns:
            Market ladder queue.
        """
        if self.stream is not None:
            logger.info(
                "There is already a Betfair market stream running. Before "
                "starting a new stream, the existing one must be stopped."
            )

            ladder_queue = self.stream.listener.output_queue

            return ladder_queue

        logger.info("Initialising output queue.")
        ladder_queue = queue.Queue()

        logger.info("Initialising Betfair stream listener.")
        listener = betfairlightweight.StreamListener(ladder_queue)

        logger.info("Creating the Betfair market stream.")
        stream = self._client.streaming.create_stream(listener=listener)

        logger.info("Setting the market filter to market_id=%s.", market_id)
        market_filter_ = streaming_market_filter(market_ids=[market_id])

        logger.info("Initialising streaming market data filter.")
        market_data_filter = streaming_market_data_filter(
            # fields=['EX_MARKET_DEF', 'EX_ALL_OFFERS'],  # Without virtual bets
            fields=['EX_MARKET_DEF', 'EX_BEST_OFFERS_DISP'],  # With virtual bets
            ladder_levels=10
        )

        logger.info("Subscribing to the market.")
        stream.subscribe_to_markets(
            market_filter=market_filter_,
            market_data_filter=market_data_filter,
            conflate_ms=min(conflate_ms, 120000),
        )

        logger.info("Starting the Betfair market stream.")
        stream.start(async_=True)

        self.stream = stream

        return ladder_queue

    def stop_betfair_ladder_stream(self) -> None:
        """Stop a running Betfair ladder stream."""
        if self.stream is not None:
            logger.info("Stopping the Betfair market stream.")
            self.stream.stop()
            self.stream.listener.output_queue.put("Terminate")
            self.stream = None
        else:
            logger.info("No existing Betfair market stream to stop.")
