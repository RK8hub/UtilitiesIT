import os
import subprocess
import tempfile
import time
import zipfile


def download_and_extract(cfg, log):
    url = (cfg.get("zip_url") or "").strip()
    if not url:
        log("ERROR: 'zip_url' está vacío en config.json")
        return 1

    base = cfg.get("base_dir") or r"C:\UtilitiesIT"
    os.makedirs(base, exist_ok=True)

    sep = "&" if "?" in url else "?"
    full = f"{url}{sep}v={int(time.time())}"
    log(f"Descargando: {url}")

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
            tmp_path = tmp.name
        proc = subprocess.run(
            ["curl", "-L", "-sS", "-o", tmp_path, full],
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or "curl falló")
        size = os.path.getsize(tmp_path)
        log(f"Descargado: {size:,} bytes")

        with zipfile.ZipFile(tmp_path) as zf:
            names = zf.namelist()
            log(f"Extrayendo {len(names)} archivos a {base}...")
            zf.extractall(base)
        log("Extracción completada.")
        return 0
    except FileNotFoundError:
        log("ERROR: no se encontró 'curl'. Se requiere en Windows 10/11.")
        return 1
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
