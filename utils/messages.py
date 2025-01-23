# utils/messages.py

MESSAGES = {
    'ru': {
        'lang_help': "Выбор языка (ru или en)",
        'ip_help': "IP-адрес(а) или файл или диапазон ip:port-ip:port",
        'no_ip': "Не указан IP (ни файл, ни диапазон, ни одиночный IP)",
        'range_error': "Неверный формат диапазона (ip:port-ip:port)",
        'cant_parse': "Не удалось разобрать IP/диапазон",
        'read_file': "Чтение IP из файла",
        'single_ip': "Одиночный IP",
        'range_ip': "Диапазон IP",
        'get_ok': "GET запрос успешно для",
        'get_fail': "Ошибка GET запроса для",
        'set_ok': "SET запрос успешно для",
        'set_fail': "Ошибка SET запроса для",
        'done': "Готово!"
    },
    'en': {
        'lang_help': "Choose language (ru or en)",
        'ip_help': "Camera IP(s) or file or range ip:port-ip:port",
        'no_ip': "No IP specified (no file, no range, no single IP)",
        'range_error': "Invalid IP range format (ip:port-ip:port)",
        'cant_parse': "Failed to parse IP/range",
        'read_file': "Reading IP from file",
        'single_ip': "Single IP",
        'range_ip': "Range of IPs",
        'get_ok': "GET request success for",
        'get_fail': "GET request failed for",
        'set_ok': "SET request success for",
        'set_fail': "SET request failed for",
        'done': "Done!"
    }
}
