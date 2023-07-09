<script setup>
let laSensor = new LinearAccelerationSensor({frequency: 60});
import { io } from "socket.io-client";

const socket = null;

laSensor.addEventListener("reading", (e) => {
  console.log(`Linear acceleration along the X-axis ${laSensor.x}`);
  console.log(`Linear acceleration along the Y-axis ${laSensor.y}`);
  console.log(`Linear acceleration along the Z-axis ${laSensor.z}`);
});
laSensor.start();

</script>

<template>
  <header>
    <p>You did it</p>
  </header>

  <main>
    <p>Hello</p>
  </main>
</template>

<style scoped>
</style>
