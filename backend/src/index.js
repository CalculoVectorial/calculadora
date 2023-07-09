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

io.on('connection', (socket) => {
    socket.on('graph-acc', (arg) => {
        console.log(arg);
        socket.emit('graph', { arg });
    })
})

httpServer.listen(3000, () => {
    console.log('listening on *:3000');
});