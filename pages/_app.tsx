import { AppProps } from "next/app";
import "../styles/global.css";
import G6component from "../components/Graph";

export default function App({ Component, pageProps }: AppProps) {
  return <G6component {...pageProps} />;
}
