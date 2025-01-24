<h1>Dahua Bulk Change Settings</h1>

<p>
A Python script for bulk management of Dahua camera settings (IP addresses, ports, video stream parameters, 
RTSP, NTP, snapshots, etc.) via the Dahua HTTP API. It supports <strong>Digest authentication</strong>, 
allowing it to work with modern firmwares, as well as working with IP ranges 
(for example <code>192.168.1.10-192.168.1.20</code>) and port ranges 
(for example <code>192.168.1.10:1008-192.168.1.10:1010</code>).
</p>

<h2>Main Features</h2>
<ul>
  <li><strong>Single parameter changes</strong> (just like manually calling <code>setConfig</code> in a browser).</li>
  <li>Changing multiple parameters <strong>in one pass</strong> — if supported by the camera.</li>
  <li>Working with <strong>IP ranges</strong> (or port ranges), as well as reading IP lists from a file.</li>
  <li>Support for <strong>Russian/English</strong> output messages (via <code>--lang ru</code> / <code>--lang en</code>).</li>
</ul>

<h2>Installation</h2>
<ol>
  <li>Clone the repository:
    <pre><code>git clone https://github.com/deemnz/dahua_change_settings.git</code></pre>
  </li>
  <li>Go to the project folder:
    <pre><code>cd dahua_change_settings</code></pre>
  </li>
  <li>Install dependencies (including <code>requests</code>):
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
</ol>

<h2>Project Structure (example)</h2>
<pre><code>dahua_change_settings/
├── main.py                # Entry point (CLI)
├── requirements.txt
├── utils/
│   ├── __init__.py
│   ├── messages.py        # Dictionary of messages (ru/en)
│   └── ip_utils.py        # Working with IP/port ranges, parsing
├── dahua_api/
│   ├── __init__.py
│   ├── camera_common.py   # Common GET/SET functions (DigestAuth)
│   ├── camera_stream.py   # Video/audio settings (Encode[..])
│   ├── camera_rtsp.py     # RTSP settings
│   ├── camera_ntp.py      # NTP settings
│   └── camera_snap.py     # Snapshot settings (Snap[..])
└── ...
</code></pre>

