import React from 'react';
import './Dashboard.css'
import NavigationBar from "../NavigationBar/NavigationBar";
import MarketInfoBar from "../MarketInfoBar/MarketInfoBar";
import OddsLadder from "../OddsLadder/OddsLadder";

const Dashboard = () => {
    return (
        <div id="dashboard">
            <NavigationBar/>
            <MarketInfoBar/>
            <OddsLadder/>
        </div>
    )
};

export default Dashboard;
