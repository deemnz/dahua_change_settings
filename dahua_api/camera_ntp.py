# dahua_api/camera_ntp.py

from .camera_common import dahua_get, dahua_set

def get_ntp_config(ip, user, pwd, timeout=5):
    """
    GET NTP
    cgi-bin/configManager.cgi?action=getConfig&name=NTP
    """
    cgi = "cgi-bin/configManager.cgi?action=getConfig&name=NTP"
    return dahua_get(ip, user, pwd, cgi, timeout=timeout)

def set_ntp_config(ip, user, pwd,
                   enable=True,
                   server="pool.ntp.org",
                   port=123,
                   interval=60,
                   timezone="GMT+03:00-Moscow",
                   timeout=5):
    """
    Пример установки NTP:
      NTP.Enable=true
      NTP.Address=pool.ntp.org
      NTP.Port=123
      NTP.Interval=60
      NTP.TimeZone=...
    """
    base = "cgi-bin/configManager.cgi?action=setConfig"
    en_val = "true" if enable else "false"
    cgi = (
        f"{base}"
        f"&NTP.Enable={en_val}"
        f"&NTP.Address={server}"
        f"&NTP.Port={port}"
        f"&NTP.Interval={interval}"
        f"&NTP.TimeZone={timezone}"
    )
    return dahua_set(ip, user, pwd, cgi, timeout=timeout)
