<script setup>
let laSensor = new LinearAccelerationSensor({frequency: 60});
import { io } from "socket.io-client";

const socket = io('https://calc-backend-na60.onrender.com');

laSensor.addEventListener("reading", (e) => {});
laSensor.start();

let id = 0;

const ticks = 1000 / 60;

function send() {
  socket.emit('graph-acc', {
    x: laSensor.x,
    y: laSensor.y,
    z: laSensor.z,
  });
}

function measureData() {
  setInterval(send, ticks);
}

</script>

<template>
  <header>
    <p>You did it</p>
  </header>

  <main>
    <p>Hello</p>
    <p>Start sending data</p>
    <button @click="measureData">Measure</button>
  </main>
</template>

<style scoped>
</style>
