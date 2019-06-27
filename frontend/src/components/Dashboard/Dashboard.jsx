import React from 'react';
import './Dashboard.css'
import NavigationBar from "../NavigationBar/NavigationBar";
import MarketInfoBox from "../MarketInfoBox/MarketInfoBox";
import OddsLadder from "../OddsLadder/OddsLadder";

const Dashboard = () => {
    return (
        <div>
            <NavigationBar/>
            <div id="dashboard">
                <MarketInfoBox/>
                <OddsLadder/>
            </div>
        </div>
    )
};

export default Dashboard;
