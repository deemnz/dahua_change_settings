# dahua_api/camera_audio.py

from .camera_common import dahua_get, dahua_set

def get_audio_config(ip, user, pwd, channel=0, timeout=5):
    """
    Допустим, у нас AudioEncode[0].MainFormat[0] — базовый вариант.
    Или смотрим, что реально возвращает GET.
    """
    cgi = f"cgi-bin/configManager.cgi?action=getConfig&name=AudioEncode[{channel}].MainFormat[0]"
    return dahua_get(ip, user, pwd, cgi, timeout=timeout)

def set_audio_config(ip, user, pwd, channel=0,
                     enable=True,
                     compression="G.711A",
                     bitrate=64,
                     timeout=5):
    """
    Пример настройки аудио:
      AudioEncode[0].MainFormat[0].Audio.Enable=true/false
      AudioEncode[0].MainFormat[0].Audio.Compression=G.711A
      AudioEncode[0].MainFormat[0].Audio.Bitrate=64
    """
    base = "cgi-bin/configManager.cgi?action=setConfig"
    en_val = "true" if enable else "false"
    cgi = (
        f"{base}"
        f"&AudioEncode[{channel}].MainFormat[0].Audio.Enable={en_val}"
        f"&AudioEncode[{channel}].MainFormat[0].Audio.Compression={compression}"
        f"&AudioEncode[{channel}].MainFormat[0].Audio.Bitrate={bitrate}"
    )
    return dahua_set(ip, user, pwd, cgi, timeout=timeout)
