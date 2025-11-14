/**
 * Pattern Selector Component
 * Select and apply waveform patterns
 */
import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Alert,
  Snackbar,
  TextField,
} from '@mui/material';
import { Send } from '@mui/icons-material';
import { patternApi } from '../../services/api';
import type { PatternConfig, PatternPreset } from '../../types';

export default function PatternSelector() {
  const [presets, setPresets] = useState<PatternPreset[]>([]);
  const [currentPattern, setCurrentPattern] = useState<PatternConfig | null>(null);
  const [selectedPreset, setSelectedPreset] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    fetchPresets();
    fetchCurrent();
  }, []);

  const fetchPresets = async () => {
    try {
      const presetsData = await patternApi.getAll();
      setPresets(presetsData);
    } catch (err: any) {
      console.error('Failed to fetch pattern presets:', err);
    }
  };

  const fetchCurrent = async () => {
    try {
      const pattern = await patternApi.getCurrent();
      setCurrentPattern(pattern);
      setSelectedPreset(pattern.pattern_type);
    } catch (err: any) {
      console.error('Failed to fetch current pattern:', err);
    }
  };

  const handlePresetChange = (patternType: string) => {
    setSelectedPreset(patternType);
    const preset = presets.find((p) => p.pattern_type === patternType);
    if (preset) {
      setCurrentPattern({
        pattern_type: preset.pattern_type,
        frequency_mhz: preset.frequency_mhz,
        cycles: preset.cycles,
        custom_hex: null,
        description: preset.description,
      });
    }
  };

  const handleApply = async () => {
    setLoading(true);
    try {
      if (currentPattern) {
        await patternApi.updateCurrent(currentPattern);
      }
      await patternApi.apply();
      setSuccess('Pattern applied to device');
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to apply pattern');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        Waveform Pattern
      </Typography>

      <Box display="flex" flexDirection="column" gap={2}>
        <FormControl size="small" fullWidth>
          <InputLabel>Pattern Type</InputLabel>
          <Select
            value={selectedPreset}
            label="Pattern Type"
            onChange={(e) => handlePresetChange(e.target.value)}
          >
            {presets.map((preset) => (
              <MenuItem key={preset.pattern_type} value={preset.pattern_type}>
                {preset.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {currentPattern && (
          <>
            <Box display="flex" gap={2}>
              <TextField
                label="Frequency (MHz)"
                type="number"
                value={currentPattern.frequency_mhz}
                onChange={(e) =>
                  setCurrentPattern({
                    ...currentPattern,
                    frequency_mhz: parseFloat(e.target.value) || 0,
                  })
                }
                size="small"
                fullWidth
                InputProps={{ readOnly: true }}
              />
              <TextField
                label="Cycles"
                type="number"
                value={currentPattern.cycles}
                onChange={(e) =>
                  setCurrentPattern({
                    ...currentPattern,
                    cycles: parseInt(e.target.value) || 0,
                  })
                }
                size="small"
                fullWidth
                InputProps={{ readOnly: true }}
              />
            </Box>

            <TextField
              label="Description"
              value={currentPattern.description}
              size="small"
              fullWidth
              multiline
              rows={2}
              InputProps={{ readOnly: true }}
            />
          </>
        )}

        <Button
          variant="contained"
          startIcon={<Send />}
          onClick={handleApply}
          disabled={loading || !currentPattern}
          fullWidth
        >
          Apply Pattern to Device
        </Button>
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

