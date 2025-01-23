<h1>Dahua Change Settings</h1>

<p>
Скрипт на Python для массового управления настройками Dahua-камер (IP-адреса, порты, параметры 
видеопотоков, RTSP, NTP, снапшоты и пр.) через HTTP API Dahua. Поддерживается <strong>Digest-аутентификация</strong>, 
позволяющая работать с современными прошивками, а также работа с диапазонами IP 
(например <code>192.168.1.10-192.168.1.20</code>) и диапазонами портов 
(например <code>192.168.1.10:1008-192.168.1.10:1010</code>).
</p>

<h2>Основные возможности</h2>
<ul>
  <li><strong>Одиночное изменение параметров</strong> (точно так же, как при ручном вызове <code>setConfig</code> через браузер).</li>
  <li>Изменение нескольких параметров <strong>за один проход</strong> — если это поддерживается камерой.</li>
  <li>Работа с <strong>диапазонами IP</strong> (или с диапазонами портов), а также чтение списков IP из файла.</li>
  <li>Поддержка <strong>русского/английского</strong> языков выводимых сообщений (через <code>--lang ru</code> / <code>--lang en</code>).</li>
</ul>

<h2>Установка</h2>
<ol>
  <li>Клонируйте репозиторий:
    <pre><code>git clone https://github.com/deemnz/dahua_change_settings.git</code></pre>
  </li>
  <li>Перейдите в папку проекта:
    <pre><code>cd dahua_change_settings</code></pre>
  </li>
  <li>Установите зависимости (включая <code>requests</code>):
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
</ol>

<h2>Структура проекта (пример)</h2>
<pre><code>dahua_change_settings/
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
</code></pre>

<h2>Запуск скрипта</h2>
<p>
Основной запуск:
</p>
<pre><code>python main.py [параметры]
</code></pre>
<p>
(Убедитесь, что запускаете из корневой папки проекта, чтобы импорты работали.)
</p>

<h3>Ключевые аргументы</h3>
<ul>
  <li><code>--ip</code>: Адрес камеры, диапазон IP или файл со списком адресов.
    <ul>
      <li><strong>Примеры:</strong></li>
      <li><code>--ip 192.168.1.10</code> (одна камера, порт 80 по умолчанию)</li>
      <li><code>--ip 192.168.1.10:8080</code> (камера с нестандартным портом 8080)</li>
      <li><code>--ip cams.txt</code> (файл, где каждая строка — <code>ip:port</code>)</li>
      <li><code>--ip 192.168.1.10:80-192.168.1.15:80</code> (диапазон IP)</li>
      <li><code>--ip 192.168.1.10:1008-192.168.1.10:1010</code> (один IP, разные порты)</li>
    </ul>
  </li>
  <li><code>--user</code>, <code>--pwd</code>: Логин и пароль. Используется DigestAuth.</li>
  <li><code>--lang</code>: Язык вывода сообщений (<code>ru</code> или <code>en</code>). По умолчанию <code>ru</code>.</li>
</ul>

<h3>Режимы изменения параметров</h3>
<ol>
  <li>
    <strong>Одиночные параметры</strong> (одноимённые короткие флаги).
    <p>
      Вызываем каждое изменение отдельным <code>setConfig</code>. Это аналогично ручному вызову в браузере.  
      Пример аргументов для <em>ExtraFormat</em>:
    </p>
    <pre><code>python main.py \
  --ip 192.168.1.10:1010 \
  --user admin --pwd 12345 \
  --stream_type ExtraFormat --stream_index 0 \
  --compression H.265 \
  --bit_rate 512 \
  --bit_rate_control VBR \
  --resolution 640x480
</code></pre>
    <p>
      При этом будут отправлены несколько запросов:
    </p>
    <pre><code>&Encode[0].ExtraFormat[0].Video.Compression=H.265
