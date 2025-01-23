import argparse
import sys

from utils.ip_utils import get_ip_list
from utils.messages import MESSAGES
from dahua_api.camera_common import set_single_param
from dahua_api.camera_stream import get_stream_config


def parse_args():
    parser = argparse.ArgumentParser(description="Dahua Change Settings")

    parser.add_argument("--lang", default="ru", help="Language: ru/en")
    parser.add_argument("--ip", required=True,
                        help="Camera IP, range ip:port-ip:port, or file with IP list")
    parser.add_argument("--user", required=True,
                        help="Camera login")
    parser.add_argument("--pwd", required=True,
                        help="Camera password")

    # Флаги управления потоком
    parser.add_argument("--get_stream", action="store_true",
                        help="GET (read) stream config: Encode[channel].stream_type[stream_index]")
    parser.add_argument("--set_stream", action="store_true",
                        help="SET (write) stream config: Encode[channel].stream_type[stream_index].Video.*")

    parser.add_argument("--channel", type=int, default=0, help="Encode[...] channel index (default 0)")
    parser.add_argument("--stream_type", type=str, default="MainFormat", help="MainFormat / ExtraFormat / etc.")
    parser.add_argument("--stream_index", type=int, default=0, help="Index of the stream, usually 0")

    # Параметры Video, которые можно прочитать/установить
    parser.add_argument("--compression", action="store_true",
                        help="Compression (H.264/H.265). For get => filter, for set => pass value via --compression_value")
    parser.add_argument("--compression_value", type=str,
                        help="Value for Video.Compression, e.g. H.265 (used with --set_stream)")

    parser.add_argument("--bit_rate", action="store_true",
                        help="BitRate (Kbps). For get => filter, for set => pass value via --bit_rate_value")
    parser.add_argument("--bit_rate_value", type=int,
                        help="Value for Video.BitRate, e.g. 512")

    parser.add_argument("--bit_rate_control", action="store_true",
                        help="BitRateControl (CBR/VBR). For get => filter, for set => pass value via --bit_rate_control_value")
    parser.add_argument("--bit_rate_control_value", type=str,
                        help="Value for Video.BitRateControl, e.g. VBR")

    parser.add_argument("--resolution", action="store_true",
                        help="Video.resolution=, for get => filter, for set => use --resolution_value (e.g. 640x480)")
    parser.add_argument("--resolution_value", type=str,
                        help="Value for Video.resolution")

    parser.add_argument("--fps", action="store_true",
                        help="Video.FPS. For get => filter, for set => pass value via --fps_value")
    parser.add_argument("--fps_value", type=int,
                        help="Value for Video.FPS")

    parser.add_argument("--quality", action="store_true",
                        help="Video.Quality. For get => filter, for set => pass value via --quality_value")
    parser.add_argument("--quality_value", type=int,
                        help="Value for Video.Quality")

    # ... при желании можно добавить gop, profile, priority, audio_enable и т.п.

    return parser.parse_args()


def main():
    args = parse_args()

    # Установка языка
    if args.lang not in MESSAGES:
        args.lang = 'ru'
    msg = MESSAGES[args.lang]

    # Получаем список IP (одиночный, диапазон, файл)
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

    # Список "поля, которые пользователь хочет получить" (для GET)
    # Мы сопоставим: если user указал --compression => хотим вытащить "Compression="
    # Если user указал --bit_rate => хотим "BitRate=" и т.д.
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
    if args.quality:
        get_fields.append("Quality=")
    # ... при желании другие поля

    # Список (param_str) -> для SET
    # Если user указал --compression_value "H.265", значит:
    # "Encode[0].MainFormat[0].Video.Compression=H.265"
    set_params = []
    ch = args.channel
    st = args.stream_type
    ix = args.stream_index

    # Если user сказал --compression и --compression_value => SET
    if args.set_stream and args.compression_value is not None:
        set_params.append(f"Encode[{ch}].{st}[{ix}].Video.Compression={args.compression_value}")
    if args.set_stream and args.bit_rate_value is not None:
        set_params.append(f"Encode[{ch}].{st}[{ix}].Video.BitRate={args.bit_rate_value}")
    if args.set_stream and args.bit_rate_control_value is not None:
        set_params.append(f"Encode[{ch}].{st}[{ix}].Video.BitRateControl={args.bit_rate_control_value}")
    if args.set_stream and args.resolution_value is not None:
        # Обратите внимание на регистр 'resolution' (см. GET-ответ)
        set_params.append(f"Encode[{ch}].{st}[{ix}].Video.resolution={args.resolution_value}")
    if args.set_stream and args.fps_value is not None:
        set_params.append(f"Encode[{ch}].{st}[{ix}].Video.FPS={args.fps_value}")
    if args.set_stream and args.quality_value is not None:
        set_params.append(f"Encode[{ch}].{st}[{ix}].Video.Quality={args.quality_value}")
    # ... аналогично можно расширить

    from dahua_api.camera_stream import get_stream_config
    from dahua_api.camera_common import set_single_param

    for cam in cameras:
        # 1. GET (если user указал --get_stream)
        if args.get_stream:
            r = get_stream_config(cam, args.user, args.pwd,
                                  channel=ch,
                                  stream_type=st,
                                  index=ix)
            if isinstance(r, Exception):
                print(f"{msg['get_fail']} {cam}: {r}")
            else:
                if r.status_code == 200:
                    print(f"{msg['get_ok']} {cam}")
                    lines = r.text.splitlines()
                    # Если пользователь указал хотя бы один --compression / --bit_rate и т.д.
                    # то мы фильтруем только нужные строки
                    if get_fields:
                        for line in lines:
                            # Проверяем, содержит ли строка один из полей
                            if any(f in line for f in get_fields):
                                print(line)
                    else:
                        # Если не указаны конкретные поля, выводим всё
                        for line in lines:
                            print(line)
                else:
                    print(f"{msg['get_fail']} {cam}: {r.status_code}")

        # 2. SET (если user указал --set_stream) - по одному параметру на запрос
        if args.set_stream:
            for param_str in set_params:
                resp = set_single_param(cam, args.user, args.pwd, param_str)
                if isinstance(resp, Exception):
                    print(f"{msg['set_fail']} {cam}: {resp}")
                else:
                    if resp.status_code == 200:
                        print(f"{msg['set_ok']} {cam} ({param_str})")
                    else:
                        print(f"{msg['set_fail']} {cam} ({param_str}): {resp.status_code}")

    print(msg["done"])


if __name__ == "__main__":
    main()
