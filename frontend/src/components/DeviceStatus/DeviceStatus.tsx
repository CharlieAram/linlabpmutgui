/**
 * Device Status Component
 * Shows connection status and provides connect/disconnect controls
 */
import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material';
import { FiberManualRecord, Refresh } from '@mui/icons-material';
import { deviceApi } from '../../services/api';
import type { DeviceStatus as DeviceStatusType } from '../../types';

interface DeviceStatusProps {
  onStatusChange?: (status: DeviceStatusType) => void;
}

export default function DeviceStatus({ onStatusChange }: DeviceStatusProps) {
  const [status, setStatus] = useState<DeviceStatusType | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchStatus = async () => {
    try {
      const statusData = await deviceApi.getStatus();
      setStatus(statusData);
      onStatusChange?.(statusData);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch status');
    }
  };

  useEffect(() => {
    fetchStatus();
    // Poll status every 2 seconds
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleConnect = async () => {
    setLoading(true);
    setError(null);
    try {
      const statusData = await deviceApi.connect();
      setStatus(statusData);
      onStatusChange?.(statusData);
      if (!statusData.connected) {
        setError(statusData.last_error || 'Connection failed');
      }
    } catch (err: any) {
      setError(err.message || 'Connection failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDisconnect = async () => {
    setLoading(true);
    setError(null);
    try {
      await deviceApi.disconnect();
      await fetchStatus();
    } catch (err: any) {
      setError(err.message || 'Disconnection failed');
    } finally {
      setLoading(false);
    }
  };

  const formatUptime = (seconds: number | null): string => {
    if (!seconds) return 'N/A';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}m ${secs}s`;
  };

  return (
    <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box display="flex" alignItems="center" gap={2}>
          <Typography variant="h6">Device Status</Typography>
          
          {status?.connected ? (
            <Chip
              icon={<FiberManualRecord />}
              label="Connected"
              color="success"
              size="small"
            />
          ) : (
            <Chip
              icon={<FiberManualRecord />}
              label="Disconnected"
              color="error"
              size="small"
            />
          )}

          {status?.connected && (
            <>
              <Typography variant="body2" color="text.secondary">
                Device: {status.device_type}
              </Typography>
              {status.usb_address && (
                <Typography variant="body2" color="text.secondary">
                  Port: {status.usb_address}
                </Typography>
              )}
              {status.uptime_seconds !== null && (
                <Typography variant="body2" color="text.secondary">
                  Uptime: {formatUptime(status.uptime_seconds)}
                </Typography>
              )}
            </>
          )}
        </Box>

        <Box display="flex" gap={1}>
          <Button
            variant="outlined"
            size="small"
            startIcon={<Refresh />}
            onClick={fetchStatus}
            disabled={loading}
          >
            Refresh
          </Button>
          
          {status?.connected ? (
            <Button
              variant="contained"
              color="error"
              size="small"
              onClick={handleDisconnect}
              disabled={loading}
            >
              {loading ? <CircularProgress size={20} /> : 'Disconnect'}
            </Button>
          ) : (
            <Button
              variant="contained"
              color="primary"
              size="small"
              onClick={handleConnect}
              disabled={loading}
            >
              {loading ? <CircularProgress size={20} /> : 'Connect'}
            </Button>
          )}
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}
    </Paper>
  );
}

