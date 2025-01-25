import argparse
import sys

from utils.ip_utils import get_ip_list
from utils.messages import MESSAGES

# Импортируем Dahua API модули
from dahua_api.camera_common import set_single_param
from dahua_api.camera_stream import get_stream_config
from dahua_api.camera_ntp import get_ntp_config, set_ntp_config
from dahua_api.camera_rtsp import get_rtsp_config, set_rtsp_config
from dahua_api.camera_audio import get_audio_config, set_audio_config


def parse_args():
    parser = argparse.ArgumentParser(description="Dahua Change Settings (Stream, NTP, RTSP, Audio)")

    parser.add_argument("--lang", default="ru", help="Language: ru/en")
    parser.add_argument("--ip", required=True,
                        help="Camera IP, range ip:port-ip:port, or file")

    parser.add_argument("--user", required=True, help="Camera login")
    parser.add_argument("--pwd", required=True, help="Camera password")

    # --- Stream (Video) ---
    parser.add_argument("--get_stream", action="store_true", help="GET stream config")
    parser.add_argument("--set_stream", action="store_true", help="SET stream config")

    parser.add_argument("--channel", type=int, default=0,
                        help="Encode[..] channel index (default 0)")
    parser.add_argument("--stream_type", type=str, default="MainFormat",
                        help="MainFormat / ExtraFormat / etc.")
    parser.add_argument("--stream_index", type=int, default=0,
                        help="Index of the stream (usually 0)")

    parser.add_argument("--compression", action="store_true",
                        help="Video.Compression (for GET filtering or used with --compression_value)")
    parser.add_argument("--compression_value", type=str,
                        help="Set compression (H.264/H.265)")
    parser.add_argument("--bit_rate", action="store_true",
                        help="Video.BitRate (for GET filter or used with --bit_rate_value)")
    parser.add_argument("--bit_rate_value", type=int,
                        help="Set BitRate in Kbps")
    parser.add_argument("--bit_rate_control", action="store_true",
                        help="Video.BitRateControl (CBR/VBR)")
    parser.add_argument("--bit_rate_control_value", type=str,
                        help="Set Video.BitRateControl")
    parser.add_argument("--resolution", action="store_true",
                        help="Video.resolution (for GET filter or used with --resolution_value)")
    parser.add_argument("--resolution_value", type=str,
                        help="Set Video.resolution")
    parser.add_argument("--fps", action="store_true",
                        help="Video.FPS (filter or used with --fps_value)")
    parser.add_argument("--fps_value", type=int,
                        help="Set Video.FPS")

    # --- NTP ---
    parser.add_argument("--get_ntp", action="store_true",
                        help="GET NTP config")
    parser.add_argument("--set_ntp", action="store_true",
                        help="SET NTP config")
    parser.add_argument("--enable_ntp", action="store_true",
                        help="NTP.Enable=true (otherwise false)")
    parser.add_argument("--ntp_server", type=str, default="pool.ntp.org",
                        help="NTP server address")
    parser.add_argument("--ntp_port", type=int, default=123,
                        help="NTP port")
    parser.add_argument("--ntp_interval", type=int, default=60,
                        help="NTP sync interval (minutes)")
    parser.add_argument("--ntp_timezone", type=str, default="GMT+03:00-Moscow",
                        help="NTP TimeZone")

    # --- RTSP ---
    parser.add_argument("--get_rtsp", action="store_true",
                        help="GET RTSP config")
    parser.add_argument("--set_rtsp", action="store_true",
                        help="SET RTSP config")
    parser.add_argument("--rtsp_port", type=int, default=554,
                        help="RTSP port")
    parser.add_argument("--rtsp_auth", type=str, default="digest",
                        help="RTSP AuthType: digest/basic/disable")

    # --- Audio ---
    parser.add_argument("--get_audio", action="store_true",
                        help="GET audio config")
    parser.add_argument("--set_audio", action="store_true",
                        help="SET audio config (enable/disable, compression, bitrate)")
    parser.add_argument("--audio_channel", type=int, default=0,
                        help="AudioEncode[..] channel index (default 0)")
    parser.add_argument("--audio_enable", action="store_true",
                        help="Audio.Enable=true (otherwise disable)")
    parser.add_argument("--audio_disable", action="store_true",
                        help="Audio.Enable=false")
    parser.add_argument("--audio_compression", type=str, default="G.711A",
                        help="Audio compression (G.711A / G.711U / AAC, etc.)")
    parser.add_argument("--audio_bitrate", type=int, default=64,
                        help="Audio bitrate (e.g. 64)")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.lang not in MESSAGES:
        args.lang = 'ru'
    msg = MESSAGES[args.lang]

    try:
        cameras = get_ip_list(args.ip)
    except ValueError as ve:
        if str(ve) == "range_error":
            print(msg["range_error"])
        else:
            print(msg["cant_parse"], ve)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

    if not cameras:
        print(msg["no_ip"])
        sys.exit(1)

    # Собираем список "полей" (для GET) в потоке
    get_fields = []
    if args.compression:
        get_fields.append("Compression=")
    if args.bit_rate:
        get_fields.append("BitRate=")
    if args.bit_rate_control:
        get_fields.append("BitRateControl=")
    if args.resolution:
        get_fields.append("resolution=")
    if args.fps:
        get_fields.append("FPS=")

    # Собираем список param_str для установки (stream)
    set_params_stream = []
    ch = args.channel
    st = args.stream_type
    ix = args.stream_index
    if args.set_stream:
        if args.compression_value is not None:
            set_params_stream.append(f"Encode[{ch}].{st}[{ix}].Video.Compression={args.compression_value}")
        if args.bit_rate_value is not None:
            set_params_stream.append(f"Encode[{ch}].{st}[{ix}].Video.BitRate={args.bit_rate_value}")
        if args.bit_rate_control_value is not None:
            set_params_stream.append(f"Encode[{ch}].{st}[{ix}].Video.BitRateControl={args.bit_rate_control_value}")
        if args.resolution_value is not None:
            set_params_stream.append(f"Encode[{ch}].{st}[{ix}].Video.resolution={args.resolution_value}")
        if args.fps_value is not None:
            set_params_stream.append(f"Encode[{ch}].{st}[{ix}].Video.FPS={args.fps_value}")
        # ... quality, gop, priority, etc.

    from dahua_api.camera_stream import get_stream_config
    from dahua_api.camera_common import set_single_param

    for cam in cameras:
        # --- 1) GET stream ---
        if args.get_stream:
            r = get_stream_config(cam, args.user, args.pwd, channel=ch, stream_type=st, index=ix)
            if isinstance(r, Exception):
                print(f"{msg['get_fail']} {cam}: {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['get_ok']} {cam}")
                    lines = r.text.splitlines()
                    if get_fields:
                        for line in lines:
                            if any(f in line for f in get_fields):
                                print(line)
                    else:
                        # если не указаны флаги --compression, --bit_rate и т.д., то выводим всё
                        for line in lines:
                            print(line)
                else:
                    print(f"{msg['get_fail']} {cam}: {r.status_code}")

        # --- 2) SET stream (по одному параметру) ---
        if args.set_stream:
            for param_str in set_params_stream:
                resp = set_single_param(cam, args.user, args.pwd, param_str)
                if isinstance(resp, Exception):
                    print(f"{msg['set_fail']} {cam}: {resp}")
                else:
                    if resp.status_code == 200:
                        print(f"{msg['set_ok']} {cam} ({param_str})")
                    else:
                        print(f"{msg['set_fail']} {cam} ({param_str}): {resp.status_code}")

        # --- 3) GET / SET NTP ---
        if args.get_ntp:
            r = get_ntp_config(cam, args.user, args.pwd)
            if isinstance(r, Exception):
                print(f"{msg['get_fail']} {cam} (NTP): {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['get_ok']} {cam} (NTP)")
                    print(r.text)
                else:
                    print(f"{msg['get_fail']} {cam} (NTP): {r.status_code}")

        if args.set_ntp:
            en_ntp = True if args.enable_ntp else False
            r = set_ntp_config(
                cam, args.user, args.pwd,
                enable=en_ntp,
                server=args.ntp_server,
                port=args.ntp_port,
                interval=args.ntp_interval,
                timezone=args.ntp_timezone
            )
            if isinstance(r, Exception):
                print(f"{msg['set_fail']} {cam} (NTP): {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['set_ok']} {cam} (NTP)")
                else:
                    print(f"{msg['set_fail']} {cam} (NTP): {r.status_code}")

        # --- 4) GET / SET RTSP ---
        if args.get_rtsp:
            r = get_rtsp_config(cam, args.user, args.pwd)
            if isinstance(r, Exception):
                print(f"{msg['get_fail']} {cam} (RTSP): {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['get_ok']} {cam} (RTSP)")
                    print(r.text)
                else:
                    print(f"{msg['get_fail']} {cam} (RTSP): {r.status_code}")

        if args.set_rtsp:
            r = set_rtsp_config(cam, args.user, args.pwd, rtsp_port=args.rtsp_port, rtsp_auth=args.rtsp_auth)
            if isinstance(r, Exception):
                print(f"{msg['set_fail']} {cam} (RTSP): {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['set_ok']} {cam} (RTSP)")
                else:
                    print(f"{msg['set_fail']} {cam} (RTSP): {r.status_code}")

        # --- 5) GET / SET Audio ---
        if args.get_audio:
            r = get_audio_config(cam, args.user, args.pwd, channel=args.audio_channel)
            if isinstance(r, Exception):
                print(f"{msg['get_fail']} {cam} (Audio): {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['get_ok']} {cam} (Audio)")
                    print(r.text)
                else:
                    print(f"{msg['get_fail']} {cam} (Audio): {r.status_code}")

        if args.set_audio:
            # Определим enable или disable
            audio_en = True
            if args.audio_disable:
                audio_en = False
            elif args.audio_enable:
                audio_en = True
            # compression / bitrate можно взять из args
            r = set_audio_config(
                cam, args.user, args.pwd,
                channel=args.audio_channel,
                enable=audio_en,
                compression=args.audio_compression,
                bitrate=args.audio_bitrate
            )
            if isinstance(r, Exception):
                print(f"{msg['set_fail']} {cam} (Audio): {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['set_ok']} {cam} (Audio)")
                else:
                    print(f"{msg['set_fail']} {cam} (Audio): {r.status_code}")

    print(msg["done"])


if __name__ == "__main__":
    main()
