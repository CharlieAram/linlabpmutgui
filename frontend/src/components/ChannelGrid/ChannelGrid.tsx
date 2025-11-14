/**
 * Channel Grid Component
 * Display and configure all 32 channels
 */
import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  ToggleButtonGroup,
  ToggleButton,
  Alert,
  Snackbar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControlLabel,
  Switch,
} from '@mui/material';
import { Save, Refresh } from '@mui/icons-material';
import { channelApi } from '../../services/api';
import type { ChannelConfig } from '../../types';

export default function ChannelGrid() {
  const [channels, setChannels] = useState<ChannelConfig[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [selectedChannel, setSelectedChannel] = useState<ChannelConfig | null>(null);
  const [editDialogOpen, setEditDialogOpen] = useState(false);

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      const channelsData = await channelApi.getAll();
      setChannels(channelsData);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch channels');
    }
  };

  const handlePreset = async (preset: 'all_tx' | 'all_rx' | 'half_tx_half_rx') => {
    setLoading(true);
    try {
      const updatedChannels = await channelApi.applyPreset(preset);
      setChannels(updatedChannels);
      setSuccess(`Preset "${preset}" applied`);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to apply preset');
    } finally {
      setLoading(false);
    }
  };

  const handleApplyToDevice = async () => {
    setLoading(true);
    try {
      await channelApi.apply();
      setSuccess('Channel configuration applied to device');
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to apply configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleChannelClick = (channel: ChannelConfig) => {
    setSelectedChannel({ ...channel });
    setEditDialogOpen(true);
  };

  const handleSaveChannel = async () => {
    if (!selectedChannel) return;
    
    setLoading(true);
    try {
      await channelApi.updateOne(selectedChannel.channel_id, selectedChannel);
      await fetchChannels();
      setEditDialogOpen(false);
      setSuccess(`Channel ${selectedChannel.channel_id} updated`);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to update channel');
    } finally {
      setLoading(false);
    }
  };

  const getChannelColor = (channel: ChannelConfig) => {
    if (!channel.enabled || channel.power_down) return '#ccc';
    return channel.mode === 'TX' ? '#4caf50' : '#2196f3';
  };

  return (
    <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Channel Configuration</Typography>
        <Box display="flex" gap={1}>
          <Button
            size="small"
            variant="outlined"
            onClick={() => handlePreset('all_tx')}
            disabled={loading}
          >
            All TX
          </Button>
          <Button
            size="small"
            variant="outlined"
            onClick={() => handlePreset('all_rx')}
            disabled={loading}
          >
            All RX
          </Button>
          <Button
            size="small"
            variant="outlined"
            onClick={() => handlePreset('half_tx_half_rx')}
            disabled={loading}
          >
            Half/Half
          </Button>
          <Button
            size="small"
            variant="outlined"
            startIcon={<Refresh />}
            onClick={fetchChannels}
            disabled={loading}
          >
            Refresh
          </Button>
          <Button
            size="small"
            variant="contained"
            startIcon={<Save />}
            onClick={handleApplyToDevice}
            disabled={loading}
          >
            Apply to Device
          </Button>
        </Box>
      </Box>

      <Grid container spacing={1}>
        {channels.map((channel) => (
          <Grid item xs={1.5} key={channel.channel_id}>
            <Box
              onClick={() => handleChannelClick(channel)}
              sx={{
                cursor: 'pointer',
                p: 1,
                border: '1px solid #ddd',
                borderRadius: 1,
                backgroundColor: getChannelColor(channel),
                color: channel.enabled ? 'white' : '#666',
                textAlign: 'center',
                '&:hover': {
                  opacity: 0.8,
                },
              }}
            >
              <Typography variant="caption" display="block" fontWeight="bold">
                Ch {channel.channel_id}
              </Typography>
              <Typography variant="caption" display="block">
                {channel.mode}
              </Typography>
              <Typography variant="caption" display="block" fontSize="0.65rem">
                Δ{channel.delay_cycles}
                {channel.delay_fractional ? '.5' : ''}
              </Typography>
            </Box>
          </Grid>
        ))}
      </Grid>

      <Box mt={2}>
        <Typography variant="caption" color="text.secondary">
          Click on a channel to configure. Green = TX, Blue = RX, Gray = Disabled
        </Typography>
      </Box>

      {/* Edit Channel Dialog */}
      <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Configure Channel {selectedChannel?.channel_id}
        </DialogTitle>
        <DialogContent>
          {selectedChannel && (
            <Box display="flex" flexDirection="column" gap={2} pt={1}>
              <FormControlLabel
                control={
                  <Switch
                    checked={selectedChannel.enabled}
                    onChange={(e) =>
                      setSelectedChannel({ ...selectedChannel, enabled: e.target.checked })
                    }
                  />
                }
                label="Enabled"
              />

              <Box>
                <Typography variant="caption" display="block" gutterBottom>
                  Mode
                </Typography>
                <ToggleButtonGroup
                  value={selectedChannel.mode}
                  exclusive
                  onChange={(_, value) => {
                    if (value) setSelectedChannel({ ...selectedChannel, mode: value });
                  }}
                  fullWidth
                  size="small"
                >
                  <ToggleButton value="TX">TX (Transmit)</ToggleButton>
                  <ToggleButton value="RX">RX (Receive)</ToggleButton>
                </ToggleButtonGroup>
              </Box>

              <TextField
                label="Delay Cycles"
                type="number"
                value={selectedChannel.delay_cycles}
                onChange={(e) =>
                  setSelectedChannel({
                    ...selectedChannel,
                    delay_cycles: parseInt(e.target.value) || 0,
                  })
                }
                inputProps={{ min: 0, max: 16383 }}
                fullWidth
                size="small"
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={selectedChannel.delay_fractional}
                    onChange={(e) =>
                      setSelectedChannel({
                        ...selectedChannel,
                        delay_fractional: e.target.checked,
                      })
                    }
                  />
                }
                label="Add 0.5 Cycle Delay"
              />

              <FormControlLabel
                control={
                  <Switch
                    checked={selectedChannel.power_down}
                    onChange={(e) =>
                      setSelectedChannel({
                        ...selectedChannel,
                        power_down: e.target.checked,
                      })
                    }
                  />
                }
                label="Power Down"
              />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveChannel} variant="contained" disabled={loading}>
            Save
          </Button>
        </DialogActions>
      </Dialog>

      {/* Notifications */}
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

