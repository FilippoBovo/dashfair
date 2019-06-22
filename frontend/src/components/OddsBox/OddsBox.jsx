import React from 'react';
import './OddsBox.css';
import { formatPrice } from '../../utils';

const OddsBox = ({odds, backSize, laySize, hasChanged}) => {
    let backSizeFormatted = formatPrice(backSize);
    let laySizeFormatted = formatPrice(laySize);

    return (
        <div className="odds-box">
            <div className="size back-color">{backSizeFormatted}</div>
            {hasChanged
                ? <div className="odds green-background">{odds}</div>
                : <div className="odds">{odds}</div>
            }
            <div className="size lay-color">{laySizeFormatted}</div>
        </div>
    )
};

export default OddsBox;
