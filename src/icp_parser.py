import json
import yaml
from pathlib import Path

class ICPParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_icp(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"❌ Config file not found: {self.file_path}")
        if self.file_path.suffix in [".yaml", ".yml"]:
            with open(self.file_path, "r") as f:
                data = yaml.safe_load(f)
        elif self.file_path.suffix == ".json":
            with open(self.file_path, "r") as f:
                data = json.load(f)
        else:
            raise ValueError("❌ Unsupported file format. Use YAML or JSON.")
        self.validate_icp(data)
        return data

    def validate_icp(self, data: dict):
        required_keys = [
            "revenue_min", "revenue_max", "industry",
            "geography", "employee_count_min", "keywords", "signals"
        ]
        for key in required_keys:
            if key not in data:
                raise KeyError(f"⚠️ Missing required key: {key}")
