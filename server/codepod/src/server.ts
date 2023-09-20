import express, { Application, Request, Response } from "express";
import http from "http";
import { wsService } from "./wsService";

const app: Application = express();

//initialize a simple http server
const server = http.createServer(app);

const PORT = 5000;
const HOST = "0.0.0.0";

//start server and attach websocket
server.listen(PORT, HOST, () => {
  console.log(`Server started on http://${HOST}:${PORT}`);
  const socket = new wsService();
  socket.attachServer(server);
});
