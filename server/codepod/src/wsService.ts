import WebSocket from "ws";
import { Pty } from "./terminal";
import { CognitoJwtVerifier } from "aws-jwt-verify";
import dotenv from "dotenv";
import path from "path";

dotenv.config({ path: path.resolve(__dirname, "..", ".env") });

// Verifier that expects valid access tokens:
const verifier = CognitoJwtVerifier.create({
  userPoolId: process.env.COGNITO_USER_POOL_ID!,
  tokenUse: "access",
  clientId: process.env.COGNITO_CLIENT_ID!,
});

const verify = async (token: string) => {
  try {
    const payload = await verifier.verify(token);
    return payload.username;
  } catch (error) {
    console.log("Token not valid!", error);
    return null;
  }
};

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

    // TODO: Change ws path
    //initialize the WebSocket server instance
    const wss = new WebSocket.Server({ server: server, path: "/ws/" });

    console.log("Created socket server, waiting for connection");

    wss.on("connection", (ws: WebSocket, request) => {
      console.log("Client connected to socket");

      const accessToken = request.headers["sec-websocket-protocol"]!;

      verify(accessToken).then((resp) => {
        if (resp === null) {
          ws.send("HTTP/1.1 401 Unauthorized\r\n\r\n");
          ws.close();
        }

        this.ws = ws;

        this.ws.on("error", console.error);

        this.ws.on("close", () => {
          console.log("Client disconnected");
        });

        this.pty = new Pty(this.ws);

        this.ws.on("message", (input: any) => {
          // convert buffer to string
          const inputString = input.toString();

          // TODO: fix CTRL+D error

          // console.log("input-string", inputString);

          if (inputString.startsWith("\x04")) {
            // Remove ASCII character and convert string to JSON
            const jsonData = JSON.parse(inputString.replace(/\x04/g, ""));
            // console.log(jsonData);
            this.pty?.reSize(jsonData.cols, jsonData.rows);
          } else {
            this.pty?.write(inputString);
          }
        });
      });
    });
  }
}
