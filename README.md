# Vinna

Utilidades internas de IT — app de escritorio (Python + Flet).

- **Impresoras**: descarga y ejecuta el instalador del driver (`impresora\Setup.exe`).
- **Office**: ejecuta el instalador de Office (`office\OfficeSetup.exe`).
- **PowerShell**: ejecuta un único comando definido en `config.json` como Administrador.

Los archivos (drivers + Office) se descargan de un zip alojado en Cloudflare R2 y se
extraen a `C:\UtilitiesIT` (por defecto). Re-ejecutar "Actualizar archivos" trae la
última versión.

## Requisitos (Windows)

- Python 3.10+ con pip.
- `curl.exe` incluido en Windows 10/11 (usado para la descarga).

## Instalación / desarrollo

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
flet run app.py
```

## Compilar el .exe (Windows)

```powershell
powershell -ExecutionPolicy Bypass -File build\build.ps1
```

Genera `dist\Vinna.exe` con UAC activado (`--uac-admin`). El icono usa `assets\icon.ico`.

Para sobreescribir la configuración sin recompilar, copie `config.json` junto al exe.

## Configuración (`config.json`)

| Clave | Descripción |
|---|---|
| `zip_url` | URL pública del zip en R2 (`https://pub-...r2.dev/utilities.zip`) |
| `base_dir` | Carpeta local donde se extrae y se ejecutan los setups |
| `setup_impresora` | Ruta relativa del instalador de impresora dentro del zip |
| `setup_office` | Ruta relativa del instalador de Office dentro del zip |
| `powershell_command` | Único comando PowerShell que se permite ejecutar |

## Estructura del zip en R2

```
utilities.zip
├── impresora/          ← Setup.exe y drivers de la impresora
└── office/             ← OfficeSetup.exe
```
