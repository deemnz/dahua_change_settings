# dahua_api/camera_ntp.py

from .camera_common import dahua_get, dahua_set

def get_ntp_config(ip, user, pwd):
    """
    cgi-bin/configManager.cgi?action=getConfig&name=NTP
    """
    cgi = "cgi-bin/configManager.cgi?action=getConfig&name=NTP"
    return dahua_get(ip, user, pwd, cgi)

def set_ntp_config(ip, user, pwd,
                   enable=True,
                   server='pool.ntp.org',
                   port=123,
                   interval=60,
                   timezone='GMT+03:00-Moscow'):
    """
    NTP.Enable=true/false
    NTP.Address=...
    NTP.Port=...
    NTP.Interval=...
    NTP.TimeZone=...
    """
    en_val = 'true' if enable else 'false'
    base = "cgi-bin/configManager.cgi?action=setConfig"
    cgi = (
        f"{base}"
        f"&NTP.Enable={en_val}"
        f"&NTP.Address={server}"
        f"&NTP.Port={port}"
        f"&NTP.Interval={interval}"
        f"&NTP.TimeZone={timezone}"
    )
    return dahua_set(ip, user, pwd, cgi)
