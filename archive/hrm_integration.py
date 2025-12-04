import sys
from pathlib import Path

# Add HRM to path
HRM_PATH = Path(__file__).parent.parent / "lib" / "hrm"
sys.path.insert(0, str(HRM_PATH))

# Now import HRM modules
import torch


class HRMOrchestrator:
    def __init__(self):
        # Auto-detect M4 Max MPS support
        self.device = torch.device(
            "mps" if torch.backends.mps.is_available() else "cpu"
        )
        print(f"HRM running on: {self.device}")

        # Load HRM models from local path
        self.model_path = HRM_PATH / "checkpoints"
        self.initialize_hrm()

    def initialize_hrm(self):
        """Initialize HRM with local models"""
        # Your HRM initialization code
        pass
