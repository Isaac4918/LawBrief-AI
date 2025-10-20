import { useState, useRef } from 'react';
import { analyzeDocument } from '../services/analysisService';

export const UploadDocumentButton = ({ onSuccess, onError }) => {
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const ALLOWED_TYPES = {
    'text/plain': '.txt',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
  };

  const handleFileSelect = async (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    // Validar tipo de archivo
    if (!ALLOWED_TYPES[file.type]) {
      const errorMsg = `Archivo no soportado. Permitidos: ${Object.values(ALLOWED_TYPES).join(', ')}`;
      onError?.(errorMsg);
      return;
    }

    // Validar tamaño (50 MB)
    const MAX_SIZE = 50 * 1024 * 1024;
    if (file.size > MAX_SIZE) {
      const errorMsg = `Archivo demasiado grande. Máximo: 50 MB`;
      onError?.(errorMsg);
      return;
    }

    setLoading(true);
    try {
      const result = await analyzeDocument(file);
      onSuccess?.(result);
    } catch (error) {
      onError?.(error.message);
    } finally {
      setLoading(false);
      // Limpiar input para permitir subir el mismo archivo de nuevo
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <>
      <button
        onClick={handleButtonClick}
        disabled={loading}
        type="button"
        className='bac-button-basic'
      >
        {loading ? 'Analizando...' : 'Subir Documento'}
      </button>
      <input
        ref={fileInputRef}
        type="file"
        accept=".txt,.docx"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
        aria-label="Subir archivo"
      />
    </>
  );
};
