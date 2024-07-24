import { useContext, useState } from 'react';
import {SecurityApi} from './SecurityApi.js';
import { UserContext } from "../UserContext.jsx";
import "./ticker.css";

export function SearchForm({securityMap, addTicker, removeTicker}) {
    const { user } = useContext(UserContext);
    const [searchTerm, setSearchTerm] = useState('');
    const [searchResults, setSearchResults] = useState([]);


    const handleChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const api = new SecurityApi(user.id);

    const handleSubmit = async (event) => {
        event.preventDefault();
        // Perform your search logic here using 'searchTerm'
        console.log("You searched for:", searchTerm);
        api.search(searchTerm, setSearchResults);
    };

    const handleAddStock = async (event, item) => {
        event.preventDefault()
        console.log(`Add Stock ${item.id}`)
        addTicker(item.ticker, item.last_price);
        await api.add(item.id)
    }

    const handleRemoveStock = async (event, item) => {
        event.preventDefault()
        removeTicker(item.ticker);
        console.log(`Remove Stock ${item.id}`)
        await api.remove(item.id)
    }

    return (
        <div className="search-form">
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                id="search"
                name="search"
                placeholder="Search"
                value={searchTerm}
                onChange={handleChange}
            />
            <button type="submit">Search</button>
        </form>
        <table className="search-results">
            <tbody>
            {searchResults.map((item, index) => (
                <tr key={index}>
                    <td>{item.name}</td>
                    <td className="security-ticker">{item.ticker}</td>
                    <td>${item.last_price}</td>
                    {securityMap[item.ticker]
                        ? <td><a onClick={(e) => handleRemoveStock(e, item)} href="#">Remove Stock</a></td>
                        : <td><a onClick={(e) => handleAddStock(e, item)} href="#">Add Stock</a></td>
                    }
                </tr>
            ))}
            </tbody>
        </table>
        </div>
);
}

export default SearchForm;
