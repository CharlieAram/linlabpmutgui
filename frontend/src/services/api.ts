/**
 * API client for TX7332 PMUT Control backend
 */
import axios from 'axios';
import type {
  DeviceStatus,
  ChannelConfig,
  BeamformingConfig,
  BeamformingDelays,
  PatternConfig,
  PatternPreset,
  DiagnosticsResponse,
  DeviceConfig,
  ConfigListItem,
  ApiResponse,
} from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Device endpoints
export const deviceApi = {
  connect: async (usb_address?: string): Promise<DeviceStatus> => {
    const response = await api.post<DeviceStatus>('/device/connect', { usb_address });
    return response.data;
  },

  disconnect: async (): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>('/device/disconnect');
    return response.data;
  },

  getStatus: async (): Promise<DeviceStatus> => {
    const response = await api.get<DeviceStatus>('/device/status');
    return response.data;
  },

  reset: async (reset_type: 'hardware' | 'software' | 'memory'): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>('/device/reset', { reset_type });
    return response.data;
  },

  runDiagnostics: async (): Promise<DiagnosticsResponse> => {
    const response = await api.post<DiagnosticsResponse>('/device/diagnostics');
    return response.data;
  },
};

// Channel endpoints
export const channelApi = {
  getAll: async (): Promise<ChannelConfig[]> => {
    const response = await api.get<ChannelConfig[]>('/channels');
    return response.data;
  },

  getOne: async (channelId: number): Promise<ChannelConfig> => {
    const response = await api.get<ChannelConfig>(`/channels/${channelId}`);
    return response.data;
  },

  updateOne: async (channelId: number, config: ChannelConfig): Promise<ChannelConfig> => {
    const response = await api.put<ChannelConfig>(`/channels/${channelId}`, config);
    return response.data;
  },

  updateBulk: async (channels: ChannelConfig[]): Promise<ChannelConfig[]> => {
    const response = await api.put<ChannelConfig[]>('/channels/bulk', { channels });
    return response.data;
  },

  applyPreset: async (preset: 'all_tx' | 'all_rx' | 'half_tx_half_rx'): Promise<ChannelConfig[]> => {
    const response = await api.post<ChannelConfig[]>('/channels/preset', { preset });
    return response.data;
  },

  apply: async (): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>('/channels/apply');
    return response.data;
  },
};

// Beamforming endpoints
export const beamformingApi = {
  getConfig: async (): Promise<BeamformingConfig> => {
    const response = await api.get<BeamformingConfig>('/beamforming/config');
    return response.data;
  },

  updateConfig: async (config: BeamformingConfig): Promise<BeamformingConfig> => {
    const response = await api.put<BeamformingConfig>('/beamforming/config', config);
    return response.data;
  },

  calculateDelays: async (config: BeamformingConfig): Promise<BeamformingDelays> => {
    const response = await api.post<BeamformingDelays>('/beamforming/calculate', config);
    return response.data;
  },

  apply: async (): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>('/beamforming/apply');
    return response.data;
  },

  getPresets: async (): Promise<any[]> => {
    const response = await api.get<any[]>('/beamforming/presets');
    return response.data;
  },
};

// Pattern endpoints
export const patternApi = {
  getAll: async (): Promise<PatternPreset[]> => {
    const response = await api.get<{ patterns: PatternPreset[] }>('/patterns');
    return response.data.patterns;
  },

  getCurrent: async (): Promise<PatternConfig> => {
    const response = await api.get<PatternConfig>('/patterns/current');
    return response.data;
  },

  updateCurrent: async (pattern: PatternConfig): Promise<PatternConfig> => {
    const response = await api.put<PatternConfig>('/patterns/current', pattern);
    return response.data;
  },

  apply: async (): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>('/patterns/apply');
    return response.data;
  },

  applyPreset: async (patternType: string): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>(`/patterns/apply-preset/${patternType}`);
    return response.data;
  },

  createCustom: async (pattern: PatternConfig): Promise<PatternConfig> => {
    const response = await api.post<PatternConfig>('/patterns/custom', pattern);
    return response.data;
  },
};

// Config endpoints
export const configApi = {
  save: async (filename: string, config: DeviceConfig): Promise<ApiResponse> => {
    const response = await api.post<ApiResponse>('/config/save', { filename, config });
    return response.data;
  },

  load: async (filename: string): Promise<DeviceConfig> => {
    const response = await api.post<DeviceConfig>('/config/load', { filename });
    return response.data;
  },

  list: async (): Promise<ConfigListItem[]> => {
    const response = await api.get<{ configs: ConfigListItem[] }>('/config/list');
    return response.data.configs;
  },

  delete: async (filename: string): Promise<ApiResponse> => {
    const response = await api.delete<ApiResponse>(`/config/${filename}`);
    return response.data;
  },

  export: async (filename: string): Promise<DeviceConfig> => {
    const response = await api.get<DeviceConfig>(`/config/export/${filename}`);
    return response.data;
  },
};

export default api;

