import { useState } from "react";
// import "./styles/General.css";

export default function Header() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-white border-bottom">
      <img
        src="BAC_LOGO.png"
        alt="Logo"
        width="170rem"
        style={{ marginLeft: "3.5rem" }}
        className="d-inline-block align-text-top p-2 my-2"
      />
      <h1 className="bac-title-header mt-4 mx-3">
        LawBrief AI
      </h1>
    </nav>
  );
}
