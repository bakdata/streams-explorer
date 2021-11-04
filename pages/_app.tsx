import { AppProps } from "next/app";
import Graph from "../components/Graph";

export default function App({ Component, pageProps }: AppProps) {
  return <Graph {...pageProps} />;
}
