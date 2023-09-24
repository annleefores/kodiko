import React, { useEffect, useRef } from "react";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { WebLinksAddon } from "xterm-addon-web-links";
import { AttachAddon } from "xterm-addon-attach";
import { CanvasAddon } from "xterm-addon-canvas";

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
  };

  const xtermjsconfig = {
    cursorBlink: true,
    convertEol: true,
    fontSize: 16,
    fontFamily: "Ubuntu Mono, monospace",
    theme: xtermjsTheme,
    ignoreBracketedPasteMode: true,
  };

  const termRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const term = new Terminal(xtermjsconfig);

    // create WebSocket connection.
    const ws = new WebSocket(`${process.env.NEXT_PUBLIC_CODEPOD_WS}`);

    // fit terminal dimension to containing element and use xterm-addon-attach for websocket comms
    let fitAddon = new FitAddon();

    // xterm addon attach for ws comms from client side
    const attachAddon = new AttachAddon(ws);

    term.open(termRef.current!);
    term.loadAddon(fitAddon);
    term.loadAddon(attachAddon);
    term.loadAddon(new WebLinksAddon());
    term.loadAddon(new CanvasAddon());

    fitAddon.fit();

    // TODO: fix resizing issue when shrinking

    // Update terminal size on change and send changes to server
    const handleResize = () => {
      fitAddon.fit();
      const { rows, cols } = term;
      const size = { rows, cols };
      ws.send("\x04" + JSON.stringify(size));
    };

    // Add resize event listener
    window.addEventListener("resize", handleResize);

    ws.onopen = () => {
      handleResize();
    };
    // remove terminal from dom on refresh and close ws connection
    return () => {
      ws.close();
      window.removeEventListener("resize", handleResize);
      try {
        term?.dispose();
      } catch (error) {}
    };
  }, []);

  return <div id="terminal" className="flex-1 my-4" ref={termRef} />;
};

export default Xterm;