&Encode[0].ExtraFormat[0].Video.BitRate=512
&Encode[0].ExtraFormat[0].Video.BitRateControl=VBR
&Encode[0].ExtraFormat[0].Video.resolution=640x480
</code></pre>
    <p>— каждый по отдельности (DigestAuth автоматически handle-ит nonce, cnonce и т.д.).</p>

    <p>Другие флаги:
      <code>--audio_enable</code> / <code>--audio_disable</code> (AudioEnable=true/false),
      <code>--fps</code>, <code>--quality</code>, <code>--gop</code>, <code>--priority</code>, <code>--profile</code> и т.д.
      (Смотрите <code>main.py</code> — раздел <code>generate_params()</code>.)
    </p>
  </li>
  <li>
    <strong>RTSP / NTP / Snap</strong> (модули <code>camera_rtsp.py</code>, <code>camera_ntp.py</code>, <code>camera_snap.py</code>):
    <ul>
      <li><code>--get_rtsp</code>, <code>--set_rtsp</code> + <code>--rtsp_port</code>, <code>--rtsp_auth</code></li>
      <li><code>--get_ntp</code>, <code>--set_ntp</code> + <code>--enable_ntp</code>, <code>--ntp_server</code>, <code>--ntp_port</code> и т.д.</li>
      <li><code>--get_snap</code>, <code>--set_snap</code> + <code>--enable_snap</code>, <code>--snap_interval</code></li>
    </ul>
    <p>
      Эти флаги вызывают соответствующие функции, которые отправляют один GET или SET запрос на все поля.
    </p>
  </li>
  <li>
    <strong>(Опционально) Пакетное изменение</strong> (старый режим <code>--set_stream_all</code>)
    — отправляет сразу все поля за один раз. Часто если один параметр неверен, камера игнорирует весь пакет.
    Поэтому в большинстве случаев удобнее пользоваться <strong>одиночной передачей</strong>.
  </li>
</ol>

<h3>Примеры</h3>
<ul>
  <li><strong>Изменить BitRateControl</strong> на VBR для дополнительного потока и выставить битрейт 512:</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10:1010 \
  --user admin \
  --pwd 12345 \
  --stream_type ExtraFormat \
  --bit_rate_control VBR \
  --bit_rate 512
</code></pre>

<ul>
  <li><strong>Отключить аудио</strong> для основного потока:</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10 \
  --user admin \
  --pwd 12345 \
  --audio_disable
</code></pre>

<ul>
  <li><strong>Настройка RTSP</strong> (порт 554, аутентификация digest):</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10 \
  --user admin --pwd 12345 \
  --set_rtsp --rtsp_port 554 --rtsp_auth digest
</code></pre>

<ul>
  <li><strong>Настройка NTP</strong>:</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10 \
  --user admin --pwd 12345 \
  --set_ntp --enable_ntp \
  --ntp_server pool.ntp.org --ntp_port 123 --ntp_interval 60 \
  --ntp_timezone "GMT+03:00-Moscow"
</code></pre>

<ul>
  <li><strong>Диапазон портов</strong>:</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10:1008-192.168.1.10:1010 \
  --user admin --pwd 12345 \
  --bit_rate_control VBR
</code></pre>
<p>
Скрипт переберёт <code>192.168.1.10:1008</code>, <code>192.168.1.10:1009</code>, <code>192.168.1.10:1010</code>.
</p>

<ul>
  <li><strong>Файл со списком адресов</strong> (<code>cams.txt</code>):</li>
</ul>
<pre><code>python main.py \
  --ip cams.txt \
  --user admin --pwd 12345 \
  --bit_rate 512
</code></pre>
<p>В файле <code>cams.txt</code> перечислены строки вида <code>192.168.1.10:80</code>, <code>192.168.1.11:8080</code> и т.д.</p>

<h3>Замечания</h3>
<ul>
  <li><strong>DigestAuth</strong> уже встроен в код (через <code>requests.auth.HTTPDigestAuth</code>). 
    Если логин/пароль верны, для большинства Dahua-камер не нужны куки или сессии.
  </li>
  <li>При неподдерживаемом названии поля (например, неправильный регистр 
    <code>Video.Resolution</code> vs. <code>Video.resolution</code>) камера вернёт <code>200 OK</code>, 
    но значение не применит.
  </li>
  <li>Если несколько параметров в одном запросе, а один неверен, камера может проигнорировать всё. 
    Поэтому (по возможности) лучше изменять <strong>один параметр за раз</strong>.
  </li>
  <li>Для уточнения доступных полей (включая регистр букв) можно сделать:
    <pre><code>http://CAMERA_IP/cgi-bin/configManager.cgi?action=getConfig&amp;name=Encode[0].ExtraFormat[0]</code></pre>
    и посмотреть, что возвращает камера.
  </li>
</ul>

<h2>Лицензия</h2>
<p>
Проект распространяется на условиях <strong>MIT License</strong> (или иной, на ваше усмотрение). 
Автор не несёт ответственности за возможные сбои, вызванные использованием данного кода.
</p>

<hr>
<p>
При возникновении вопросов, обращайтесь в <strong>Issues</strong> репозитория или создавайте Pull Request. 
Будем рады вашим улучшениям!
</p>
