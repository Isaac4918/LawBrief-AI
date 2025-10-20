const API_URL = import.meta.env.VITE_API_URL;

export const analyzeDocument = async (file) => {

  console.log(API_URL);
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_URL}/analyze`, {
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