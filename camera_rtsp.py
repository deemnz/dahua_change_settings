# dahua_api/camera_rtsp.py

from .camera_common import dahua_get, dahua_set

def get_rtsp_config(ip, user, pwd):
    """
    Пример: cgi-bin/configManager.cgi?action=getConfig&name=RTSP
    """
    cgi = "cgi-bin/configManager.cgi?action=getConfig&name=RTSP"
    return dahua_get(ip, user, pwd, cgi)

def set_rtsp_config(ip, user, pwd, rtsp_port=554, rtsp_auth="digest"):
    """
    Пример:
      RTSP.ProtoPort=554
      RTSP.AuthType=digest (или basic, disable)
    """
    base = "cgi-bin/configManager.cgi?action=setConfig"
    cgi = (
        f"{base}"
        f"&RTSP.ProtoPort={rtsp_port}"
        f"&RTSP.AuthType={rtsp_auth}"
    )
    return dahua_set(ip, user, pwd, cgi)
