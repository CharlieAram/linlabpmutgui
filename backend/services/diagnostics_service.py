"""Device diagnostics service."""
from typing import List, Tuple
from backend.device.controller import TX7332Controller


class DiagnosticsService:
    """Service for running device diagnostics."""
    
    def __init__(self, controller: TX7332Controller):
        self.controller = controller
    
    def run_diagnostics(self) -> Tuple[str, List[dict]]:
        """
        Run comprehensive diagnostics on the device.
        Based on existing boardDiagnostics_TX7364 function.
        
        Returns:
            Tuple of (overall_status, list of check results)
        """
        self.controller.ensure_connected()
        
        checks = []
        all_passed = True
        
        try:
            # Read diagnostic registers (using TX7364 registers as reference)
            reg1D = self.controller.read_reg(0x1D)
            reg4D = self.controller.read_reg(0x4D)
            reg4E = self.controller.read_reg(0x4E)
            reg62 = self.controller.read_reg(0x62)
            reg6C = self.controller.read_reg(0x6C)
            reg78 = self.controller.read_reg(0x78)
            
            # Convert to binary strings
            reg1D_bin = format(reg1D, '032b')
            reg4D_bin = format(reg4D, '032b')
            reg4E_bin = format(reg4E, '032b')
            reg62_bin = format(reg62, '032b')
            reg6C_bin = format(reg6C, '032b')
            reg78_bin = format(reg78, '032b')
            
            # Define checks (based on existing code)
            diagnostic_checks = [
                (int(reg4D_bin[-6:], 2) == 0, "TEMP_SHUT_ERR[11:6]", reg4D_bin[-6:]),
                (int(reg62_bin[-6:], 2) == 0, "TEMP_SHUT_ERR[5:0]", reg62_bin[-6:]),
                (reg6C_bin[15] == '1', "NO_CLK_ERR", reg6C_bin[15]),
                (reg1D_bin[31] == '0', "SINGLE_LVL_ERR", reg1D_bin[31]),
                (reg1D_bin[29] == '0', "LONG_TRAN_ERR", reg1D_bin[29]),
                (reg4E_bin[27] == '0', "P5V_SUP_ERR", reg4E_bin[27]),
                (reg4E_bin[26] == '0', "M5V_SUP_ERR", reg4E_bin[26]),
                (reg4E_bin[16] == '0', "PHV_RANGE_ERR", reg4E_bin[16]),
                (reg78_bin[29] == '0', "TRIG_ERR", reg78_bin[29]),
                (reg78_bin[31] == '0', "STANDBY_ERR", reg78_bin[31]),
                (int(reg4D_bin[:5], 2) == 21, "VALID_FLAG_1", str(int(reg4D_bin[:5], 2))),
                (int(reg4E_bin[:5], 2) == 10, "VALID_FLAG_2", str(int(reg4E_bin[:5], 2))),
                (int(reg62_bin[:5], 2) == 11, "VALID_FLAG_3", str(int(reg62_bin[:5], 2))),
                (int(reg6C_bin[:5], 2) == 22, "VALID_FLAG_4", str(int(reg6C_bin[:5], 2))),
                (int(reg78_bin[:5], 2) == 25, "VALID_FLAG_5", str(int(reg78_bin[:5], 2))),
                (reg4D_bin[15] == '0', "ERROR_RST", reg4D_bin[15])
            ]
            
            for passed, check_name, value in diagnostic_checks:
                status_msg = f"{check_name}: {'PASSED' if passed else 'FAILED'}"
                checks.append({
                    "check_name": check_name,
                    "passed": passed,
                    "message": status_msg,
                    "value": value
                })
                if not passed:
                    all_passed = False
            
            # If diagnostics failed, attempt to reset error flags
            if not all_passed:
                try:
                    # Check for NO_CLK_ERR
                    if reg6C_bin[15] != '1':
                        self.controller.write_reg(0x08, 0x00000002)
                    
                    # Reset error flags
                    self.controller.write_reg(0x4D, 1 << 16)  # Set ERROR_RST
                    import time
                    time.sleep(1)
                    self.controller.write_reg(0x4D, 0)  # Clear ERROR_RST
                    
                    checks.append({
                        "check_name": "ERROR_RESET",
                        "passed": True,
                        "message": "Error flags reset attempted",
                        "value": None
                    })
                except Exception as e:
                    checks.append({
                        "check_name": "ERROR_RESET",
                        "passed": False,
                        "message": f"Failed to reset error flags: {e}",
                        "value": None
                    })
            
            overall_status = "PASS" if all_passed else "FAIL"
            
        except Exception as e:
            checks.append({
                "check_name": "DIAGNOSTICS",
                "passed": False,
                "message": f"Diagnostic error: {str(e)}",
                "value": None
            })
            overall_status = "FAIL"
        
        return overall_status, checks

