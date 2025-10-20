const API_BASE_URL = import.meta.env.API_URL || 'http://127.0.0.1:8000';

export const analyzeDocument = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      body: formData,
      // No incluyas Content-Type header, el navegador lo establece automáticamente
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    throw new Error(`Error al analizar documento: ${error.message}`);
  }
};