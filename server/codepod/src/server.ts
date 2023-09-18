import express, { Application, Request, Response } from "express";
import http from "http";
import WebSocket from "ws";

const app: Application = express();

//initialize a simple http server
const server = http.createServer(app);

//initialize the WebSocket server instance
const wss = new WebSocket.Server({ server });

const PORT = 5000;
const HOST = "0.0.0.0";

wss.on("connection", (ws: WebSocket) => {
  //connection is up, let's add a simple simple event
  ws.on("message", (message: string) => {
    //log the received message and send it back to the client
    console.log("received: %s", message);
    ws.send(`Hello, you sent -> ${message}`);
  });

  //send immediatly a feedback to the incoming connection
  ws.send("Hi there, I am a WebSocket server");
});

//start our server
server.listen(PORT, HOST, () => {
  console.log(`Server started on http://${HOST}:${PORT}`);
});
