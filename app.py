import flet as ft

from src import config as cfgmod
from src import download
from src import installer
from src import powershell


def main(page: ft.Page):
    cfg = cfgmod.load()

    page.title = "Vinna"
    page.width = 840
    page.height = 620
    page.padding = 12
    page.theme_mode = ft.ThemeMode.LIGHT

    log_view = ft.ListView(expand=True, auto_scroll=True, spacing=2)
    status = ft.Text("Listo.", size=12)
    progress = ft.ProgressBar(visible=False)

    download_btn = ft.FilledButton("Actualizar archivos", icon=ft.Icons.DOWNLOAD)
    printer_btn = ft.FilledButton("Instalar driver de impresora", icon=ft.Icons.PRINT)
    office_btn = ft.FilledButton("Instalar Office", icon=ft.Icons.DESKTOP_WINDOWS)
    ps_btn = ft.FilledButton("Ejecutar comando PowerShell", icon=ft.Icons.TERMINAL)

    all_buttons = [download_btn, printer_btn, office_btn, ps_btn]

    def log(msg: str):
        log_view.controls.append(ft.Text(msg, size=12))
        status.value = msg
        page.update()

    def set_busy(busy: bool):
        progress.visible = busy
        for b in all_buttons:
            b.disabled = busy
        page.update()

    def worker(label, fn):
        try:
            fn()
        except Exception as e:
            log(f"ERROR: {e}")
        finally:
            set_busy(False)
            log(f"--- {label} terminado ---")

    def run_job(label, fn):
        log(f"--- {label} ---")
        set_busy(True)
        page.run_thread(worker, label, fn)

    def on_update(e):
        run_job("Actualizar archivos", lambda: download.download_and_extract(cfg, log))

    def on_printer(e):
        run_job(
            "Instalar driver de impresora",
            lambda: installer.run_setup(cfg, cfg["setup_impresora"], log),
        )

    def on_office(e):
        run_job(
            "Instalar Office",
            lambda: installer.run_setup(cfg, cfg["setup_office"], log),
        )

    def on_powershell(e):
        run_job("PowerShell", lambda: powershell.run_command(cfg, log))

    download_btn.on_click = on_update
    printer_btn.on_click = on_printer
    office_btn.on_click = on_office
    ps_btn.on_click = on_powershell

    printer_tab = ft.Column(
        [
            printer_btn,
            ft.Text(
                f"Ejecuta el instalador del driver descargado.\n"
                f"Ruta: {cfg['base_dir']}\\{cfg['setup_impresora']}",
                size=12,
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    office_tab = ft.Column(
        [
            office_btn,
            ft.Text(
                f"Ejecuta el instalador de Office descargado.\n"
                f"Ruta: {cfg['base_dir']}\\{cfg['setup_office']}",
                size=12,
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    ps_tab = ft.Column(
        [
            ps_btn,
            ft.TextField(
                label="Comando único (desde config.json)",
                value=cfg.get("powershell_command", ""),
                read_only=True,
                multiline=True,
                min_lines=1,
                max_lines=3,
            ),
            ft.Text(
                "Se ejecuta como Administrador en PowerShell.\n"
                "Para cambiarlo, edita powershell_command en config.json.",
                size=12,
            ),
        ],
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
    )

    tabs = ft.Tabs(
        expand=True,
        tabs=[
            ft.Tab(text="Impresoras", content=printer_tab),
            ft.Tab(text="Office", content=office_tab),
            ft.Tab(text="PowerShell", content=ps_tab),
        ],
    )

    page.add(
        ft.Row([download_btn], alignment=ft.MainAxisAlignment.START),
        progress,
        tabs,
        ft.Divider(),
        ft.Row(
            [
                ft.Text("Bitácora", weight=ft.FontWeight.BOLD, size=13),
                ft.Container(expand=True),
                status,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        ft.Container(
            content=log_view,
            expand=True,
            border=ft.Border(
                top=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                right=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                bottom=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                left=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            ),
            border_radius=8,
            padding=8,
        ),
    )


if __name__ == "__main__":
    ft.app(main)
