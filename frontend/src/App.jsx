import React from "react";
import Header from "./features/Header";
import Body from "./features/Body";
import { Toaster } from "react-hot-toast";
import Footer from "./features/Footer";

function App() {
  return (
    <>
      <Toaster />
      <div>
        <Header />
      </div>
      <div>
        <Body />
      </div>
      <Footer />
    </>
  );
}

export default App;
