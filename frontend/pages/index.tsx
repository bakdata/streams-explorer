import "antd/dist/antd.css";
import dynamic from "next/dynamic";
import Head from "next/head";
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

  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta charSet="utf-8" />
        <title>Streams Explorer</title>
        <meta name="description" content="Streams Explorer" />
        <meta name="theme-color" content="#323232" />
      </Head>
      <App />
    </>
  );
}

export default Home;
