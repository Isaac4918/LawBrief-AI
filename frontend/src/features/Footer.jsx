import React from "react";

export default function Footer() {
  return (
    <footer
      style={{
        backgroundColor: "#333", // gris oscuro elegante
        color: "#ccc",            // texto gris claro
        textAlign: "center",
        padding: "20px",
        position: "fixed",
        bottom: 0,
        width: "100%",
        height: "80px",
        fontSize: "0.9rem",
        letterSpacing: "0.5px"
      }}
    >
      Prueba técnica elaborada por <strong>Isaac Araya Solano</strong>
    </footer>
  );
}
