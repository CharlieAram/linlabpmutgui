/**
 * Diagnostics Panel Component
 * Display device diagnostic information
 */
import { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  Snackbar,
  CircularProgress,
} from '@mui/material';
import { PlayArrow, CheckCircle, Error } from '@mui/icons-material';
import { deviceApi } from '../../services/api';
import type { DiagnosticsResponse } from '../../types';

export default function DiagnosticsPanel() {
  const [diagnostics, setDiagnostics] = useState<DiagnosticsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRunDiagnostics = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await deviceApi.runDiagnostics();
      setDiagnostics(result);
    } catch (err: any) {
      setError(err.message || 'Failed to run diagnostics');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={2} sx={{ p: 2, mb: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Device Diagnostics</Typography>
        <Button
          variant="contained"
          startIcon={loading ? <CircularProgress size={16} /> : <PlayArrow />}
          onClick={handleRunDiagnostics}
          disabled={loading}
        >
          Run Diagnostics
        </Button>
      </Box>

      {diagnostics && (
        <>
          <Box mb={2}>
            <Chip
              icon={diagnostics.overall_status === 'PASS' ? <CheckCircle /> : <Error />}
              label={`Overall Status: ${diagnostics.overall_status}`}
              color={diagnostics.overall_status === 'PASS' ? 'success' : 'error'}
            />
            <Typography variant="caption" color="text.secondary" ml={2}>
              {diagnostics.error_count} error(s) found
            </Typography>
          </Box>

          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>Check</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Message</TableCell>
                  <TableCell>Value</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {diagnostics.checks.map((check, index) => (
                  <TableRow key={index}>
                    <TableCell>
                      <Typography variant="body2" fontWeight="medium">
                        {check.check_name}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      {check.passed ? (
                        <Chip label="PASS" color="success" size="small" />
                      ) : (
                        <Chip label="FAIL" color="error" size="small" />
                      )}
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">{check.message}</Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2" color="text.secondary">
                        {check.value || 'N/A'}
                      </Typography>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          <Typography variant="caption" color="text.secondary" display="block" mt={2}>
            Last run: {new Date(diagnostics.timestamp).toLocaleString()}
          </Typography>
        </>
      )}

      {!diagnostics && !loading && (
        <Alert severity="info">
          Click "Run Diagnostics" to check device status
        </Alert>
      )}

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

