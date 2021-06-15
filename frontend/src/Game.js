import "./App.css";
import "./Game.css";
import piano from "./graphics/piano.gif";
import flute from "./graphics/flute.gif";
import drum from "./graphics/drum.gif";
import saxophone from "./graphics/saxophone.gif";
import trumpet from "./graphics/trumpet.gif";
import axios from "axios";
import React, { useState, useEffect } from "react";
import piano0 from "./sounds/piano/piano0.mp3";
import piano1 from "./sounds/piano/piano1.mp3";
import piano2 from "./sounds/piano/piano2.mp3";
import piano3 from "./sounds/piano/piano3.mp3";
import piano4 from "./sounds/piano/piano4.mp3";
import piano5 from "./sounds/piano/piano5.mp3";
import piano6 from "./sounds/piano/piano6.mp3";
import piano7 from "./sounds/piano/piano7.mp3";
import drum0 from "./sounds/drum/drum0.mp3";
import drum1 from "./sounds/drum/drum1.mp3";
import drum2 from "./sounds/drum/drum2.mp3";
import drum3 from "./sounds/drum/drum3.mp3";
import drum4 from "./sounds/drum/drum4.mp3";
import drum5 from "./sounds/drum/drum5.mp3";
import drum6 from "./sounds/drum/drum6.mp3";
import drum7 from "./sounds/drum/drum7.mp3";
import saxophone0 from "./sounds/saxophone/saxophone0.mp3";
import saxophone1 from "./sounds/saxophone/saxophone1.mp3";
import saxophone2 from "./sounds/saxophone/saxophone2.mp3";
import saxophone3 from "./sounds/saxophone/saxophone3.mp3";
import saxophone4 from "./sounds/saxophone/saxophone4.mp3";
import saxophone5 from "./sounds/saxophone/saxophone5.mp3";
import saxophone6 from "./sounds/saxophone/saxophone6.mp3";
import saxophone7 from "./sounds/saxophone/saxophone7.mp3";
import flute0 from "./sounds/flute/flute0.mp3";
import flute1 from "./sounds/flute/flute1.mp3";
import flute2 from "./sounds/flute/flute2.mp3";
import flute3 from "./sounds/flute/flute3.mp3";
import flute4 from "./sounds/flute/flute4.mp3";
import flute5 from "./sounds/flute/flute5.mp3";
import flute6 from "./sounds/flute/flute6.mp3";
import flute7 from "./sounds/flute/flute7.mp3";
import trumpet0 from "./sounds/trumpet/trumpet0.mp3";
import trumpet1 from "./sounds/trumpet/trumpet1.mp3";
import trumpet2 from "./sounds/trumpet/trumpet2.mp3";
import trumpet3 from "./sounds/trumpet/trumpet3.mp3";
import trumpet4 from "./sounds/trumpet/trumpet4.mp3";
import trumpet5 from "./sounds/trumpet/trumpet5.mp3";
import trumpet6 from "./sounds/trumpet/trumpet6.mp3";
import trumpet7 from "./sounds/trumpet/trumpet7.mp3";

