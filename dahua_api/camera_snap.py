# dahua_api/camera_snap.py

from .camera_common import dahua_get, dahua_set

def get_snap_config(ip, user, pwd, channel=0):
    """
    cgi-bin/configManager.cgi?action=getConfig&name=Snap[0]
    """
    cgi = f"cgi-bin/configManager.cgi?action=getConfig&name=Snap[{channel}]"
    return dahua_get(ip, user, pwd, cgi)

def set_snap_config(ip, user, pwd, channel=0, enable=True, interval=60):
    """
    Пример: Snap[0].Enable=..., Snap[0].TimingEnable=..., Snap[0].TimingInterval=60
    """
    en_val = 'true' if enable else 'false'
    base = "cgi-bin/configManager.cgi?action=setConfig"
    cgi = (
        f"{base}"
        f"&Snap[{channel}].Enable={en_val}"
        f"&Snap[{channel}].TimingEnable={en_val}"
        f"&Snap[{channel}].TimingInterval={interval}"
    )
    return dahua_set(ip, user, pwd, cgi)
