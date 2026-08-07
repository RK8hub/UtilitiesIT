import json
import os
import sys

DEFAULT_CONFIG = {
    "zip_url": "",
    "base_dir": r"C:\UtilitiesIT",
    "setup_impresora": r"impresora\Setup.exe",
    "setup_office": r"office\OfficeSetup.exe",
    "powershell_command": "",
}


def config_path():
    if getattr(sys, "frozen", False):
        exe_dir = os.path.dirname(sys.executable)
        external = os.path.join(exe_dir, "config.json")
        if os.path.exists(external):
            return external
        bundled = os.path.join(getattr(sys, "_MEIPASS", exe_dir), "config.json")
        return bundled
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")


def load():
    cfg = dict(DEFAULT_CONFIG)
    path = config_path()
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                cfg.update(data)
        except (OSError, ValueError) as e:
            raise RuntimeError(f"No se pudo leer {path}: {e}")
    return cfg
