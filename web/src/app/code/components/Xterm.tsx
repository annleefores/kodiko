import React, { useEffect, useRef, useState } from 'react';
import { Terminal } from "xterm";
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import "xterm/css/xterm.css";
import ansiColors from 'ansi-colors';
import { AttachAddon } from 'xterm-addon-attach';
import { WebglAddon } from 'xterm-addon-webgl';
import { CanvasAddon } from 'xterm-addon-canvas';

const Xterm: React.FC = () => {

  const xtermjsTheme = {
    background: "#fffff",
    foreground: "#f8f8f2",
    cyan: "#8be9fd",
    green: "#50fa7b",
    yellow: "#f1fa8c",
    red: "#ff5555",
    cursor: "#f8f8f2",
    cursorAccent: "#282a36",
  }

  const xtermjsconfig = {
    cursorBlink: true,
    convertEol: true,
    fontSize: 16,
    fontFamily: "Ubuntu Mono, monospace",
    theme: xtermjsTheme,
    ignoreBracketedPasteMode: true

  }

  const termRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const term = new Terminal(xtermjsconfig)

    // create WebSocket connection.
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_CODEPOD_WS}`)

    // fit terminal dimension to containing element and use xterm-addon-attach for websocket comms 
    let fitAddon = new FitAddon();

    const attachAddon = new AttachAddon(ws);

    term.open(termRef.current!);
    console.log(termRef.current)
    term.loadAddon(fitAddon);
    term.loadAddon(attachAddon);
    term.loadAddon(new WebLinksAddon());
    term.loadAddon(new CanvasAddon());

    fitAddon.fit()

    // Send the terminal size to the server whenever it changes
    const handleResize = () => {
      const { rows, cols } = term;
      const size = { rows, cols };
      console.log(size)
      ws.send("\x04" + JSON.stringify(size));
    };

    // Add resize event listener
    window.addEventListener('resize', handleResize);

    // remove terminal from dom on refresh and close ws connection
    return () => {
      term.dispose();
      ws.close()
      window.removeEventListener('resize', handleResize);
    };
  }, [])


  return (

    <div id='terminal' className='w-full h-full' ref={termRef} />

  )

};

export default Xterm;
