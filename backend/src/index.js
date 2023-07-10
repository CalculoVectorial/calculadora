const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
    cors: {
        origin: '*'
    }
});

const roomId = 1;

io.on('connection', (socket) => {
    let pythonService = true;

    socket.on('measure', (arg) => {        
        socket.join(roomId);
        socket.broadcast.to(roomId).emit('graph', arg);
        pythonService = false;
    })

    if (pythonService) {
        socket.join(roomId);
    }
});

httpServer.listen(3000, () => {
    console.log('listening on *:3000');
});