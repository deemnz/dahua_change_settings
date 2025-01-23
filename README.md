Dahua Change Settings
Скрипт на Python для массового управления настройками Dahua-камер (IP-адреса, порты, параметры видеопотоков, RTSP, NTP, снапшоты и пр.) через HTTP API Dahua. Поддерживается Digest-аутентификация, позволяющая работать с современными прошивками, а также работа с диапазонами IP (например 192.168.1.10-192.168.1.20) и диапазонами портов (например 192.168.1.10:1008-192.168.1.10:1010).

Основные возможности
Одиночное изменение параметров (точно так же, как при ручном вызове setConfig через браузер).
Изменение нескольких параметров за один проход — если это поддерживается камерой.
Работа с диапазонами IP (или с диапазонами портов), а также чтение списков IP из файла.
Поддержка русского/английского языков выводимых сообщений (через --lang ru / --lang en).
Установка
Клонируйте репозиторий:
bash
Копировать
git clone https://github.com/deemnz/dahua_change_settings.git
Перейдите в папку проекта:
bash
Копировать
cd dahua_change_settings
Установите зависимости (включая requests):
bash
Копировать
pip install -r requirements.txt
Структура проекта (пример)
bash
Копировать
dahua_change_settings/
├── main.py                # Точка входа (CLI)
├── requirements.txt
├── utils/
│   ├── __init__.py
│   ├── messages.py        # Словарь сообщений (ru/en)
│   └── ip_utils.py        # Работа с диапазонами IP/портов, парсинг
├── dahua_api/
│   ├── __init__.py
│   ├── camera_common.py   # Общие функции GET/SET (DigestAuth)
│   ├── camera_stream.py   # Настройки видео/аудио (Encode[..])
│   ├── camera_rtsp.py     # Настройки RTSP
│   ├── camera_ntp.py      # Настройки NTP
│   └── camera_snap.py     # Настройки snapshot (Snap[..])
└── ...
Запуск скрипта
Основной запуск:

bash
Копировать
python main.py [параметры]
(Убедитесь, что запускаете из корневой папки проекта, чтобы импорты работали.)

Ключевые аргументы
--ip: Адрес камеры, диапазон IP или файл со списком адресов.
- Примеры:
- --ip 192.168.1.10 (одна камера, порт 80 по умолчанию)
- --ip 192.168.1.10:8080 (камера с нестандартным портом 8080)
- --ip cams.txt (файл, где каждая строка — ip:port)
- --ip 192.168.1.10:80-192.168.1.15:80 (диапазон IP)
- --ip 192.168.1.10:1008-192.168.1.10:1010 (один IP, разные порты)

--user, --pwd: Логин и пароль. Используется DigestAuth.

--lang: Язык вывода сообщений (ru или en). По умолчанию ru.

Режимы изменения параметров
Одиночные параметры (одноимённые короткие флаги):
Вызываем каждое изменение отдельным setConfig. Это аналогично ручному вызову в браузере.

Пример аргументов для ExtraFormat:

bash
Копировать
python main.py \
  --ip 192.168.1.10:1010 \
  --user admin --pwd 12345 \
  --stream_type ExtraFormat --stream_index 0 \
  --compression H.265 \
  --bit_rate 512 \
  --bit_rate_control VBR \
  --resolution 640x480
При этом будут отправлены несколько запросов:

mathematica
Копировать
&Encode[0].ExtraFormat[0].Video.Compression=H.265
&Encode[0].ExtraFormat[0].Video.BitRate=512
&Encode[0].ExtraFormat[0].Video.BitRateControl=VBR
&Encode[0].ExtraFormat[0].Video.resolution=640x480
— каждый по отдельности (DigestAuth автоматически handle-ит nonce, cnonce и т.д.).

Другие флаги:
- --audio_enable / --audio_disable (AudioEnable=true/false),
- --fps, --quality, --gop, --priority, --profile и т.д.
(Смотрите main.py — раздел generate_params().)

RTSP / NTP / Snap (модули camera_rtsp.py, camera_ntp.py, camera_snap.py):

--get_rtsp, --set_rtsp + --rtsp_port, --rtsp_auth
--get_ntp, --set_ntp + --enable_ntp, --ntp_server, --ntp_port, т.д.
--get_snap, --set_snap + --enable_snap, --snap_interval
Эти флаги вызывают соответствующие функции, которые отправляют один GET или SET запрос на все поля.
(Опционально) Пакетное изменение (старый режим --set_stream_all) — отправляет сразу все поля разом. Часто бывает, что если один параметр неверный, Dahua камеру игнорирует всё. Поэтому в большинстве случаев удобнее пользоваться одиночной передачей, описанной выше.

Примеры
Изменить BitRateControl на VBR для дополнительного потока и выставить битрейт 512:

bash
Копировать
python main.py \
  --ip 192.168.1.10:1010 \
  --user admin \
  --pwd 12345 \
  --stream_type ExtraFormat \
  --bit_rate_control VBR \
  --bit_rate 512
Отключить аудио для основного потока:

bash
Копировать
python main.py \
  --ip 192.168.1.10 \
  --user admin \
  --pwd 12345 \
  --audio_disable
Настройка RTSP (порт 554, аутентификация digest):

bash
Копировать
python main.py \
  --ip 192.168.1.10 \
  --user admin --pwd 12345 \
  --set_rtsp --rtsp_port 554 --rtsp_auth digest
Настройка NTP:

bash
Копировать
python main.py \
  --ip 192.168.1.10 \
  --user admin --pwd 12345 \
  --set_ntp --enable_ntp \
  --ntp_server pool.ntp.org --ntp_port 123 --ntp_interval 60 \
  --ntp_timezone "GMT+03:00-Moscow"
Диапазон портов:

bash
Копировать
python main.py \
  --ip 192.168.1.10:1008-192.168.1.10:1010 \
  --user admin --pwd 12345 \
  --bit_rate_control VBR
Скрипт переберёт 192.168.1.10:1008, 192.168.1.10:1009, 192.168.1.10:1010.

Файл со списком адресов (cams.txt):

bash
Копировать
python main.py \
  --ip cams.txt \
  --user admin --pwd 12345 \
  --bit_rate 512
В файле cams.txt перечислены строки вроде 192.168.1.10:80, 192.168.1.11:8080 и т.д.

Замечания
DigestAuth уже встроен в код (через requests.auth.HTTPDigestAuth). Если логин/пароль верны, для большинства Dahua-камер не нужны куки или сессии.
При неподдерживаемом названии поля (например, неправильный регистр Video.Resolution vs. Video.resolution) камера вернёт 200 OK, но значение не применит.
Если несколько параметров в одном запросе, а один неверен, камера может проигнорировать весь набор. Поэтому (по возможности) лучше изменять один параметр за раз.
Для уточнения доступных полей (включая регистр букв) можно сделать:
arduino
Копировать
http://CAMERA_IP/cgi-bin/configManager.cgi?action=getConfig&name=Encode[0].ExtraFormat[0]
и посмотреть, что возвращает камера.