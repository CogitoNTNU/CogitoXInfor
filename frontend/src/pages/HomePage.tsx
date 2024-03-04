import { signal } from "@preact/signals-react";

export const sliderSignal = signal<number>(50);

const HomePage = () => {
  return <h1> It works</h1>;
};

export default HomePage;
