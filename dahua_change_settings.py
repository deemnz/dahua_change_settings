import os
import requests
from requests.auth import HTTPDigestAuth

# Отключаем использование системного прокси
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
os.environ['ftp_proxy'] = ''


def fetch_url_content(url, username, password, headers=None):
    """
    Отправка запроса с Digest Authentication напрямую, обходя системный прокси.
    """
    try:
        proxies = {}  # Явно отключаем прокси в requests
        response = requests.get(url, auth=HTTPDigestAuth(username, password), proxies=proxies, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе: {e}"


def generate_ip_range(start_ip, end_ip):
    """
    Генерирует список IP-адресов в заданном диапазоне.

    Args:
        start_ip (str): Начальный IP-адрес (например, 192.168.100.6).
        end_ip (str): Конечный IP-адрес (например, 192.168.100.10).

    Returns:
        list: Список IP-адресов.
    """
    start_parts = list(map(int, start_ip.split('.')))
    end_parts = list(map(int, end_ip.split('.')))
    return [f"{start_parts[0]}.{start_parts[1]}.{start_parts[2]}.{i}" for i in range(start_parts[3], end_parts[3] + 1)]


def select_suffix_file():
    """
    Отображает список файлов с суффиксами и позволяет выбрать один.
    """
    print("\nДоступные файлы с суффиксами в текущей папке:")
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(".txt")]

    if not files:
        print("Нет доступных файлов с суффиксами (.txt).")
        return None

    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

    try:
        file_choice = int(input("Введите номер файла: ").strip()) - 1
        if file_choice < 0 or file_choice >= len(files):
            print("Неверный выбор.")
            return None
        return files[file_choice]
    except ValueError:
        print("Ошибка ввода.")
        return None


def process_ips_and_suffixes():
    """
    Обрабатывает диапазон IP или одиночный IP с суффиксами из выбранного файла.
    """
    username = input("Введите имя пользователя: ").strip()
    password = input("Введите пароль: ").strip()

    # Ввод диапазона IP или одиночного IP
    ip_input = input("Введите диапазон IP (например, 192.168.100.6-192.168.100.10) или один IP: ").strip()
    if '-' in ip_input:
        start_ip, end_ip = ip_input.split('-')
        ips = generate_ip_range(start_ip.strip(), end_ip.strip())
    else:
        ips = [ip_input.strip()]

    # Выбор файла с суффиксами
    suffix_file = select_suffix_file()
    if not suffix_file:
        print("Не выбран файл с суффиксами. Завершение.")
        return

    try:
        with open(suffix_file, "r", encoding="utf-8") as file:
            suffixes = [line.strip() for line in file if line.strip()]
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Заголовки для имитации браузерного запроса
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    # Обработка URL для каждого IP и суффикса
    for ip in ips:
        for suffix in suffixes:
            url = f"http://{ip}{suffix}"
            print(f"\nОбработка URL: {url}")
            response = fetch_url_content(url, username, password, headers=headers)
            print(f"Ответ от {ip}:\n{response}")


def main():
    """
    Меню выбора действий для пользователя.
    """
    while True:
        print("\nВыберите опцию:")
        print("1. Обработать диапазон IP и суффиксы URL")
        print("2. Выйти")
        choice = input("Введите ваш выбор: ").strip()

        if choice == "1":
            process_ips_and_suffixes()
        elif choice == "2":
            print("Выход.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
