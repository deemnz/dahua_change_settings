import argparse
import sys

from utils.ip_utils import get_ip_list
from utils.messages import MESSAGES

from dahua_api.camera_common import set_single_param

def parse_args():
    parser = argparse.ArgumentParser(description="Dahua Cameras: single-param changes")

    parser.add_argument("--lang", default="ru", help="Language (ru/en)")
    parser.add_argument("--ip", required=True,
                        help="IP/file/range (e.g. 192.168.1.10:80 or cams.txt or 192.168.1.10:80-192.168.1.20:80)")
    parser.add_argument("--user", required=True, help="Camera login")
    parser.add_argument("--pwd", required=True, help="Camera password")

    # Для указания, к какому потоку обращаемся
    parser.add_argument("--channel", type=int, default=0, help="Encode channel (default 0)")
    parser.add_argument("--stream_type", type=str, default="MainFormat",
                        help="MainFormat / ExtraFormat / etc.")
    parser.add_argument("--stream_index", type=int, default=0,
                        help="Index of the stream (usually 0)")

    # --- Удобные флаги для Video ---
    # Если пользователь не укажет --compression, значит мы этот параметр не трогаем.
    parser.add_argument("--compression", type=str,
                        help="Video compression, e.g. H.264 / H.265")
    parser.add_argument("--bit_rate", type=int,
                        help="Video.BitRate (Kbps)")
    parser.add_argument("--bit_rate_control", type=str,
                        help="Video.BitRateControl (CBR/VBR)")
    parser.add_argument("--fps", type=int,
                        help="Video.FPS")
    parser.add_argument("--resolution", type=str,
                        help="Video.resolution (e.g. 640x480)")
    parser.add_argument("--width", type=int,
                        help="Video.Width")
    parser.add_argument("--height", type=int,
                        help="Video.Height")
    parser.add_argument("--quality", type=int,
                        help="Video.Quality")
    parser.add_argument("--quality_range", type=int,
                        help="Video.QualityRange")
    parser.add_argument("--gop", type=int,
                        help="Video.GOP")
    parser.add_argument("--profile", type=str,
                        help="Video.Profile (e.g. Main/High)")
    parser.add_argument("--priority", type=int,
                        help="Video.Priority")
    # ... при желании добавляйте другие

    # --- Удобные флаги для Audio (если нужно) ---
    parser.add_argument("--audio_enable", action="store_true",
                        help="Encode[..].AudioEnable=true")
    parser.add_argument("--audio_disable", action="store_true",
                        help="Encode[..].AudioEnable=false")
    parser.add_argument("--audio_bitrate", type=int,
                        help="Audio.Bitrate")
    parser.add_argument("--audio_compression", type=str,
                        help="Audio.Compression (G.711A, G.711U, AAC, etc.)")
    # ... и т.д.

    return parser.parse_args()


def main():
    args = parse_args()
    if args.lang not in MESSAGES:
        args.lang = 'ru'
    msg = MESSAGES[args.lang]

    # Получаем список IP-адресов
    try:
        cameras = get_ip_list(args.ip)
    except ValueError as ve:
        if str(ve) == "range_error":
            print(msg['range_error'])
        else:
            print(msg['cant_parse'], ve)
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

    if not cameras:
        print(msg['no_ip'])
        sys.exit(1)

    # Формируем список "параметров" для Video / Audio
    # исходя из того, что указал пользователь
    # Пример: "Encode[0].ExtraFormat[0].Video.BitRateControl=VBR"
    # Внимательно смотрим регистр - сопоставляем с тем, что в GET-ответе у вашей камеры

    # Для удобства сделаем функцию-генератор
    def generate_params():
        ch = args.channel
        st = args.stream_type
        idx = args.stream_index

        # Video
        if args.compression is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.Compression={args.compression}"
        if args.bit_rate is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.BitRate={args.bit_rate}"
        if args.bit_rate_control is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.BitRateControl={args.bit_rate_control}"
        if args.fps is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.FPS={args.fps}"
        if args.resolution is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.resolution={args.resolution}"
        if args.width is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.Width={args.width}"
        if args.height is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.Height={args.height}"
        if args.quality is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.Quality={args.quality}"
        if args.quality_range is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.QualityRange={args.quality_range}"
        if args.gop is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.GOP={args.gop}"
        if args.profile is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.Profile={args.profile}"
        if args.priority is not None:
            yield f"Encode[{ch}].{st}[{idx}].Video.Priority={args.priority}"

        # AudioEnable
        if args.audio_enable:
            yield f"Encode[{ch}].{st}[{idx}].AudioEnable=true"
        elif args.audio_disable:
            yield f"Encode[{ch}].{st}[{idx}].AudioEnable=false"

        # Audio
        if args.audio_bitrate is not None:
            yield f"Encode[{ch}].{st}[{idx}].Audio.Bitrate={args.audio_bitrate}"
        if args.audio_compression is not None:
            yield f"Encode[{ch}].{st}[{idx}].Audio.Compression={args.audio_compression}"
        # ... и т.д. по аналогии

    for cam in cameras:
        for param_str in generate_params():
            r = set_single_param(cam, args.user, args.pwd, param_str)
            if isinstance(r, Exception):
                print(f"{msg['set_fail']} {cam}: {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['set_ok']} {cam} ({param_str})")
                else:
                    print(f"{msg['set_fail']} {cam} ({param_str}): {r.status_code}")

    print(msg['done'])


if __name__ == "__main__":
    main()
