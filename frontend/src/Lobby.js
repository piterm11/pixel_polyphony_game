import "./App.css";
import "./Lobby.css";
import piano from "./graphics/piano.gif";
import flute from "./graphics/flute.gif";
import drum from "./graphics/drum.gif";
import saxophone from "./graphics/saxophone.gif";
import trumpet from "./graphics/trumpet.gif";
import axios from "axios";
import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";

function Lobby({ match }) {
  useEffect(() => {
    getData();
    const interval = setInterval(() => {
      getData();
    }, 1000);
    return () => clearInterval(interval);
  }, []);
  let history = useHistory();
  const [lobby, setItem] = useState({
    team: [],
    available_instruments: [],
    player: {},
  });
  const getData = async () => {
    const item = await axios.get(
      `http://172.104.240.119:8000/api/lobby/${match.params.id}/`
    );
    console.log("Ej");
    setItem(item.data);
    setActive(item.data.player.want_play);
    if (item.data.confirmed_players !== item.data.all_players) setTimer(10);
    else setTimer((timer) => timer - 1);
    console.log(item.data);
  };
  const getReady = async (data) => {
    const res = await axios.put(
      `http://172.104.240.119:8000/api/player/${match.params.id}/`,
      data
    );
    console.log(res);
  };

  let dataComponent = [];
  const [instrument, setInstrument] = useState(null);
  const [isActive, setActive] = useState(false);
  const [isClicked, setClicked] = useState(false);
  const toggleCliclked = () => {
    setClicked(!isClicked);
    if (!isClicked) {
      setInstrument("piano");
      setClicked2(false);
      setClicked3(false);
      setClicked4(false);
      setClicked5(false);
    } else setInstrument(null);
  };
  const [isClicked2, setClicked2] = useState(false);
  const toggleCliclked2 = () => {
    setClicked2(!isClicked2);
    if (!isClicked2) {
      setInstrument("flute");
      setClicked(false);
      setClicked3(false);
      setClicked4(false);
      setClicked5(false);
    } else setInstrument(null);
  };
  const [isClicked3, setClicked3] = useState(false);
  const toggleCliclked3 = () => {
    setClicked3(!isClicked3);
    if (!isClicked3) {
      setInstrument("saxophone");
      setClicked2(false);
      setClicked(false);
      setClicked4(false);
      setClicked5(false);
    } else setInstrument(null);
  };
  const [isClicked4, setClicked4] = useState(false);
  const toggleCliclked4 = () => {
    setClicked4(!isClicked4);
    if (!isClicked4) {
      setInstrument("drum");
      setClicked2(false);
      setClicked3(false);
      setClicked(false);
      setClicked5(false);
    } else setInstrument(null);
  };
  const [isClicked5, setClicked5] = useState(false);
  const toggleCliclked5 = () => {
    setClicked5(!isClicked5);
    if (!isClicked5) {
      setInstrument("trumpet");
      setClicked2(false);
      setClicked3(false);
      setClicked4(false);
      setClicked(false);
    } else setInstrument(null);
  };
  const toggleClass = () => {
    setActive(!isActive);
  };
  const single = (element) => {
    return {
      background: `url(${element})`,
      backgroundRepeat: "no-repeat",
      backgroundPosition: "center",
      width: "100%",
      height: "100%",
      display: "flex",
      justifyContent: "center",
      alignItems: "flex-end",
    };
  };

  const [timer, setTimer] = useState(10);

  return (
    <div className="App">
      <div className="App-header">
        <div className="lobby-container">
          <div className="instruments">
            <div className="single-instrument">
              Lobby id: {lobby.code}
              <br />
              Nick: {lobby.player.name}
            </div>
            <div
              className={`single-instrument ${
                isClicked ? "single-instrument-clicked" : ""
              } ${
                lobby.available_instruments.includes("piano") && !isActive
                  ? ""
                  : "deactive"
              }`}
              onClick={toggleCliclked}
            >
              <div style={single(piano)}>Piano</div>
            </div>
            <div
              className={`single-instrument ${
                isClicked2 ? "single-instrument-clicked" : ""
              } ${
                lobby.available_instruments.includes("flute") && !isActive
                  ? ""
                  : "deactive"
              }`}
              onClick={toggleCliclked2}
            >
              <div style={single(flute)}>Flute</div>
            </div>
            <div
              className={`single-instrument ${
                isClicked3 ? "single-instrument-clicked" : ""
              } ${
                lobby.available_instruments.includes("saxophone") && !isActive
                  ? ""
                  : "deactive"
              }`}
              onClick={toggleCliclked3}
            >
              <div style={single(saxophone)}>Saxophone</div>
            </div>
            <div
              className={`single-instrument ${
                isClicked4 ? "single-instrument-clicked" : ""
              } ${
                lobby.available_instruments.includes("drum") && !isActive
                  ? ""
                  : "deactive"
              }`}
              onClick={toggleCliclked4}
            >
              <div style={single(drum)}>Drum</div>
            </div>
            <div
              className={`single-instrument ${
                isClicked5 ? "single-instrument-clicked" : ""
              } ${
                lobby.available_instruments.includes("trumpet") && !isActive
                  ? ""
                  : "deactive"
              }`}
              onClick={toggleCliclked5}
            >
              <div style={single(trumpet)}>Trumpet</div>
            </div>
          </div>
          <div className="lobby-users" onClick={() => console.log(instrument)}>
            Users:
            {lobby.team.forEach(function (el) {
              dataComponent.push(
                <li style={{ listStyleType: "none", paddingLeft: "20px" }}>
                  {" "}
                  {el.name}{" "}
                </li>
              );
            })}
            {dataComponent}
          </div>
          <div
            className={`ready ${isActive ? "ready_active" : ""}`}
            onClick={async () => {
              toggleClass();
              if (instrument === null && lobby.player.want_play === false)
                alert("Please choose an instrument!");
              else
                getReady({
                  id: match.params.id,
                  name: lobby.player.name,
                  want_play: !lobby.player.want_play,
                  instrument: lobby.player.want_play ? null : instrument,
                });
              // console.log(isActive ? instrument : null)
              // getData()
            }}
          >
            {lobby.confirmed_players} / {lobby.all_players}
            <br />
            {/* {timer >=0 ? timer : history.push(`/game/${match.params.id}`)} */}
            {timer === 10
              ? ""
              : timer >= 0
              ? timer
              : history.push(`/game/${lobby.game_number}-${match.params.id}`)}
            <span
              style={{
                display: "block",
                position: "absolute",
                bottom: "30px",
                left: "30px",
                fontSize: "120px",
              }}
            >
              {isActive ? "Ready" : "Play"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Lobby;
