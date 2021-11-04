// catch-all
import { useState, useEffect } from "react";
import App from "../src/App";

function Home() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
  }, []);

  if (!isMounted) {
    return null;
  }

  return <App />;
}

export default Home;
