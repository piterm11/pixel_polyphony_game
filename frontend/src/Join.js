import React from "react";
import "./App.css";
import noteBlue from "./graphics/noteBlue.gif";
import noteOrange from "./graphics/noteOrange.gif";
import noteRed from "./graphics/noteRed.gif";
import noteGreen from "./graphics/noteGreen.gif";
import { Link, useHistory } from "react-router-dom";
import axios from "axios";

function Join() {
  const style_blue = {
    position: "absolute",
    top: "20vh",
    left: "18vw",
  };
  const style_orange = {
    position: "absolute",
    bottom: "25vh",
    left: "25vw",
  };
  const style_red = {
    position: "absolute",
    bottom: "23vh",
    right: "20vw",
  };
  const style_green = {
    position: "absolute",
    top: "22vh",
    right: "25vw",
  };
  const xd = {
    marginLeft: "20px",
    color: "white",
    cursor: "pointer",
  };
  let history = useHistory();
  const redirect_lobby = (id) => {
    history.push("/lobby/" + id);
  };
  return (
    <div className="App">
      <div className="App-header"> </div>
      <div className="xd">
        <h1>Pixel Polyphony</h1>
        <form>
          <label>
            Nick:
            <input
              type="text"
              maxLength="14"
              spellCheck="false"
              name="nick"
              style={{ width: "510px" }}
            />
            <br />
          </label>
          <label>
            Room Code:
            <input
              type="text"
              maxLength="6"
              spellCheck="false"
              name="code"
              style={{ width: "250px" }}
            />
          </label>
          <br />
        </form>
      </div>
      <div className="buttons">
        <div className="start">
          <Link to="/" className="link">
            Back
          </Link>
        </div>
        <div
          className="start"
          style={xd}
          onClick={async () => {
            const nick = document.querySelector('[name="nick"]').value;
            const code = document.querySelector('[name="code"]').value;
            const login = {
              name: nick,
              code: code,
            };
            const response = await axios.post(
              "http://localhost:8000/api/join/",
              login,
              {
                headers: {
                  "Content-Type": "application/x-www-form-urlencoded",
                },
              }
            );
            redirect_lobby(response.data.player.id);
          }}
        >
          Start
        </div>
      </div>
      <img src={noteBlue} alt="blue" style={style_blue}></img>
      <img src={noteOrange} alt="blue" style={style_orange}></img>
      <img src={noteRed} alt="blue" style={style_red}></img>
      <img src={noteGreen} alt="blue" style={style_green}></img>
    </div>
  );
}

export default Join;
