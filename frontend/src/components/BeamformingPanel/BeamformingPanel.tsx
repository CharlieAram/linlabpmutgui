/**
 * Beamforming Panel Component
 * Configure focal point and beamforming parameters
 */
import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  TextField,
  FormControlLabel,
  Switch,
  Alert,
  Snackbar,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import { Calculate, Send } from '@mui/icons-material';
import { beamformingApi } from '../../services/api';
import type { BeamformingConfig } from '../../types';

export default function BeamformingPanel() {
  const [config, setConfig] = useState<BeamformingConfig>({
    focal_point_x_mm: 0.0,
    focal_point_z_mm: 15.0,
    steering_angle_deg: 0.0,
    speed_of_sound: 1500,
    auto_calculate: true,
  });
  
  const [delays, setDelays] = useState<number[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    fetchConfig();
  }, []);

  const fetchConfig = async () => {
    try {
      const configData = await beamformingApi.getConfig();
      setConfig(configData);
    } catch (err: any) {
      console.error('Failed to fetch beamforming config:', err);
    }
  };

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const result = await beamformingApi.calculateDelays(config);
      setDelays(result.delays);
      setSuccess('Delays calculated successfully');
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to calculate delays');
    } finally {
      setLoading(false);
    }
  };

  const handleApply = async () => {
    setLoading(true);
    try {
      await beamformingApi.updateConfig(config);
      await beamformingApi.apply();
      setSuccess('Beamforming configuration applied to device');
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to apply beamforming');
    } finally {
      setLoading(false);
    }
  };

  const handlePresetSelect = async (presetName: string) => {
    try {
      const presets = await beamformingApi.getPresets();
      const preset = presets.find((p: any) => p.name === presetName);
      if (preset) {
        setConfig(preset.config);
      }
    } catch (err: any) {
      setError('Failed to load preset');
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        Beamforming Configuration
      </Typography>

      <Box display="flex" flexDirection="column" gap={2}>
        <FormControl size="small" fullWidth>
          <InputLabel>Preset</InputLabel>
          <Select
            label="Preset"
            defaultValue=""
            onChange={(e) => handlePresetSelect(e.target.value as string)}
          >
            <MenuItem value="Center focus 15mm">Center focus 15mm</MenuItem>
            <MenuItem value="Center focus 20mm">Center focus 20mm</MenuItem>
            <MenuItem value="Steering +15 degrees">Steering +15 degrees</MenuItem>
            <MenuItem value="Steering -15 degrees">Steering -15 degrees</MenuItem>
          </Select>
        </FormControl>

        <FormControlLabel
          control={
            <Switch
              checked={config.auto_calculate}
              onChange={(e) =>
                setConfig({ ...config, auto_calculate: e.target.checked })
              }
            />
          }
          label="Auto-calculate from focal point"
        />

        {config.auto_calculate ? (
          <>
            <Box display="flex" gap={2}>
              <TextField
                label="Focal Point X (mm)"
                type="number"
                value={config.focal_point_x_mm}
                onChange={(e) =>
                  setConfig({
                    ...config,
                    focal_point_x_mm: parseFloat(e.target.value) || 0,
                  })
                }
                size="small"
                fullWidth
              />
              <TextField
                label="Focal Point Z (mm)"
                type="number"
                value={config.focal_point_z_mm}
                onChange={(e) =>
                  setConfig({
                    ...config,
                    focal_point_z_mm: parseFloat(e.target.value) || 0,
                  })
                }
                inputProps={{ min: 0 }}
                size="small"
                fullWidth
              />
            </Box>
          </>
        ) : (
          <TextField
            label="Steering Angle (degrees)"
            type="number"
            value={config.steering_angle_deg}
            onChange={(e) =>
              setConfig({
                ...config,
                steering_angle_deg: parseFloat(e.target.value) || 0,
              })
            }
            inputProps={{ min: -30, max: 30 }}
            size="small"
            fullWidth
          />
        )}

        <TextField
          label="Speed of Sound (m/s)"
          type="number"
          value={config.speed_of_sound}
          onChange={(e) =>
            setConfig({
              ...config,
              speed_of_sound: parseFloat(e.target.value) || 1500,
            })
          }
          inputProps={{ min: 1000, max: 2000 }}
          size="small"
          fullWidth
        />

        <Box display="flex" gap={1}>
          <Button
            variant="outlined"
            startIcon={<Calculate />}
            onClick={handleCalculate}
            disabled={loading}
            fullWidth
          >
            Calculate Delays
          </Button>
          <Button
            variant="contained"
            startIcon={<Send />}
            onClick={handleApply}
            disabled={loading}
            fullWidth
          >
            Apply to Device
          </Button>
        </Box>

        {delays.length > 0 && (
          <Box>
            <Typography variant="caption" color="text.secondary">
              Calculated Delays (first 8): {delays.slice(0, 8).join(', ')}...
            </Typography>
          </Box>
        )}
      </Box>

      <Snackbar
        open={!!success}
        autoHideDuration={3000}
        onClose={() => setSuccess(null)}
        message={success}
      />
      <Snackbar
        open={!!error}
        autoHideDuration={5000}
        onClose={() => setError(null)}
      >
        <Alert severity="error" onClose={() => setError(null)}>
          {error}
        </Alert>
      </Snackbar>
    </Paper>
  );
}