function Game({ match }) {
  let notesComponent = [];
  var selectedInstrument = "";
  const sounds = {
    piano: {
      note_c: piano0,
      note_D: piano1,
      note_E: piano2,
      note_F: piano3,
      note_G: piano4,
      note_A: piano5,
      note_H: piano6,
      note_C: piano7,
    },
    drum: {
      note_c: drum0,
      note_D: drum1,
      note_E: drum2,
      note_F: drum3,
      note_G: drum4,
      note_A: drum5,
      note_H: drum6,
      note_C: drum7,
    },
    saxophone: {
      note_c: saxophone0,
      note_D: saxophone1,
      note_E: saxophone2,
      note_F: saxophone3,
      note_G: saxophone4,
      note_A: saxophone5,
      note_H: saxophone6,
      note_C: saxophone7,
    },
    flute: {
      note_c: flute0,
      note_D: flute1,
      note_E: flute2,
      note_F: flute3,
      note_G: flute4,
      note_A: flute5,
      note_H: flute6,
      note_C: flute7,
    },
    trumpet: {
      note_c: trumpet0,
      note_D: trumpet1,
      note_E: trumpet2,
      note_F: trumpet3,
      note_G: trumpet4,
      note_A: trumpet5,
      note_H: trumpet6,
      note_C: trumpet7,
    },
  };

  const addNotes = () => {
    for (const [key, value] of Object.entries(notes)) {
      if (key === "c")
        notesComponent.push(
          <div
            style={{ backgroundColor: value[1], border: "none" }}
            className={`note ${key}`}
          >
            <span style={{ fontWeight: "700", marginBottom: "auto" }}>
              {key}
            </span>
            <span style={{ fontWeight: "400", textTransform: "lowercase" }}>
              {value[0]}
            </span>
          </div>
        );
      else
        notesComponent.push(
          <div style={{ backgroundColor: value[1] }} className={`note ${key}`}>
            <span style={{ fontWeight: "700", marginBottom: "auto" }}>
              {key}
            </span>
            <span style={{ fontWeight: "400", textTransform: "lowercase" }}>
              {value[0]}
            </span>
          </div>
        );
    }
  };
  const [time, setTime] = useState(0);
  var clickNotes = {
    q: 0,
    w: 1,
    e: 2,
    r: 3,
    t: 4,
    y: 5,
    u: 6,
    i: 7,
  };
  useEffect(() => {
    getData();
    let link = match.params.id.split("-");
    const socket = new WebSocket(
      `ws://172.104.240.119:8000/api/hit/${link[0]}/`
    );
    socket.onopen = () => {
      console.log("Hello from websocket");
    };
    socket.onmessage = (e) => {
      var xd = JSON.parse(e.data);
      console.log(xd);
      let instrument = xd.instrument;
      let tone = xd.tone;
      tone = "note_" + tone;
      console.log(instrument, tone);
      let audio = new Audio(sounds[instrument][tone]);
      audio.addEventListener('loadedmetadata', (e) => {
        console.log(e.target.duration);
        if (instrument === selectedInstrument){
          let xd = document.getElementsByClassName("playground")
          xd = [...xd]
          xd = xd[0]
          xd.style.boxShadow = "0 0 10px 5px green inset"
          setTimeout(() =>{
            xd.style.boxShadow = "none"
          }, e.target.duration * 1000)
        }
        else {
          let xd = document.getElementsByClassName(instrument)
          xd = [...xd]
          xd = xd[0]
          xd.style.border = "4px solid green"
          setTimeout(() =>{
            xd.style.border = "4px solid black"
          }, e.target.duration * 1000)
        }
      });
      audio.play();
    };
    const notes = document.getElementsByClassName("note");
    const notesArray = [...notes];
    notesArray.forEach((note) => {
      note.addEventListener("click", (e) => {
        let tone = e.target.className;
        tone = tone.charAt(tone.length - 1);
        console.log(selectedInstrument, e.target.className);
        socket.send(
          JSON.stringify({
            instrument: selectedInstrument,
            tone: tone,
          })
        );
      });
    });
    document.addEventListener("keydown", (e) => {
      if (e.repeat || !(e.key in clickNotes)) return;
      let tone = notesArray[clickNotes[e.key]].className;
      notesArray[clickNotes[e.key]].classList.add("note-active");
      tone = tone.charAt(tone.length - 1);
      socket.send(
        JSON.stringify({
          instrument: selectedInstrument,
          tone: tone,
        })
      );
      setTimeout(() => {
        notesArray[clickNotes[e.key]].classList.remove("note-active");
        console.log(
          selectedInstrument,
          notesArray[clickNotes[e.key]].className
        );
      }, 200);
    });
  }, []);
  const [lobby, setItem] = useState({
    team: [],
    available_instruments: [],
    player: {},
  });

  const getData = async () => {
    let link = match.params.id.split("-");
    console.log(match.params.id);
    const item = await axios.get(
      `http://172.104.240.119:8000/api/lobby/${link[1]}/`
    );
    setItem(item.data);
    console.log(item.data);
    selectedInstrument = item.data.player.instrument;
  };

  const single = (element, contain) => {
    if (element === "piano") element = piano;
    else if (element === "saxophone") element = saxophone;
    else if (element === "drum") element = drum;
    else if (element === "flute") element = flute;
    else if (element === "trumpet") element = trumpet;
    return {
      backgroundImage: `url(${element})`,
      backgroundRepeat: "no-repeat",
      backgroundPosition: "center",
      backgroundSize: contain ? "contain" : "auto",
      width: "100%",
      height: "100%",
      display: "flex",
      justifyContent: "center",
      alignItems: "flex-end",
      imageRendering: "pixelated",
    };
  };
  const notes = {
    c: ["Q", "#fb0000"],
    D: ["W", "#fb6701"],
    E: ["E", "#fff302"],
    F: ["R", "#7dfe04"],
    G: ["T", "#32f2ff"],
    A: ["Y", "#0d6bff"],
    H: ["U", "#021aff"],
    C: ["I", "#6b1aff"],
  };
  let usersComponent = [];
  const addUsers = () => {
    lobby.team.forEach((player) => {
      usersComponent.push(
        <div className={`user ${player.instrument}`}>
          <div style={single(player.instrument, false)}>{player.name}</div>
        </div>
      );
    });
  };
  return (
    <div className="App">
      <div className="App-header">
        <div className="container">
          <div className="timer">00:{time < 10 ? "0" + time : time}</div>
          <div className="username">{lobby.player.name}</div>
          <div className="users">
            {addUsers()}
            {usersComponent}
          </div>
          <div className="playground">
            <div style={single(lobby.player.instrument, true)}></div>
          </div>
          <div className="keyboard">
            <div className="labels">
              Note:
              <br />
              <br />
              <br />
              Key:
            </div>
            {addNotes()}
            {notesComponent}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Game;
