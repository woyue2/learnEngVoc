from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def deal_with_text(text):
    text = text.strip()
    pattern = r"\s*/\s*"
    text = re.sub(pattern, "/", text)
    pattern = r"IPA guide"
    text = re.sub(pattern, r"\n\t", text)
    return text

def get_voc_definition(keyword):
    url = f"https://www.vocabulary.com/dictionary/{keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    first_result = soup.find("div", class_="word-area")

    if first_result:
        result_text = deal_with_text(first_result.text)
        return result_text
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def dictionary():
    if request.method == 'POST':
        keyword = request.form['keyword']
        first_result = get_voc_definition(keyword)
        if first_result:
            return render_template('index.html', definition=first_result, keyword=keyword)
        else:
            return render_template('index.html', error="Word not found in the dictionary.", keyword=keyword)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)