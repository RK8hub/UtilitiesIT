$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

Write-Host "== Vinna - Build (Windows) =="

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

$iconArgs = @()
if (Test-Path "assets\icon.ico") {
    $iconArgs = @("--icon", "assets\icon.ico")
} else {
    Write-Host "ADVERTENCIA: no existe assets\icon.ico, se usara el icono por defecto de Flet."
}

flet pack app.py `
    --name Vinna `
    --uac-admin `
    --add-data "config.json:." `
    --add-data "assets\window_icon.ico:assets" `
    --product-name Vinna `
    --file-description "Utilidades internas IT" `
    --company-name "IT" `
    --product-version "1.0.0" `
    --file-version "1.0.0.0" `
    @iconArgs

Write-Host ""
Write-Host "Listo: dist\Vinna.exe"
Write-Host "Config editable junto al exe: copie config.json junto a dist\Vinna.exe para sobrescribir la empaquetada."