<h2>Running the Script</h2>
<p>
Basic usage:
</p>
<pre><code>python main.py [options]
</code></pre>
<p>
(Make sure you run it from the project's root folder so that imports work correctly.)
</p>

<h3>Key Arguments</h3>
<ul>
  <li><code>--ip</code>: Camera address, IP range, or a file with a list of addresses.
    <ul>
      <li><strong>Examples:</strong></li>
      <li><code>--ip 192.168.1.10</code> (single camera, default port 80)</li>
      <li><code>--ip 192.168.1.10:8080</code> (camera with non-standard port 8080)</li>
      <li><code>--ip cams.txt</code> (file where each line is <code>ip:port</code>)</li>
      <li><code>--ip 192.168.1.10:80-192.168.1.15:80</code> (IP range)</li>
      <li><code>--ip 192.168.1.10:1008-192.168.1.10:1010</code> (same IP, different ports)</li>
    </ul>
  </li>
  <li><code>--user</code>, <code>--pwd</code>: Login and password. DigestAuth is used.</li>
  <li><code>--lang</code>: Language for output messages (<code>ru</code> or <code>en</code>). Default is <code>ru</code>.</li>
</ul>

<h3>Parameter Change Modes</h3>
<ol>
  <li>
    <strong>Single parameters</strong> (similarly named short flags).
    <p>
      Each change is sent via an individual <code>setConfig</code> call, just like a manual call in the browser.
      For example, arguments for <em>ExtraFormat</em>:
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
      This will send multiple requests:
    </p>
    <pre><code>&Encode[0].ExtraFormat[0].Video.Compression=H.265
&Encode[0].ExtraFormat[0].Video.BitRate=512
&Encode[0].ExtraFormat[0].Video.BitRateControl=VBR
&Encode[0].ExtraFormat[0].Video.resolution=640x480
</code></pre>
    <p>— each one separately (DigestAuth automatically handles nonce, cnonce, etc.).</p>

    Other flags:
      --audio_enable / --audio_disable (AudioEnable=true/false),
      --fps, --quality, --gop, --priority, --profile, etc.
      (See main.py — the generate_params() section.)    
  </li>
  <li>
    <strong>RTSP / NTP / Snap</strong> (modules <code>camera_rtsp.py</code>, <code>camera_ntp.py</code>, <code>camera_snap.py</code>):
    <ul>
      <li><code>--get_rtsp</code>, <code>--set_rtsp</code> + <code>--rtsp_port</code>, <code>--rtsp_auth</code></li>
      <li><code>--get_ntp</code>, <code>--set_ntp</code> + <code>--enable_ntp</code>, <code>--ntp_server</code>, <code>--ntp_port</code>, etc.</li>
      <li><code>--get_snap</code>, <code>--set_snap</code> + <code>--enable_snap</code>, <code>--snap_interval</code></li>
    </ul>
    <p>
      These flags call the corresponding functions that send a single GET or SET request for all fields.
    </p>
  </li>
  <li>
    <strong>(Optional) Batch changes</strong> (the old mode <code>--set_stream_all</code>)
    — sends all fields at once in a single request. Often, if one parameter is invalid, the camera ignores the entire request.
    So in most cases, it’s more convenient to use <strong>single-parameter</strong> changes.
  </li>
</ol>

<h3>Examples</h3>
<ul>
  <li><strong>Change BitRateControl</strong> to VBR for the extra stream and set bitrate to 512:</li>
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
  <li><strong>Get camera settings:</li>
</ul>

<pre><code>python main.py \
  --lang ru \
  --ip 10.88.39.16:1006 \
  --user admin \
  --pwd 39Cprkbgr! \
  --get_stream
</code></pre>

<ul>
  <li><strong>Disable audio</strong> for the main stream:</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10 \
  --user admin \
  --pwd 12345 \
  --audio_disable
</code></pre>

<ul>
  <li><strong>RTSP setup</strong> (port 554, digest authentication):</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10 \
  --user admin --pwd 12345 \
  --set_rtsp --rtsp_port 554 --rtsp_auth digest
</code></pre>

<ul>
  <li><strong>NTP setup</strong>:</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10 \
  --user admin --pwd 12345 \
  --set_ntp --enable_ntp \
  --ntp_server pool.ntp.org --ntp_port 123 --ntp_interval 60 \
  --ntp_timezone "GMT+03:00-Moscow"
</code></pre>

<ul>
  <li><strong>Port range</strong>:</li>
</ul>
<pre><code>python main.py \
  --ip 192.168.1.10:1008-192.168.1.10:1010 \
  --user admin --pwd 12345 \
  --bit_rate_control VBR
</code></pre>
<p>
The script will iterate over <code>192.168.1.10:1008</code>, <code>192.168.1.10:1009</code>, and <code>192.168.1.10:1010</code>.
</p>

<ul>
  <li><strong>File with a list of addresses</strong> (<code>cams.txt</code>):</li>
</ul>
<pre><code>python main.py \
  --ip cams.txt \
  --user admin --pwd 12345 \
  --bit_rate 512
</code></pre>
<p>In <code>cams.txt</code>, there are lines like <code>192.168.1.10:80</code>, <code>192.168.1.11:8080</code>, etc.</p>

<h3>Notes</h3>
<ul>
  <li><strong>DigestAuth</strong> is already built into the code (via <code>requests.auth.HTTPDigestAuth</code>).
    If the login/password are correct, most Dahua cameras do not need cookies or sessions.
  </li>
  <li>If an unsupported field name is used (for example, the wrong letter case
    <code>Video.Resolution</code> vs. <code>Video.resolution</code>), the camera will return <code>200 OK</code>,
    but the value will not be applied.
  </li>
  <li>If multiple parameters are included in one request and one is invalid, the camera may ignore the entire request.
    Therefore, (if possible) it’s better to <strong>change one parameter at a time</strong>.
  </li>
  <li>To check available fields (including letter case), you can do:
    <pre><code>http://CAMERA_IP/cgi-bin/configManager.cgi?action=getConfig&amp;name=Encode[0].ExtraFormat[0]</code></pre>
    and see what the camera returns.
  </li>
</ul>
