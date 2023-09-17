import React, { useEffect, useRef } from 'react';
import { Terminal } from "xterm";
import { FitAddon } from 'xterm-addon-fit';

const Xterm: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const termRef = useRef<Terminal>();

  useEffect(() => {
    termRef.current = new Terminal({
      cursorBlink: true,
      theme: {
        background: '#fff'
      }

    });
    const fitAddon = new FitAddon();
    if (containerRef.current) {
      termRef.current.loadAddon(fitAddon)
      termRef.current.open(containerRef.current);
      fitAddon.fit()
      termRef.current.write('kodiko $ ');
    }

    return function cleanup() {
      termRef.current?.dispose();
    };
  }, []);

  return (
    <div className='border' ref={containerRef} />
  )

};

export default Xterm;
