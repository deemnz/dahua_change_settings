<h1>Dahua Bulk Change Settings</h1>
<p>
A Python script for bulk management of various Dahua camera settings (video streams, RTSP, NTP, audio, etc.)
through the Dahua HTTP API. It supports <strong>Digest authentication</strong>, as well as IP/port ranges
(e.g., <code>192.168.1.10-192.168.1.20</code> or <code>192.168.1.10:1008-192.168.1.10:1010</code>)
and file-based address lists.
</p>

<h2>Main Features</h2>
<ul>
  <li><strong>Video stream management</strong> (read/set parameters like BitRate, FPS, Compression, Resolution, etc.) via <code>--get_stream</code> / <code>--set_stream</code> flags.</li>
  <li><strong>NTP management</strong> (read/set) via <code>--get_ntp</code> / <code>--set_ntp</code>.</li>
  <li><strong>RTSP management</strong> (read/set) via <code>--get_rtsp</code> / <code>--set_rtsp</code>.</li>
  <li><strong>Audio management</strong> (read/set) via <code>--get_audio</code> / <code>--set_audio</code>.</li>
  <li><strong>Supports IP ranges</strong> (and port ranges) as well as file-based IP lists for bulk configuration.</li>
  <li><strong>Multilingual output</strong> (<code>--lang ru</code> or <code>--lang en</code>).</li>
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
│   ├── messages.py        # Message dictionary (ru/en)
│   └── ip_utils.py        # IP/port range handling, parsing
├── dahua_api/
│   ├── __init__.py
│   ├── camera_common.py   # Common GET/SET functions (DigestAuth)
│   ├── camera_stream.py   # get_stream_config(...) for video streams
│   ├── camera_ntp.py      # get_ntp_config(...), set_ntp_config(...)
│   ├── camera_rtsp.py     # get_rtsp_config(...), set_rtsp_config(...)
│   └── camera_audio.py    # get_audio_config(...), set_audio_config(...)
└── ...
</code></pre>

<h2>Running the Script</h2>
<p>
Run from the project root directory:
</p>
<pre><code>python main.py [arguments]
</code></pre>
<p>
Make sure you use the same Python environment where dependencies are installed.
</p>

<h2>Video Stream Settings</h2>
<p>
Use <strong>--get_stream</strong> / <strong>--set_stream</strong> to read or modify parameters such as 
<code>Compression</code>, <code>BitRate</code>, <code>BitRateControl</code>, <code>FPS</code>, <code>resolution</code>, and more.
</p>
<ul>
  <li><code>--channel 0</code>, <code>--stream_type MainFormat</code>, <code>--stream_index 0</code> specify
    which exact stream is targeted (<em>Encode[0].MainFormat[0]</em>, <em>Encode[0].ExtraFormat[0]</em>, etc.).
  </li>
</ul>

<pre><code># Example: Get only BitRate and Compression from ExtraFormat
python main.py --ip 192.168.1.10:1010 --user admin --pwd 12345 \
  --get_stream \
  --stream_type ExtraFormat \
  --stream_index 0 \
  --bit_rate \
  --compression

# Example: Set BitRate and BitRateControl (each parameter is sent as a separate request)
python main.py --ip 192.168.1.10:1010 --user admin --pwd 12345 \
  --set_stream \
  --bit_rate_value 1024 \
  --bit_rate_control_value VBR
</code></pre>

<h2>NTP Settings</h2>
<p>
Use <code>--get_ntp</code> and <code>--set_ntp</code> to read/set NTP.
</p>
<pre><code># Example: get NTP settings
python main.py --ip 192.168.1.10 --user admin --pwd 12345 --get_ntp

# Example: set NTP
python main.py --ip 192.168.1.10 --user admin --pwd 12345 \
  --set_ntp --enable_ntp \
  --ntp_server time.windows.com \
  --ntp_port 123 \
  --ntp_interval 60 \
  --ntp_timezone "GMT+03:00-Moscow"
</code></pre>

<h2>RTSP Settings</h2>
<p>
Use <code>--get_rtsp</code> / <code>--set_rtsp</code> to read/set RTSP port and authentication.
</p>
<pre><code># Example: get RTSP settings
python main.py --ip 192.168.1.10 --user admin --pwd 12345 --get_rtsp

# Example: change RTSP settings
python main.py --ip 192.168.1.10 --user admin --pwd 12345 \
  --set_rtsp \
  --rtsp_port 10554 \
  --rtsp_auth disable
</code></pre>

<h2>Audio Settings</h2>
<p>
Use <code>--get_audio</code> / <code>--set_audio</code> to read/set audio configurations (bitrate, compression, etc.).
</p>
<pre><code># Example: get audio
python main.py --ip 192.168.1.10 --user admin --pwd 12345 --get_audio

# Example: set audio (enable, G.711A, bitrate=64)
python main.py --ip 192.168.1.10 --user admin --pwd 12345 \
  --set_audio \
  --audio_enable \
  --audio_compression G.711A \
  --audio_bitrate 64
</code></pre>

<h2>IP Ranges and Files</h2>
<ul>
  <li><strong>IP range</strong>: <code>--ip 192.168.1.10-192.168.1.15</code><br>
    The script will iterate from <code>.10</code> to <code>.15</code> (port 80 by default).</li>
  <li><strong>Port range</strong>: <code>--ip 192.168.1.10:1008-192.168.1.10:1010</code><br>
    The script will iterate ports <code>1008</code>, <code>1009</code>, <code>1010</code>.</li>
  <li><strong>File</strong> with IP addresses: <code>--ip cams.txt</code>, where each line is 
    something like <code>192.168.1.10:80</code>.
  </li>
</ul>

<h2>Examples</h2>
<pre><code># Example: set VBR for all cameras in cams.txt
python main.py \
  --ip cams.txt \
  --user admin --pwd 12345 \
  --set_stream \
  --bit_rate_control_value VBR

# Example: disable audio on a range of IP addresses
python main.py \
  --ip 192.168.1.10-192.168.1.15 \
  --user admin --pwd 12345 \
  --set_audio --audio_disable
</code></pre>

<h2>Notes</h2>
<ul>
  <li><strong>DigestAuth</strong> (via <code>requests.auth.HTTPDigestAuth</code>) is enabled. 
    No extra cookies are needed if the login/password are correct.</li>
  <li>If the camera returns <code>200 OK</code> but the value does not actually change,
    check the case (uppercase/lowercase) and exact field names (see <code>getConfig&amp;name=...</code> response).</li>
  <li>If an invalid parameter is provided, Dahua may ignore the update but still return <code>200 OK</code>.</li>
  <li>To see all keys (e.g., <code>Encode[0].ExtraFormat[0]</code>), try:
    <pre><code>http://CAMERA_IP/cgi-bin/configManager.cgi?action=getConfig&amp;name=Encode[0].ExtraFormat[0]</code></pre>
    or similar requests.
  </li>
</ul>

<h2>License</h2>
<p>
Distributed under the <strong>MIT License</strong>. The author is not responsible for any consequences 
arising from use of this code.
</p>

<hr>
<p>
If you have questions or suggestions, feel free to open an <strong>Issue</strong> or Pull Request in the 
<a href="https://github.com/deemnz/dahua_change_settings">repository</a>.
</p>
