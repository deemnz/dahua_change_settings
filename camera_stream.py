# dahua_api/camera_stream.py

from .camera_common import dahua_get, dahua_set

def get_stream_config(ip, user, pwd, channel=0, stream_type='MainFormat', index=0):
    """
    GET: Encode[channel].MainFormat[0] или ExtraFormat
    Пример: "cgi-bin/configManager.cgi?action=getConfig&name=Encode[0].MainFormat[0]"
    """
    cgi = f"cgi-bin/configManager.cgi?action=getConfig&name=Encode[{channel}].{stream_type}[{index}]"
    return dahua_get(ip, user, pwd, cgi)

def set_stream_all(
    ip, user, pwd,
    channel=0, stream_type='MainFormat', index=0,

    # --- Audio ---
    audio_enable=False,
    audio_bitrate=64,
    audio_compression="G.711A",
    audio_depth=16,
    audio_frequency=44000,
    audio_mode=0,
    audio_pack="DHAV",

    # --- Video ---
    video_enable=True,
    resolution="2560x1440",
    width=2560,
    height=1440,
    compression="H.265",
    bit_rate=6144,
    bit_rate_control="VBR",
    fps=25,
    gop=50,
    priority=0,
    profile="Main",
    quality=5,
    quality_range=6,
    svct_layer=1,
    space_svc_layer=1,
    time_svc_layer=1,
    pack="DHAV",
    custom_res_name="2560x1440"
):
    """
    Устанавливаем **все** перечисленные параметры для Encode[channel].{stream_type}[index]:
      AudioEnable=...
      Audio.(Bitrate,Compression,Depth,Frequency,Mode,Pack)
      VideoEnable=...
      Video.(resolution,Width,Height,BitRate,BitRateControl,Compression,FPS,GOP,Priority,Profile,Quality,QualityRange,SVCTLayer,etc.)
    """

    base = "cgi-bin/configManager.cgi?action=setConfig"

    # Префиксы
    prefix_audio = f"Encode[{channel}].{stream_type}[{index}].Audio"
    prefix_video = f"Encode[{channel}].{stream_type}[{index}].Video"

    # В Dahua часто AudioEnable идёт не внутри "Audio.", а на уровень выше:
    # Encode[0].MainFormat[0].AudioEnable=false
    # Или бывает Encode[0].MainFormat[0].Audio.Enable=true
    # Ниже — вариант, когда AudioEnable=... на том же уровне, что VideoEnable=...
    audio_en_val = "true" if audio_enable else "false"
    video_en_val = "true" if video_enable else "false"

    # Формируем строку с параметрами
    cgi_params = []
    
    # --- AudioEnable ---
    cgi_params.append(f"Encode[{channel}].{stream_type}[{index}].AudioEnable={audio_en_val}")
    # --- Audio.* ---
    cgi_params.append(f"{prefix_audio}.Bitrate={audio_bitrate}")
    cgi_params.append(f"{prefix_audio}.Compression={audio_compression}")
    cgi_params.append(f"{prefix_audio}.Depth={audio_depth}")
    cgi_params.append(f"{prefix_audio}.Frequency={audio_frequency}")
    cgi_params.append(f"{prefix_audio}.Mode={audio_mode}")
    cgi_params.append(f"{prefix_audio}.Pack={audio_pack}")

    # --- VideoEnable ---
    cgi_params.append(f"Encode[{channel}].{stream_type}[{index}].VideoEnable={video_en_val}")
    # --- Video.* ---
    cgi_params.append(f"{prefix_video}.resolution={resolution}")  # иногда нужно Video.Resolution (с большой буквы). См. прошивку
    cgi_params.append(f"{prefix_video}.Width={width}")
    cgi_params.append(f"{prefix_video}.Height={height}")
    cgi_params.append(f"{prefix_video}.BitRate={bit_rate}")
    cgi_params.append(f"{prefix_video}.BitRateControl={bit_rate_control}")
    cgi_params.append(f"{prefix_video}.Compression={compression}")
    cgi_params.append(f"{prefix_video}.FPS={fps}")
    cgi_params.append(f"{prefix_video}.GOP={gop}")
    cgi_params.append(f"{prefix_video}.Priority={priority}")
    cgi_params.append(f"{prefix_video}.Profile={profile}")
    cgi_params.append(f"{prefix_video}.Quality={quality}")
    cgi_params.append(f"{prefix_video}.QualityRange={quality_range}")
    cgi_params.append(f"{prefix_video}.SVCTLayer={svct_layer}")
    cgi_params.append(f"{prefix_video}.SvacSVCLayer.SpaceDomainSVCLayer={space_svc_layer}")
    cgi_params.append(f"{prefix_video}.SvacSVCLayer.TimeDomainSVCLayer={time_svc_layer}")
    cgi_params.append(f"{prefix_video}.Pack={pack}")
    cgi_params.append(f"{prefix_video}.CustomResolutionName={custom_res_name}")

    # Склеиваем
    param_str = '&'.join(cgi_params)
    full_cgi = f"{base}&{param_str}"

    return dahua_set(ip, user, pwd, full_cgi)
