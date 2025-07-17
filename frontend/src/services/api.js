import axios from 'axios'

const API_BASE = '/api';
const FILE_MANAGER_BASE = '/file_manager';

export const triggerScan = () => axios.post(`${FILE_MANAGER_BASE}/scan/`);
export const fetchScanStatus = () => axios.get(`${FILE_MANAGER_BASE}/status/`);
export const fetchScanResults = () => axios.get(`${FILE_MANAGER_BASE}/results/`);
