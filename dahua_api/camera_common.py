# dahua_api/camera_common.py

import requests
from requests.auth import HTTPDigestAuth

def dahua_get(ip, user, pwd, cgi_path, timeout=5):
    url = f"http://{ip}/{cgi_path}"
    try:
        r = requests.get(url, auth=HTTPDigestAuth(user, pwd), timeout=timeout)
        return r
    except Exception as e:
        return e

def dahua_set(ip, user, pwd, cgi_path, timeout=5):
    url = f"http://{ip}/{cgi_path}"
    try:
        r = requests.get(url, auth=HTTPDigestAuth(user, pwd), timeout=timeout)
        return r
    except Exception as e:
        return e

def set_single_param(ip, user, pwd, param: str, timeout=5):
    """
    Отправляет РОВНО ОДИН параметр в Dahua через setConfig.
    Пример param: "Encode[0].ExtraFormat[0].Video.BitRateControl=VBR"
    Итоговый URL: cgi-bin/configManager.cgi?action=setConfig&Encode[0].ExtraFormat[0].Video.BitRateControl=VBR
    """
    base = "cgi-bin/configManager.cgi?action=setConfig"
    cgi = f"{base}&{param}"
    return dahua_set(ip, user, pwd, cgi, timeout=timeout)
