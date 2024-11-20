from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/usia', methods=['GET', 'POST'])
def cek_usia():
    if request.method == 'POST':
        # Ambil data dari form
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir
        return render_template('cek_usia.html', usia=usia, tahun_lahir=tahun_lahir)
    return render_template('cek_usia.html', usia= None)
    