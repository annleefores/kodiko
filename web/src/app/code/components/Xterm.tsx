import React, { useEffect, useRef } from 'react';
import { Terminal } from "xterm";
import { FitAddon } from 'xterm-addon-fit';
import { WebLinksAddon } from 'xterm-addon-web-links';
import "xterm/css/xterm.css";
import ansiColors from 'ansi-colors';

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

  const termRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const term = new Terminal({
      cursorBlink: true,
      convertEol: true,
      fontSize: 16,
      fontFamily: "Ubuntu Mono, monospace",
      theme: xtermjsTheme,
      ignoreBracketedPasteMode: true

    })

    term.open(termRef.current!);

    // fit terminal dimension to containing element

    let fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.write(` \n`)
    term.write(` ${ansiColors.green('kodiko')} $ `)

    fitAddon.fit();

    // remove terminal from dom on refresh
    return () => {
      term.dispose();
    };
  }, [])


  return (
    <div id='terminal' className='w-full h-full' ref={termRef} />
  )

};

export default Xterm;
