<script setup>
let laSensor = new LinearAccelerationSensor({frequency: 60});
import { io } from "socket.io-client";

const socket = io('https://calc-backend-na60.onrender.com');

laSensor.addEventListener("reading", (e) => {});
laSensor.start();

let id = 0;

function sendData() {
  socket.emit(`graph-acc`, {
    x: laSensor.x,
    y: laSensor.y,
    z: laSensor.z,
  });
  id++;
}

</script>

<template>
  <header>
    <p>You did it</p>
  </header>

  <main>
    <p>Hello</p>
    <p>Start sending data</p>
    <button @click="sendData">Measure</button>
  </main>
</template>

<style scoped>
</style>
