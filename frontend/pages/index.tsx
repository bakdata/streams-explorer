// catch-all entry
import "antd/dist/antd.css";
import dynamic from "next/dynamic";
import { useEffect, useState } from "react";

const App = dynamic(() => import("../components/App"), { ssr: false });

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
