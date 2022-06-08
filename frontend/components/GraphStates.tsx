import React, { useMemo } from "react";

export const isBrowser = typeof window !== "undefined"; // disable SSR

interface Props {}

const GraphStates = (props: Props) => {
  const ws = useMemo(
    () =>
      isBrowser ? new WebSocket("ws://localhost:8000/api/graph/ws") : null,
    []
  );

  if (ws) {
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
      <ul id="messages"></ul>
    </>
  );
};

export default GraphStates;
