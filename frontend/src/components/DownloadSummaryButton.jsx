import { useState } from 'react';
import { Download } from 'lucide-react';
import html2pdf from 'html2pdf.js';

export function DownloadSummaryButton({ text = "", content = "", disabled = false, isFinancial = false }) {
  const [isLoading, setIsLoading] = useState(false);
  const [showDialog, setShowDialog] = useState(false);

  const handleDownloadClick = () => {
    setShowDialog(true);
  };

  const handleDownloadTxt = () => {
    setIsLoading(true);
    setTimeout(() => {
      const element = document.createElement('a');
      const file = new Blob([content], { type: 'text/plain' });
      element.href = URL.createObjectURL(file);
      element.download = 'resultado.txt';
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
      URL.revokeObjectURL(element.href);
      setIsLoading(false);
      setShowDialog(false);
    }, 500);
  };

  const handleDownloadPdf = () => {
    setIsLoading(true);
    setTimeout(() => {
      const element = document.createElement('div');
      element.innerHTML = `<pre style="font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; white-space: pre-wrap; word-wrap: break-word;">${content}</pre>`;
      
      const opt = {
        margin: 10,
        filename: 'resultado.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { orientation: 'portrait', unit: 'mm', format: 'a4' }
      };
      
      html2pdf().set(opt).from(element).save();
      setIsLoading(false);
      setShowDialog(false);
    }, 500);
  };

  const handleCancel = () => {
    setShowDialog(false);
  };

  return (
    <>
      <button
        onClick={handleDownloadClick}
        disabled={disabled || isLoading || showDialog}
        className="bac-button-highlighted"
      >
        <Download size={20} />
        {text}
      </button>

      {showDialog && (
        <div className="modal d-block" style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header d-flex flex-column">
                <h5 className="modal-title">{isFinancial ? "✅ El resumen contiene contenido financiero!" : "ℹ️ El resumen no contiene contenido financiero."}</h5>
                <h5 className="modal-title">¿Qué formato prefieres?</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={handleCancel}
                  disabled={isLoading}
                ></button>
              </div>
              <div className="modal-body">
                <p className="text-muted">
                  Elige el formato en el que deseas descargar el resultado.
                </p>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-success"
                  onClick={handleDownloadTxt}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Descargando...
                    </>
                  ) : (
                    'Descargar TXT'
                  )}
                </button>
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={handleDownloadPdf}
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                      Descargando...
                    </>
                  ) : (
                    'Descargar PDF'
                  )}
                </button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={handleCancel}
                  disabled={isLoading}
                >
                  Cancelar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}