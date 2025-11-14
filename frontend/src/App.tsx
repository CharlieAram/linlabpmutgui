/**
 * Main Application Component
 * TX7332 PMUT Control Panel
 */
import { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  AppBar,
  Toolbar,
  Grid,
  Tabs,
  Tab,
  Paper,
  ThemeProvider,
  createTheme,
  CssBaseline,
} from '@mui/material';
import { Settings, Waves, Storage, BugReport } from '@mui/icons-material';
import DeviceStatus from './components/DeviceStatus';
import ChannelGrid from './components/ChannelGrid';
import BeamformingPanel from './components/BeamformingPanel';
import PatternSelector from './components/PatternSelector';
import ConfigManager from './components/ConfigManager';
import DiagnosticsPanel from './components/DiagnosticsPanel';
import type { DeviceStatus as DeviceStatusType } from './types';

// Create Material-UI theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ pt: 2 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [deviceStatus, setDeviceStatus] = useState<DeviceStatusType | null>(null);
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (_: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      
      <AppBar position="static">
        <Toolbar>
          <Waves sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            TX7332 PMUT Control Panel
          </Typography>
          <Typography variant="body2">
            v1.0.0
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 3, mb: 3 }}>
        {/* Device Status Bar */}
        <DeviceStatus onStatusChange={setDeviceStatus} />

        {/* Main Control Tabs */}
        <Paper elevation={2}>
          <Tabs
            value={currentTab}
            onChange={handleTabChange}
            indicatorColor="primary"
            textColor="primary"
          >
            <Tab icon={<Settings />} label="Channels & Beamforming" />
            <Tab icon={<Waves />} label="Pattern" />
            <Tab icon={<Storage />} label="Configuration" />
            <Tab icon={<BugReport />} label="Diagnostics" />
          </Tabs>
        </Paper>

        {/* Tab: Channels & Beamforming */}
        <TabPanel value={currentTab} index={0}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <ChannelGrid />
            </Grid>
            <Grid item xs={12} md={6}>
              <BeamformingPanel />
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper elevation={2} sx={{ p: 2, height: '100%' }}>
                <Typography variant="h6" gutterBottom>
                  Quick Guide
                </Typography>
                <Typography variant="body2" paragraph>
                  <strong>Channels:</strong> Click on any channel to configure its mode (TX/RX), delays, and power settings.
                </Typography>
                <Typography variant="body2" paragraph>
                  <strong>Beamforming:</strong> Set focal point coordinates or steering angle to focus the ultrasound beam.
                </Typography>
                <Typography variant="body2" paragraph>
                  <strong>Workflow:</strong>
                </Typography>
                <Typography variant="body2" component="ol" sx={{ pl: 2 }}>
                  <li>Configure channels (TX/RX modes)</li>
                  <li>Set beamforming parameters</li>
                  <li>Apply configuration to device</li>
                  <li>Select and apply waveform pattern</li>
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Tab: Pattern */}
        <TabPanel value={currentTab} index={1}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <PatternSelector />
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper elevation={2} sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Pattern Information
                </Typography>
                <Typography variant="body2" paragraph>
                  Select a waveform pattern to apply to the device. Available patterns include:
                </Typography>
                <Typography variant="body2" component="ul">
                  <li><strong>5.6 MHz 3-Level:</strong> Standard high-frequency waveform</li>
                  <li><strong>3.4 MHz 2-Level:</strong> Lower frequency for deeper penetration</li>
                  <li><strong>Custom patterns:</strong> Define your own waveform parameters</li>
                </Typography>
                <Typography variant="body2" paragraph sx={{ mt: 2 }}>
                  Each pattern defines the voltage levels and timing for the ultrasound transmission.
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Tab: Configuration */}
        <TabPanel value={currentTab} index={2}>
          <ConfigManager />
        </TabPanel>

        {/* Tab: Diagnostics */}
        <TabPanel value={currentTab} index={3}>
          <DiagnosticsPanel />
        </TabPanel>

        {/* Device Not Connected Warning */}
        {deviceStatus && !deviceStatus.connected && (
          <Box mt={2}>
            <Paper elevation={2} sx={{ p: 2, bgcolor: 'warning.light' }}>
              <Typography variant="body1" fontWeight="bold">
                ⚠️ Device Not Connected
              </Typography>
              <Typography variant="body2">
                Please connect to the TX7332 device to use the control features.
              </Typography>
            </Paper>
          </Box>
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
