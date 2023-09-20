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
    const wss = new WebSocket.Server({ server: server, path: "/ws/" });

    console.log("Created socket server, waiting for connection");

    wss.on("connection", (ws: WebSocket) => {
      console.log("Client connected to socket");

      this.ws = ws;

      this.ws.on("close", () => {
        console.log("Client disconnected");
      });

      this.pty = new Pty(this.ws);

      this.ws.on("message", (input: any) => {
        // convert buffer to string
        const inputString = input.toString();

        if (inputString.startsWith("\x04")) {
          // Remove ASCII character and convert string to JSON
          const jsonData = JSON.parse(inputString.replace(/\x04/g, ""));
          console.log(jsonData);
          this.pty?.reSize(jsonData.cols, jsonData.rows);
        } else {
          this.pty?.write(inputString);
        }
      });
    });
  }
}
