import React, { useEffect, useMemo, useState } from "react";

export const isBrowser = typeof window !== "undefined"; // disable SSR

interface Props {}

const readyStates = {
  [WebSocket.CONNECTING]: "Connecting",
  [WebSocket.OPEN]: "Open",
  [WebSocket.CLOSING]: "Closing",
  [WebSocket.CLOSED]: "Closed",
  [4]: "Uninstantiated",
};

const GraphStates = (props: Props) => {
  const ws = useMemo(
    () =>
      isBrowser ? new WebSocket("ws://localhost:8000/api/graph/ws") : null,
    []
  );

  const [connectionStatus, setConnectionStatus] = useState(readyStates[4]);

  useEffect(() => {
    setConnectionStatus(readyStates[ws?.readyState ? ws?.readyState : 4]);
  }, [ws?.readyState]);

  if (ws) {
    ws.onopen = function () {
      console.log("WebSocket opened");
    };

    ws.onclose = function () {
      console.log("WebSocket closed");
    };

    ws.onerror = function (event) {
      console.log("WebSocket error", event);
    };

    ws.onmessage = function (event) {
      const messages = document.getElementById("messages");
      const message = document.createElement("li");
      const content = document.createTextNode(
        "Message from server: " + event.data
      );
      message.appendChild(content);
      messages?.appendChild(message);
    };
  }

  return (
    <>
      <p>WebSocket readyState: {connectionStatus}</p>
      <ul id="messages"></ul>
    </>
  );
};

export default GraphStates;
