from __future__ import annotations
from pathlib import Path
import sys
import json 
from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    test: int

def load_config(config_filename: str) -> AppConfig:
    config_path = resource_path(config_filename)
    with config_path.open(encoding="utf-8") as f:
        c = json.load(f)

    return AppConfig(
        test=1
    )

def resource_path(relative: str) -> Path:
    """
    Return an absolute path to a bundled resource (works in dev + PyInstaller onefile).
    """
    if hasattr(sys, "_MEIPASS"):  # PyInstaller extracts here at runtime
        return Path(sys._MEIPASS) / relative  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent / relative
