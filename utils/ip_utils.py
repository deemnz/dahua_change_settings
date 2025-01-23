import ipaddress

def parse_ip_port(s: str):
    """
    Разбивает строку 'IP[:port]' на (ip_address, port или None).
    Пример:
      '192.168.1.10' -> (IPv4Address('192.168.1.10'), None)
      '192.168.1.10:80' -> (IPv4Address('192.168.1.10'), 80)
    """
    if ':' in s:
        ip_str, port_str = s.split(':', 1)
        return ipaddress.ip_address(ip_str), int(port_str)
    else:
        return ipaddress.ip_address(s), None


def expand_ip_range(start_str: str, end_str: str) -> list:
    """
    Обрабатывает диапазоны формата:
      - IP:port-IP:port (если IP совпадают, перебираем порты; если порты совпадают, перебираем IP)
      - IP-IP (без порта) -> перебираем IP
      - IP:port-IP (или IP-IP:port) -> считаем, что порт указан только в start (или end) и используем его
      - Если IP и порт отличаются, используем упрощённую схему:
         * перебираем IP от start_ip до end_ip,
         * порт = start_port (если он есть),
         * port2 игнорируем или должны совпадать (на ваше усмотрение).

    Примеры:
      1) "10.88.39.16:1008-10.88.39.16:1069"
         -> ["10.88.39.16:1008", "10.88.39.16:1009", ... "10.88.39.16:1069"]
      2) "192.168.100.6:80-192.168.100.9:80"
         -> ["192.168.100.6:80", "192.168.100.7:80", ... "192.168.100.9:80"]
      3) "192.168.100.6-192.168.100.69"
         -> ["192.168.100.6", "192.168.100.7", ... "192.168.100.69"]
      4) "192.168.100.6:80-192.168.100.9:81" (разные IP и разные порты)
         -> Перебираем IP от .6 до .9, порт = 80 (port1).
    """

    ip1, port1 = parse_ip_port(start_str)
    ip2, port2 = parse_ip_port(end_str)

    # Если IP одинаковые
    if ip1 == ip2:
        # Если оба порта заданы и отличаются -> перебор портов
        if port1 is not None and port2 is not None and port1 != port2:
            start_p = min(port1, port2)
            end_p = max(port1, port2)
            return [f"{ip1}:{p}" for p in range(start_p, end_p + 1)]
        else:
            # Один порт (или совпадают), либо оба None => фактически 1 IP
            # Если нужно перебрать порты при port1=port2, это редкий случай, пока считаем 1 IP
            # Можно возвращать IP:port, если port1 есть, иначе просто IP
            if port1 is not None:
                return [f"{ip1}:{port1}"]
            elif port2 is not None:
                return [f"{ip1}:{port2}"]
            else:
                return [str(ip1)]
    else:
        # IP разные -> перебираем IP от ip1..ip2
        if ip2 < ip1:
            ip1, ip2 = ip2, ip1

        results = []
        current = ip1
        while current <= ip2:
            if port1 is not None:
                results.append(f"{current}:{port1}")
            else:
                # порт не задан
                results.append(str(current))
            current += 1
        return results


def get_ip_list(ip_arg: str) -> list:
    """
    Проверяем, не является ли ip_arg файлом.
    Если в строке есть '-', считаем, что это диапазон (ip:port-ip:port) или (ip-ip).
    Иначе одиночный IP (с портом или без).
    """
    import os

    if os.path.isfile(ip_arg):
        out = []
        with open(ip_arg, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    out.append(line)
        return out

    if '-' in ip_arg:
        parts = ip_arg.split('-', 1)
        if len(parts) != 2:
            raise ValueError("range_error")
        start_str, end_str = parts
        return expand_ip_range(start_str, end_str)

    # Одиночный IP
    return [ip_arg]
