import shutil

from .installer import run_process


def run_command(cfg, log):
    cmd = (cfg.get("powershell_command") or "").strip()
    if not cmd:
        log("ERROR: 'powershell_command' está vacío en config.json")
        return 1
    if shutil.which("powershell.exe") is None:
        log("ERROR: no se encontró powershell.exe (este paso corre en Windows).")
        return 1
    log(f"Comando: {cmd}")
    return run_process(
        ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
        None,
        log,
    )
