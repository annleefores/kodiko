import WebSocket from "ws";
import { Pty } from "./terminal";

export class wsService {
  private ws: WebSocket | null;
  private pty: Pty | null;

  constructor() {
    this.ws = null;
    this.pty = null;
  }

  attachServer(server: any): void {
    if (!server) {
      throw new Error("Server not found");
    }

    //initialize the WebSocket server instance
    const wss = new WebSocket.Server({ server });

    console.log("Created socket server, waiting for connection");

    wss.on("connection", (ws: WebSocket) => {
      console.log("Client connected to socket");

      this.ws = ws;

      this.ws.on("close", () => {
        console.log("Client disconnected");
      });

      this.pty = new Pty(this.ws);

      this.ws.on("message", (input: any) => {
        const inputString = input.toString();

        if (inputString.startsWith("\x04")) {
          console.log(inputString);
          // this.pty?.reSize(Number(inputString.cols), Number(inputString.rows));
        } else {
          this.pty?.write(inputString);
        }
      });
    });
  }
}
