import machine
import secrets_config
from app.libs.ota_updater import OTAUpdater
from app.start import main

p = machine.Pin(2, machine.Pin.OUT)

def download_and_install_update_if_available():
    p.on()
    o = OTAUpdater(
        "https://github.com/datalexum/Smart-ATO-Micropython",
        main_dir="app",
        github_src_dir="src",
    )
    updated = o.install_update_if_available_after_boot(
        secrets_config.WIFI_SSID, secrets_config.WIFI_PASSWORD
    )
    p.off()
    if updated:
        machine.reset()


download_and_install_update_if_available()
main()