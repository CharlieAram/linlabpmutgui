/**
 * TypeScript types for TX7332 PMUT Control
 */

export interface ChannelConfig {
  channel_id: number;
  enabled: boolean;
  mode: "TX" | "RX";
  delay_cycles: number;
  delay_fractional: boolean;
  power_down: boolean;
}

export interface BeamformingConfig {
  focal_point_x_mm: number;
  focal_point_z_mm: number;
  steering_angle_deg: number;
  speed_of_sound: number;
  auto_calculate: boolean;
}

export interface BeamformingDelays {
  delays: number[];
  focal_point_x_mm: number;
  focal_point_z_mm: number;
  steering_angle_deg: number;
}

export interface PatternConfig {
  pattern_type: string;
  frequency_mhz: number;
  cycles: number;
  custom_hex: string[] | null;
  description: string;
}

export interface PatternPreset {
  name: string;
  pattern_type: string;
  frequency_mhz: number;
  cycles: number;
  pattern_hex: number[];
  description: string;
}

export interface DeviceStatus {
  connected: boolean;
  device_type: string;
  usb_address: string | null;
  last_error: string | null;
  uptime_seconds: number | null;
}

export interface DiagnosticResult {
  check_name: string;
  passed: boolean;
  message: string;
  value: string | null;
}

export interface DiagnosticsResponse {
  timestamp: string;
  overall_status: "PASS" | "FAIL" | "WARNING";
  checks: DiagnosticResult[];
  error_count: number;
}

export interface ConfigMetadata {
  name: string;
  description: string;
  author: string;
  created_at?: string;
}

export interface DeviceConfig {
  version: string;
  device_type: string;
  timestamp: string;
  channels: ChannelConfig[];
  beamforming: BeamformingConfig;
  pattern: PatternConfig;
  metadata: ConfigMetadata;
}

export interface ConfigListItem {
  filename: string;
  name: string;
  description: string;
  created_at: string | null;
  device_type: string;
}

export interface ApiResponse {
  success: boolean;
  message: string;
  data?: any;
}

