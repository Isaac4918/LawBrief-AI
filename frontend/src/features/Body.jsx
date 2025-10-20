import { useState } from "react";
import { UploadDocumentButton } from "../components/UploadDocumentButton";
// import "./styles/General.css";

export default function Body() {
  const handleSuccess = (result) => {
    let jsonString = result.result;

    jsonString = jsonString.replace(/\\n/g, ""); // quitar saltos de línea
    jsonString = jsonString.replace(/\\/g, ""); // quitar backslashes

    try {
      const jsonData = JSON.parse(jsonString);
      // console.log("Análisis completado:", result.result);
      console.log("Análisis completado:", jsonData);
    } catch (error) {
      console.error("Error al parsear JSON:", error);
    }
    // Hacer algo con el resultado
  };

  const handleError = (error) => {
    console.error("Error:", error);
    // Mostrar error al usuario
  };

  return (
    <div className="container w-75 p-3 py-5 bg-white">
      <h2 className="bac-title">Bienvenido a LawBrief AI</h2>
      <p className="border-bottom py-3">
        Tu solución integral para el análisis y resumen de documentos legales.
      </p>
      <p>
        Ingrese el archivo de texto o el documento .docx que desea analizar:
      </p>
      <UploadDocumentButton onSuccess={handleSuccess} onError={handleError} />
    </div>
  );
}
