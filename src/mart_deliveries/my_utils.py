from __future__ import annotations
from pathlib import Path
import sys
import json 
from dataclasses import dataclass

@dataclass(frozen=True)
class AppConfig:
    delivery_excel: Path
    excel_suffixes: set[str]
    supported_filetypes: list[tuple[str, str]]
    delivery_start_dir: Path


def load_config(config_filename: str) -> AppConfig:
    config_path = resource_path(config_filename)
    with config_path.open(encoding="utf-8") as f:
        c = json.load(f)

    return AppConfig(
        delivery_excel=Path(c.get("DELIVERY", "Desktop")),
        excel_suffixes=set(c.get("excel_suffixes", [])),
        supported_filetypes=[(a, b) for a, b in c.get("supported_filetypes", [])],
        delivery_start_dir=Path(c.get("delivery_start_dir", "Desktop"))
    ) 

def resource_path(relative: str) -> Path:
    """
    Return an absolute path to a bundled resource (works in dev + PyInstaller onefile).
    """
    if hasattr(sys, "_MEIPASS"):  # PyInstaller extracts here at runtime
        return Path(sys._MEIPASS) / relative  # type: ignore[attr-defined]
    return Path(__file__).resolve().parent / relative
