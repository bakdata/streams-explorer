// catch-all
import { useState, useEffect } from "react";
// import App from "../src/App";
import dynamic from "next/dynamic";

const App = dynamic(() => import("../src/App"), { ssr: false });

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
