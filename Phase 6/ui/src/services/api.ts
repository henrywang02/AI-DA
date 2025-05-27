import axios from 'axios';

const regexp = /localhost|127\.0\.0\.1/gm

// depending on setup change the api url and port
const BASE_URL = regexp.test(location.origin) ? `${location.protocol}//${location.hostname}:8000`: `${location.origin}`; // Adjust as needed
// const BASE_URL = `http://localhost:8000`; // For development

export const fetchLabelMappings = async () => {
  const response = await axios.get(`${BASE_URL}/api/v1/predict/label_mappings`);
  return response.data;
};

export const fetchOpenApiSchema = async () => {
  const response = await axios.get(`${BASE_URL}/openapi.json`);
  return response.data;
};

export const predictPrice = async (data: any) => {
  const response = await axios.post(`${BASE_URL}/api/v1/predict/price`, data);
  return response.data;
};

export const insertTrainingRow = async (data: any) => {
  const response = await axios.post(`${BASE_URL}/api/v1/predict/insert_row`, data);
  return response.data;
};

export const retrainModels = async()=>{
  const response  = await axios.post(`${BASE_URL}/api/v1/predict/__retrain_models__`);
  return response.data
}
