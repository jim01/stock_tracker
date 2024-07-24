import { useEffect, useContext, useState, useRef } from 'react';
import {SecurityApi} from './SecurityApi.js';
import { UserContext } from "../UserContext.jsx";
import "./ticker.css";

export function Ticker({securityMap}) {

    const buildTickerDisplay = function (obj) {
        const display = [];
        Object.keys(obj).forEach(key => {
            if (obj[key]) { // don't show missing prices
                // show at least 2 decimals ex $1.10 instead of $1.1
                const price = Number(obj[key]).toLocaleString('en-US', {
                    maximumFractionDigits: 4,
                    minimumFractionDigits: 2
                });
                display.push(`${key} $${price}`);
            }
        })
        return display;
    }

    return (
        <div className="ticker-wrap">
            <div className="ticker">
                {buildTickerDisplay(securityMap).map((stock, k) => (
                    <div key={k} className="ticker__item">{stock}</div>
                ))}
            </div>
            <div className="ticker">
                {buildTickerDisplay(securityMap).map((stock,k) => (
                    <div key={k} className="ticker__item">{stock}</div>
                ))}
            </div>
        </div>
    );
}

export default Ticker;
