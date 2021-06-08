import React from 'react'
import "./App.css";
import noteBlue from "./graphics/noteBlue.gif"
import noteOrange from "./graphics/noteOrange.gif"
import noteRed from "./graphics/noteRed.gif"
import noteGreen from "./graphics/noteGreen.gif"
import {Link} from 'react-router-dom'
function Home() {
    const style_blue ={
        position: 'absolute',
        top: '35vh',
        left: '18vw'
    }
    const style_orange ={
        position: 'absolute',
        bottom: '25vh',
        left: '25vw'
    }
    const style_red ={
        position: 'absolute',
        bottom: '23vh',
        right: '20vw'
    }
    const style_green ={
        position: 'absolute',
        top: '38vh',
        right: '25vw'
    }
    return (
        <div className="App">
            <div className="App-header"> </div>
            <div className = "xd"> 
				<h1>Pixel Polyphony</h1>
                <div className="start">
                    <Link to='/join' className='link'>Join</Link>
                </div>
                <div className="start">
                    <Link to='/join' className='link'>Rate us</Link>
                </div>
            </div>
            <img src={noteBlue} alt="blue" style = {style_blue}></img>
            <img src={noteOrange} alt="blue" style = {style_orange}></img>
            <img src={noteRed} alt="blue" style = {style_red}></img>
            <img src={noteGreen} alt="blue" style = {style_green}></img>
        </div>
    );
}

export default Home;
