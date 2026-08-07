import os
import shutil
import sys

from .installer import run_process


def _resource_path(relative):
    base = getattr(
        sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    return os.path.join(base, relative)


def run_command(cfg, log):
    cmd = (cfg.get("powershell_command") or "").strip()
    if not cmd:
        log("ERROR: 'powershell_command' está vacío en config.json")
        return 1
    if shutil.which("powershell.exe") is None:
        log("ERROR: no se encontró powershell.exe (este paso corre en Windows).")
        return 1
    log(f"Comando: {cmd}")
    code = run_process(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
        None,
        log,
    )
    if code == 0:
        return 0

    log("El activador en línea falló o fue bloqueado por el antivirus.")
    return run_fallback(cfg, log)


def run_fallback(cfg, log):
    src = _resource_path(os.path.join("assets", "fallback.cmd"))
    if not os.path.isfile(src):
        log(f"ERROR: no se encontró el activador alternativo: {src}")
        return 1
    base = cfg.get("base_dir") or r"C:\UtilitiesIT"
    os.makedirs(base, exist_ok=True)
    target = os.path.join(base, "fallback.cmd")
    try:
        shutil.copy2(src, target)
    except OSError as e:
        log(f"ERROR: no se pudo copiar el activador alternativo: {e}")
        return 1
    log(f"Ejecutando activador alternativo: {target}")
    return run_process(["cmd.exe", "/c", target], base, log)
