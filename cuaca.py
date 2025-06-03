from flask import Flask, render_template_string, request, redirect, url_for
import requests
import mysql.connector

API_KEY = 'YOUR_API_KEY'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="cuaca_app"
)
cursor = db.cursor()

app = Flask(__name__)

HTML = '''
<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <title>Cek Cuaca</title>
  <style>
    body {
      background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
      font-family: 'Segoe UI', Arial, sans-serif;
      margin: 0;
      padding: 0;
      min-height: 100vh;
    }
    .container {
      background: rgba(255,255,255,0.95);
      max-width: 420px;
      margin: 40px auto;
      border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.18);
      padding: 32px 28px 24px 28px;
    }

        h1 {
      text-align: center;
      color: #2471A3;
      margin-bottom: 24px;
    }
    form {
      display: flex;
      justify-content: center;
      gap: 8px;
      margin-bottom: 18px;
    }
    input[type="text"] {
      padding: 8px 12px;
      border: 1px solid #b2bec3;
      border-radius: 6px;
      font-size: 1em;
      width: 60%;
    }
    input[type="submit"] {
      background: #2471A3;
      color: #fff;
      border: none;
      border-radius: 6px;
      padding: 8px 18px;
      font-size: 1em;
      cursor: pointer;
      transition: background 0.2s;
    }
    input[type="submit"]:hover {
      background: #1b4f72;
    }
    .hasil {
      background: #d6eaff;
      border-left: 5px solid #2471A3;
      padding: 12px 16px;
      margin-bottom: 18px;
      border-radius: 8px;
      font-size: 1.1em;
    }
    h2 {
      color: #2471A3;
      margin-top: 24px;
      margin-bottom: 10px;
      font-size: 1.2em;
    }
    ul {
      list-style: none;
      padding: 0;
      margin: 0;
      max-height: 180px;
      overflow-y: auto;
    }
    li {
      background: #f4f8fb;
      margin-bottom: 8px;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 0.98em;
      box-shadow: 0 1px 2px rgba(36,113,163,0.04);
    }
    @media (max-width: 500px) {
      .container { padding: 18px 6px; }
      input[type="text"] { width: 100%; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🌤️ Cek Cuaca</h1>
    <form method="post" action="/">
      <input type="text" name="kota" placeholder="Masukkan nama kota" required>
      <input type="submit" value="Cek">
    </form>
    {% if hasil %}
      <div class="hasil">
        <b>Cuaca di {{ hasil.kota|capitalize }}:</b> {{ hasil.suhu }}°C, {{ hasil.deskripsi|capitalize }}
      </div>
    {% endif %}
    <h2>Riwayat Cuaca</h2>
    <ul>
    {% for row in riwayat %}
      <li>
        <b>{{ row[1]|capitalize }}</b> | {{ row[2] }}°C | {{ row[3]|capitalize }} <br>
        <small style="color:#888;">{{ row[4] }}</small>
      </li>
    {% endfor %}
    </ul>
  </div>
</body>
</html>
'''

def simpan_ke_db(kota, suhu, deskripsi):
    sql = "INSERT INTO cuaca (kota, suhu, deskripsi) VALUES (%s, %s, %s)"
    val = (kota, suhu, deskripsi)
    cursor.execute(sql, val)
    db.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    if request.method == "POST":
        kota = request.form["kota"]
        params = {'q': kota, 'appid': API_KEY, 'units': 'metric'}
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            suhu = data['main']['temp']
            deskripsi = data['weather'][0]['description']
            hasil = {"kota": kota, "suhu": suhu, "deskripsi": deskripsi}
            simpan_ke_db(kota, suhu, deskripsi)
        else:
            hasil = {"kota": kota, "suhu": "-", "deskripsi": "Kota tidak ditemukan atau error API."}
    cursor.execute("SELECT * FROM cuaca ORDER BY waktu DESC")
    riwayat = cursor.fetchall()
    return render_template_string(HTML, hasil=hasil, riwayat=riwayat)

if __name__ == "__main__":
    app.run(debug=True)
