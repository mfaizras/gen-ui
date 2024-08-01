# <center>GENUI</center>
# Tentang
Aplikasi ini merupakan sebuah interface untuk beberapa model LLM, tujuannya adalah membuat model LLM menjadi <b>Pay as You go</b>. Jadi tidak perlu menghabiskan rata-rata 20$ perbulan untuk ChatGPT pro atau Claude Pro tapi hanya kita pakai beberapa kali saja yang seharusnya tidak sampai value 20$
# Cara menjalankan Program
## Buat Virtual environment
```
python -m venv genai
```
### Aktifkan Virtual environment
#### Pada windows :
```
/genai/Scripts/activate
```
#### Pada linux/mac :
```
source ./genai/bin/activate
```
## Jalankan Program

 1. Instal Requirements

```
pip install -r requirement.txt
```

 2. Jalankan Streamlit
```
streamlit run app.py
```