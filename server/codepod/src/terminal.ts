import * as os from "node:os";
import * as pty from "node-pty";
import WebSocket from "ws";

export class Pty {
  private shell: string;
  private ptyProcess: pty.IPty | null;
  private socket: WebSocket;

  constructor(socket: WebSocket) {
    this.shell = os.platform() === "win32" ? "powershell.exe" : "bash";
    this.ptyProcess = null;
    this.socket = socket;
    // init pty process
    this.startPtyProcess();
  }

  // spawn an instance of pty with a selected shell
  startPtyProcess() {
    this.ptyProcess = pty.spawn(this.shell, [], {
      name: "xterm-color",
      cwd: process.env.HOME,
      env: process.env,
    });

    this.ptyProcess.onData((data: any) => {
      this.sendToClient(data);
    });
  }

  write(data: any): void {
    if (this.ptyProcess) {
      this.ptyProcess.write(data);
    }
  }
  sendToClient(data: any): void {
    this.socket.send(data);
  }

  reSize(cols: number, rows: number): void {
    if (isNaN(cols) || isNaN(rows) || cols <= 0 || rows <= 0) {
      console.error("Invalid values for cols and rows:", cols, rows);
      return;
    }

    if (this.ptyProcess) {
      this.ptyProcess.resize(cols, rows);
    }
  }
}
