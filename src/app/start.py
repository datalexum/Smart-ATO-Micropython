from libs.ota_updater import OTAUpdater
from ..secrets_config import WIFI_PASSWORD, WIFI_SSID

def main():
    o = OTAUpdater('https://github.com/datalexum/Smart-ATO-Micropython', main_dir='src/app')
    OTAUpdater._using_network(WIFI_SSID, WIFI_PASSWORD)
    o.check_for_update_to_install_during_next_reboot()
    print("In start.py - 1")
