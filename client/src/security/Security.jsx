import {useEffect, useContext, useState, useRef} from 'react';
import Ticker from "./Ticker.jsx";
import SearchForm from "./SearchForm.jsx";
import {UserContext} from "../UserContext.jsx";
import {SecurityApi} from "./SecurityApi.js";

export function Security() {

    const { user } = useContext(UserContext);
    const [securityMap, setSecurityMap] = useState({});
    const [api, setSecurityApi] = useState(null);
    const initialized = useRef(false)

    useEffect(() => {
        if (initialized.current) {
            // this is to get around dev mode calling 'useEffect' twice
            return;
        }
        initialized.current = true;

        /**
         * Connects to server over a websocket and listens for price changes
         */
        const _api = new SecurityApi(user.id);
        setSecurityApi(_api);
        _api.listenForUpdate(data => {
            setSecurityMap(securityMap => {
                return Object.assign({}, securityMap, data);
            })
        })
    }, []);


    /**
     * Callback for monitoring a new stock
     */
    const addToTicker = function(ticker, price) {
        securityMap[ticker] =  price;
        setSecurityMap(Object.assign({}, securityMap));
        api.subTicker(ticker)
    }

    /**
     * Callback for removing a stock
     */
    const removeFromTicker = function(ticker) {
        api.unsubTicker(ticker)
        securityMap[ticker] = null;
        setSecurityMap(securityMap => {
            return {
                ...securityMap,
                ticker: null
            }
        });
    }

    return (
        <div className="security-watch">
            <Ticker securityMap={securityMap}/>
            <br/>
            <br/>
            <br/>
            <SearchForm securityMap={securityMap}
                        addTicker={(ticker, price) => addToTicker(ticker, price)}
                        removeTicker={(ticker) => removeFromTicker(ticker)} />
        </div>
    );
}

export default Security;
