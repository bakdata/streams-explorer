import "../styles/global.css";
import { AppProps } from "next/app";
import dynamic from "next/dynamic";

const G6component = dynamic(() => import("../pages/G6component"), {
  ssr: false,
});

export default function App({ Component, pageProps }: AppProps) {
  // return <Component {...pageProps} />
  return (
    <div>
      <G6component {...pageProps} />
    </div>
  );
}
