import React from 'react';
import socketIOClient from "socket.io-client";
import Header from './Header';
import OddsBox from '../OddsBox/OddsBox'
import './OddsLadder.css'
import { generateOddsLadder } from '../../utils'

const url = "http://127.0.0.1";
const port = "5000";
const namespace = "/test";
const endpoint = url + ":" + port + namespace;

class OddsLadder extends React.Component {
    constructor(props) {
        super(props);

        // Set the initial state of the price ladder
        let ladder = {};
        let oddsLadder = generateOddsLadder();
        oddsLadder.forEach((key) => {
            ladder[key] = {backSize: null, laySize: null, hasChanged: false}
        });

        this.state = {ladder: ladder};
    }

    componentDidMount() {
        const socket = socketIOClient(endpoint);

        socket.on("my_response", data => {
            let priceUpdate = data.priceUpdate;

            this.setState((prevState) => {
                let prevLadder = prevState.ladder;
                let newLadder = {};

                Object.keys(prevLadder).forEach((key) => {
                    let sizesUpdate = priceUpdate[key] || {"backSize": null, "laySize": null};

                    if ((sizesUpdate.backSize === prevLadder[key].backSize)  && (sizesUpdate.laySize === prevLadder[key].laySize)) {
                        Object.assign(
                            newLadder,
                            {[key]: Object.assign({}, sizesUpdate, {hasChanged: false})}
                        )

                        console.log("same");
                    } else {
                        Object.assign(
                            newLadder,
                            {[key]: Object.assign({}, sizesUpdate, {hasChanged: true})}
                        )

                        console.log("different");
                    }

                    // if (Object.keys(priceUpdate).includes(key)) {
                    //     Object.assign(
                    //         newLadder,
                    //         {[key]: Object.assign({}, priceUpdate[key], {hasChanged: true})}
                    //     )
                    // } else {
                    //     Object.assign(
                    //         newLadder,
                    //         {[key]: Object.assign({}, prevLadder[key], {hasChanged: false})}
                    //     )
                    // }
                });

                return {ladder: newLadder}
            });

        });
    }

    render() {
        let { ladder } = this.state;

        let oddsLadder = (
            Object.keys(ladder)
                .map((key) => key)
                .sort((a, b) => parseFloat(b) - parseFloat(a))
        );

        return (
            <div className="ladder-box">
                <Header/>
                <div className="ladder">
                    {oddsLadder.map((key, i) => {
                        return (
                            <OddsBox
                                key={i}
                                odds={key}
                                backSize={ladder[key].backSize}
                                laySize={ladder[key].laySize}
                                hasChanged={ladder[key].hasChanged}
                            />
                        );
                    })}
                </div>
            </div>
        )
    }
}

export default OddsLadder;
