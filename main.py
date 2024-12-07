from groq import Groq
from flask import Flask, render_template, request
from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

### HARDCODED AI_KEY TUTORIAL VERSION ###
AI_KEY = "masukan api key groq disini"  #
###  -------------------------------- ###

# AI_KEY = os.getenv(
#    "GROQ_API_KEY"
# )  # komentari kode ini jika tidak menyiapkan enviroment spesifik.

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


def class_filter(media_name):
    class_name = ""
    element_selector = ""

    if media_name == "kompas":
        class_name = "hlTitle"
        element_selector = "h1"
    elif media_name == "detik":
        class_name = "media__title"
        element_selector = "h2"
    elif media_name == "tribun":
        class_name = "hltitle"
        element_selector = "div"

    return [class_name, element_selector]


def scrape_news(name, url):
    detector = class_filter(name)
    class_name, element_selector = detector[0], detector[1]

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    headline_element = soup.find(element_selector, class_=class_name)
    return headline_element.text.strip()


@app.route("/")
def main():
    kompas = scrape_news("kompas", "https://www.kompas.com/")
    detik = scrape_news("detik", "https://news.detik.com/")
    tribun = scrape_news("tribun", "https://www.tribunnews.com/")

    return render_template("index.html", news1=kompas, news2=detik, news3=tribun)


@app.route("/usia", methods=["GET", "POST"])
def cek_usia():
    if request.method == "POST":
        tahun_lahir = int(request.form["tahun_lahir"])
        tahun_sekarang = datetime.now().year
        usia = tahun_sekarang - tahun_lahir

        ai_output = ai_call(tahun_lahir)

        return render_template(
            "cek_usia.html", usia=usia, tahun_lahir=tahun_lahir, ai_output=ai_output
        )
    return render_template("cek_usia.html", usia=None)


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=True)
