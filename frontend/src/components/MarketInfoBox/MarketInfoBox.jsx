import React from 'react';
import './MarketInfoBox.css'

const startLadderStream = (marketId, selectionId) => {
    const betfairUrl = 'http://localhost:5000/start_ladder_stream';

    return fetch(betfairUrl, {
        method: 'post',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "market_id": marketId,
            "selection_id": selectionId
        })
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(response.statusText);
            }
        })
        .then(data => {
            if (data) {
                return data;
            } else {
                throw new Error("No data in response");
            }
        });
};

const stopLadderStream = () => {
    const betfairUrl = 'http://localhost:5000/stop_ladder_stream';

    return fetch(betfairUrl, {
        method: 'post',
        headers: {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(response.statusText);
            }
        })
        .then(data => {
            if (data) {
                return data;
            } else {
                throw new Error("No data in response");
            }
        });
};

class MarketInfoBox extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            streaming: false,
            marketId: "",
            selectionId: null,
            eventType: "",
            eventName: "",
            competitionName: "",
            marketName: "",
            eventStartTime: null,
            selectionName: ""
        }
    }

    onMarketIdChange = (event) => {
        this.setState( {marketId: event.target.value} )
    };

    onSelectionIdChange = (event) => {
        this.setState( {selectionId: parseInt(event.target.value)} )
    };

    onStartBetfairStream = () => {
        const { marketId, selectionId } = this.state;
        startLadderStream(marketId, selectionId)
            .then(data => {
                this.setState({
                    streaming: true,
                    eventType: data.event_type,
                    eventName: data.event_name,
                    competitionName: data.competition_name,
                    marketName: data.market_name,
                    eventStartTime: data.market_start_time,
                    selectionName: data.selection_name,
                })
            })
            .catch(err => console.error(err))
    };

    onStopBetfairStream = () => {
        stopLadderStream()
            .then(data => {
                this.setState({
                    streaming: false
                })
            })
            .catch(err => console.error(err))
    };

    render() {
        let { streaming, eventType, eventName, competitionName, marketName, eventStartTime, selectionName } = this.state;

        return (
            <div id="market-info-bar">
                <div className="field">
                    <label>Market ID:</label>
                    <input
                        type="text"
                        name="market-id"
                        id="market-id"
                        placeholder="Eg: 1.234567890"
                        onChange={this.onMarketIdChange}
                    />
                </div>
                <div className="field">
                    <label>Selection ID:</label>
                    <input
                        type="number"
                        name="market-id"
                        id="market-id"
                        placeholder="Eg: 12345"
                        onChange={this.onSelectionIdChange}
                    />
                </div>
                <div className="field">
                    {
                        !streaming
                            ? <input
                                onClick={this.onStartBetfairStream}
                                type="submit"
                                value="Start"
                            />
                            : <input
                                onClick={this.onStopBetfairStream}
                                type="submit"
                                value="Stop"
                            />
                    }
                </div>
                <div className="field">&nbsp;</div>
                <div className="field">
                    <label>Event Type:</label>
                    <label>{eventType}</label>
                </div>
                <div className="field">
                    <label>Competition Name:</label>
                    <label>{competitionName}</label>
                </div>
                <div className="field">
                    <label>Event Name:</label>
                    <label>{eventName}</label>
                </div>
                <div className="field">
                    <label>Start Time:</label>
                    <label>{eventStartTime}</label>
                </div>
                <div className="field">
                    <label>Market Name:</label>
                    <label>{marketName}</label>
                </div>
                <div className="field">
                    <label>Selection Name:</label>
                    <label>{selectionName}</label>
                </div>
            </div>
        )
    }

}

export default MarketInfoBox;
