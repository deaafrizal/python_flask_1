import os
from groq import Groq
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

### HARDCODED AI_KEY TUTORIAL VERSION ###
# AI_KEY = "masukan api key groq disini" #
###  -------------------------------- ###

AI_KEY = os.getenv(
    "GROQ_API_KEY"
)  # komentari kode ini jika tidak menyiapkan enviroment spesifik.

if not AI_KEY:
    raise ValueError(
        "Masukan GROQ API KEY ke environment masing2 atau pake hardcoded version."
    )

client = Groq(
    api_key=AI_KEY,
)


def ai_call(year):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"berikan 1 fakta menarik seputar teknologi pada tahun {year}",
                }
            ],
            model="llama-3.2-1b-preview",
            stream=False,
        )

        ai_output = chat_completion.choices[0].message.content
        return ai_output
    except Exception:
        return "Maaf, AI tidak tersedia saat ini. Silakan coba lagi nanti."


@app.route('/')
def main():
    user = "dea"
    return render_template('index.html')

@app.route('/usia', methods=['GET', 'POST'])
def cek_usia():
    if request.method == 'POST':
        # Ambil data dari form
        tahun_lahir = int(request.form['tahun_lahir'])
        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir

        ai_output = ai_call(tahun_lahir)

        return render_template(
            "cek_usia.html", usia=usia, tahun_lahir=tahun_lahir, ai_output=ai_output
        )
    return render_template('cek_usia.html', usia= None)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
