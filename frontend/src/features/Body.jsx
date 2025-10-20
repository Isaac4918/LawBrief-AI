// Body.jsx
import { useState } from "react";
import { UploadDocumentButton } from "../components/UploadDocumentButton";
import { DownloadSummaryButton } from "../components/DownloadSummaryButton";
import toast from "react-hot-toast";

export default function Body() {
  const [result, setResult] = useState(null);
  const [fileName, setFileName] = useState(null);

  const handleSuccess = (result) => {
    let jsonString = result.result;

    jsonString = jsonString.replace(/\\n/g, "");
    jsonString = jsonString.replace(/\\/g, "");

    try {
      const jsonData = JSON.parse(jsonString);
      setResult(jsonData);
      setFileName(result.fileName);
      console.log("Parsed JSON data:", jsonData);
      toast.success("¡Éxito!");
    } catch (error) {
      console.error("Error al parsear JSON:", error);
      toast.error("Error al procesar el documento.");
    }
  };

  const handleError = (error) => {
    console.error("Error:", error);
  };

  return (
    <div className="container w-75 px-5 bg-white border border-light shadow-lg rounded my-5" style={{ "height": "600px", "paddingTop":"100px"}}>
      <h2 className="bac-title">Bienvenido a LawBrief AI</h2>
      <p className="border-bottom py-5">
        Tu solución integral para el análisis y resumen de documentos legales donde te ayudaremos a analizar las actas de la Asamblea Legislativa.
      </p>
      <div className="d-flex flex-row border-bottom py-4">
        <div className="border-right w-50">
          <p>
            Ingrese el archivo de texto o el documento .docx que desea analizar:
          </p>
          <div className="my-2">
            <UploadDocumentButton
              onSuccess={handleSuccess}
              onError={handleError}
            />
            <p className="text-secondary"> {fileName ? "Documento cargado: " + fileName + " ✅" : ""} </p>
          </div>
        </div>
        <div className="w-50 px-5 pb-1 border-start">
          <p>
            Descargue aquí el resumen generado por LawBrief AI:
          </p>
          <DownloadSummaryButton
            content={
              result
                ? result.temas_financieros ? ("Resumen general:\n" + result.resumen_general +
                  "\n\n\nResumen financiero:\n" + result.resumen_financiero) 
                  : 
                  ("Resumen general:\n" + result.resumen_general)
                : ""
            }
            isFinancial={result ? result.temas_financieros : false}
            disabled={result === null}
            text=" Descargar resumen"
          />
        </div>
      </div>

      <div className="mt-4"></div>
    </div>
  );
}
