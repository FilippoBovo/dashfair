import React from 'react';
import './MarketInfoBar.css'

const setMarketSelection = (marketId, selectionId) => {
    const sentimentUrl = 'http://localhost:5000/betfair';

    return fetch(sentimentUrl, {
        method: 'post',
        headers: {
            // 'Authorization': 'Bearer ' + token,
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
                throw new Error("No data in response score in response");
            }
        });
};

class MarketInfoBar extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
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
        setMarketSelection(marketId, selectionId)
            .then(data => {
                this.setState({
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

    render() {
        let { eventType, eventName, competitionName, marketName, eventStartTime, selectionName } = this.state;

        return (
            <div id="market-info-bar">
                <div id="input-bar">
                    <label>Market ID</label>
                    <input
                        type="text"
                        name="market-id"
                        id="market-id"
                        onChange={this.onMarketIdChange}
                    />
                    <label>Selection ID</label>
                    <input
                        type="number"
                        name="market-id"
                        id="market-id"
                        onChange={this.onSelectionIdChange}
                    />
                    <input
                        onClick={this.onStartBetfairStream}
                        type="submit"
                        value="Start"
                    />
                </div>
                <div id="output-bar">
                    <label>Event Type: {eventType} – Competition Name: {competitionName} – Event Name: {eventName} – Start Time: {eventStartTime} – Market: {marketName} – Selection: {selectionName}</label>    
                </div>
            </div>
        )
    }

}

export default MarketInfoBar;
