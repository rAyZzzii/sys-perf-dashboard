from flask import Flask, jsonify, render_template_string
import psutil

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>System Performance Dashboard</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #1e1e2e; color: #cdd6f4; margin: 0; padding: 40px; display: flex; flex-direction: column; align-items: center; }
        h1 { color: #89b4fa; margin-bottom: 30px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; width: 100%; max-width: 1000px; }
        .card { background: #313244; padding: 25px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); border-left: 5px solid #cba6f7; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); }
        .card h3 { margin-top: 0; color: #a6e3a1; font-size: 1.2rem; }
        .value { font-size: 2rem; font-weight: bold; margin: 10px 0; color: #f38ba8; }
        .details { font-size: 0.9rem; color: #a6adc8; }
    </style>
    <script>
        async function fetchStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('cpu').innerText = data.cpu + '%';
                
                document.getElementById('ram').innerText = data.ram.percent + '%';
                document.getElementById('ram-details').innerText = (data.ram.used / 1e9).toFixed(2) + ' GB / ' + (data.ram.total / 1e9).toFixed(2) + ' GB';
                
                document.getElementById('disk').innerText = data.disk.percent + '%';
                document.getElementById('disk-details').innerText = (data.disk.used / 1e9).toFixed(2) + ' GB / ' + (data.disk.total / 1e9).toFixed(2) + ' GB';
                
                document.getElementById('net-sent').innerText = (data.net.bytes_sent / 1e6).toFixed(2) + ' MB';
                document.getElementById('net-recv').innerText = (data.net.bytes_recv / 1e6).toFixed(2) + ' MB';
            } catch (err) {
                console.error("Error fetching stats: ", err);
            }
        }
        setInterval(fetchStats, 2000);
        window.onload = fetchStats;
    </script>
</head>
<body>
    <h1>System Performance Dashboard</h1>
    <div class="grid">
        <div class="card" style="border-left-color: #f38ba8;">
            <h3>CPU Usage</h3>
            <div class="value" id="cpu">--%</div>
            <div class="details">Overall CPU load</div>
        </div>
        <div class="card" style="border-left-color: #fab387;">
            <h3>RAM Usage</h3>
            <div class="value" id="ram">--%</div>
            <div class="details" id="ram-details">-- GB / -- GB</div>
        </div>
        <div class="card" style="border-left-color: #a6e3a1;">
            <h3>Disk Usage (/)</h3>
            <div class="value" id="disk">--%</div>
            <div class="details" id="disk-details">-- GB / -- GB</div>
        </div>
        <div class="card" style="border-left-color: #89b4fa;">
            <h3>Network Activity</h3>
            <div class="details">Sent: <strong id="net-sent" class="value" style="font-size:1.2rem;">-- MB</strong></div>
            <div class="details">Recv: <strong id="net-recv" class="value" style="font-size:1.2rem;">-- MB</strong></div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def stats():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    return jsonify({
        'cpu': cpu,
        'ram': {'total': ram.total, 'used': ram.used, 'percent': ram.percent},
        'disk': {'total': disk.total, 'used': disk.used, 'percent': disk.percent},
        'net': {'bytes_sent': net.bytes_sent, 'bytes_recv': net.bytes_recv}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
