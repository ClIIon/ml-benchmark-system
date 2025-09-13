import { io } from "socket.io-client";

const socket = io("http://localhost:5000");

export function runBenchmark(params, onProgress, onResult, onError) {
  socket.emit("run_benchmark", params);

  socket.on("progress", (msg) => {
    if (onProgress) onProgress(msg);
  });

  socket.on("result", (msg) => {
    if (onResult) onResult(msg);
  });

  socket.on("error", (msg) => {
    if (onError) onError(msg);
  });
}
