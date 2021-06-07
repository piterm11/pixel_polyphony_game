import React from 'react'
import "./App.css";
import {Link} from 'react-router-dom'
function Home() {
    return (
        <div className="App">
            <header className="App-header"> </header>
            <div className = "xd"> 
				<h1>Pixel Polyphony</h1>
                <Link to='/join'>
                    Join
                </Link>
            </div>
        </div>
    );
}

export default Home;
