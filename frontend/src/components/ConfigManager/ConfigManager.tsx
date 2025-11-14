/**
 * Config Manager Component
 * Save and load device configurations
 */
import { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
  Snackbar,
} from '@mui/material';
import { Save, FolderOpen, Delete, FileDownload } from '@mui/icons-material';
import { configApi, channelApi, beamformingApi, patternApi } from '../../services/api';
import type { ConfigListItem, DeviceConfig } from '../../types';

export default function ConfigManager() {
  const [configs, setConfigs] = useState<ConfigListItem[]>([]);
  const [saveDialogOpen, setSaveDialogOpen] = useState(false);
  const [configName, setConfigName] = useState('');
  const [configDescription, setConfigDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  useEffect(() => {
    fetchConfigs();
  }, []);

  const fetchConfigs = async () => {
    try {
      const configsData = await configApi.list();
      setConfigs(configsData);
    } catch (err: any) {
      console.error('Failed to fetch configs:', err);
    }
  };

  const handleSave = async () => {
    if (!configName) {
      setError('Please enter a configuration name');
      return;
    }

    setLoading(true);
    try {
      // Gather current configuration from all APIs
      const channels = await channelApi.getAll();
      const beamforming = await beamformingApi.getConfig();
      const pattern = await patternApi.getCurrent();

      const deviceConfig: DeviceConfig = {
        version: '1.0',
        device_type: 'TX7332',
        timestamp: new Date().toISOString(),
        channels,
        beamforming,
        pattern,
        metadata: {
          name: configName,
          description: configDescription,
          author: '',
          created_at: new Date().toISOString(),
        },
      };

      await configApi.save(configName, deviceConfig);
      await fetchConfigs();
      setSaveDialogOpen(false);
      setConfigName('');
      setConfigDescription('');
      setSuccess(`Configuration "${configName}" saved`);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to save configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleLoad = async (filename: string) => {
    setLoading(true);
    try {
      const config = await configApi.load(filename);
      
      // Apply loaded configuration to APIs
      await channelApi.updateBulk(config.channels);
      await beamformingApi.updateConfig(config.beamforming);
      await patternApi.updateCurrent(config.pattern);

      setSuccess(`Configuration "${config.metadata.name}" loaded`);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (filename: string) => {
    if (!window.confirm(`Delete configuration "${filename}"?`)) return;

    setLoading(true);
    try {
      await configApi.delete(filename);
      await fetchConfigs();
      setSuccess('Configuration deleted');
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to delete configuration');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (filename: string) => {
    try {
      const config = await configApi.export(filename);
      const blob = new Blob([JSON.stringify(config, null, 2)], {
        type: 'application/json',
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
      URL.revokeObjectURL(url);
      setSuccess('Configuration exported');
    } catch (err: any) {
      setError('Failed to export configuration');
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Configuration Management</Typography>
        <Button
          variant="contained"
          startIcon={<Save />}
          onClick={() => setSaveDialogOpen(true)}
          size="small"
        >
          Save Configuration
        </Button>
      </Box>

      <List dense>
        {configs.length === 0 ? (
          <Typography variant="body2" color="text.secondary" textAlign="center" py={2}>
            No saved configurations
          </Typography>
        ) : (
          configs.map((config) => (
            <ListItem key={config.filename} divider>
              <ListItemText
                primary={config.name}
                secondary={`${config.description || 'No description'} • ${config.device_type}`}
              />
              <ListItemSecondaryAction>
                <IconButton
                  size="small"
                  onClick={() => handleLoad(config.filename)}
                  disabled={loading}
                  title="Load"
                >
                  <FolderOpen fontSize="small" />
                </IconButton>
                <IconButton
                  size="small"
                  onClick={() => handleExport(config.filename)}
                  title="Export"
                >
                  <FileDownload fontSize="small" />
                </IconButton>
                <IconButton
                  size="small"
                  onClick={() => handleDelete(config.filename)}
                  disabled={loading}
                  title="Delete"
                >
                  <Delete fontSize="small" />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))
        )}
      </List>

      {/* Save Dialog */}
      <Dialog open={saveDialogOpen} onClose={() => setSaveDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Save Configuration</DialogTitle>
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={2} pt={1}>
            <TextField
              label="Configuration Name"
              value={configName}
              onChange={(e) => setConfigName(e.target.value)}
              fullWidth
              size="small"
              autoFocus
            />
            <TextField
              label="Description"
              value={configDescription}
              onChange={(e) => setConfigDescription(e.target.value)}
              fullWidth
              size="small"
              multiline
              rows={3}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSaveDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSave} variant="contained" disabled={loading || !configName}>
            Save
          </Button>
        </DialogActions>
      </Dialog>

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

