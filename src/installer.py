import os
import subprocess


def run_setup(cfg, relpath, log):
    base = cfg.get("base_dir") or r"C:\UtilitiesIT"
    exe = os.path.join(base, relpath)
    if not os.path.isfile(exe):
        log(f"ERROR: no se encontró {exe}")
        log("Presiona 'Actualizar archivos' primero para descargar e instalar los archivos.")
        return 1
    log(f"Ejecutando: {exe}")
    return run_process([exe], os.path.dirname(exe), log)


def run_process(cmd, cwd, log):
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
    except FileNotFoundError:
        log(f"ERROR: no se pudo iniciar: {cmd[0]}")
        return 1
    except OSError as e:
        log(f"ERROR: no se pudo iniciar: {e}")
        return 1

    for line in iter(proc.stdout.readline, ""):
        if line.strip():
            log(line.rstrip())
    proc.stdout.close()
    code = proc.wait()
    log(f"Código de salida: {code}")
    return code
