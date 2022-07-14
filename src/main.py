import secrets_config
from app.libs.ota_updater import OTAUpdater
from app.start import main


def download_and_install_update_if_available():
    o = OTAUpdater('https://github.com/datalexum/Smart-ATO-Micropython', main_dir='app', github_src_dir='src/app')
    o.install_update_if_available_after_boot(secrets_config.WIFI_SSID, secrets_config.WIFI_PASSWORD)


def start():
    main()


def boot_showerloop():
    download_and_install_update_if_available()


s = None
boot_showerloop()
