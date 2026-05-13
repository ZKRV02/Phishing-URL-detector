import streamlit as st
import pandas as pd
import pickle
import re
from whitelist import *

with open('maybefinallysomeimprovement/model.pkl', 'rb') as f:
    model = pickle.load(f)

def is_whitelisted(url):
    for domain in WHITELIST:
        if domain in url:
            return True
    return False

def extract_features(url):
    features = {}
    features['dots'] = url.count('.')
    features['at'] = url.count('@')
    features['equals'] = url.count('=')
    features['slashes'] = url.count('/')
    features['hyphens'] = url.count('-')
    features['digits'] = sum(c.isdigit() for c in url)
    features['is_https'] = 1 if url.startswith('https') else 0
    features['url_length'] = len(url)
    features['is_domain_ip'] = 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0
    
    
    domain = url.split('/')[2] if len(url.split('/')) > 2 else url
    features['subdomains'] = domain.count('.') - 1 if domain.count('.') > 1 else 0
    features['special_chars'] = sum(not c.isalnum() for c in url)
    features['digit_to_length_ratio'] = features['digits'] / len(url) if len(url) > 0 else 0
    
    return pd.DataFrame([features])


st.title("Детектор фишинговых сайтов")
st.write("Введите ссылку ниже, чтобы проверить её на безопасность.")

user_input = st.text_input("URL адрес:", "https://example.com")

if st.button("Проверить"):
    if is_whitelisted(user_input):
        result = "✅ Безопасно (данный сайт находиться в белом списке)"
        st.success(result)
    else:
       data = extract_features(user_input)
    
  
       prediction = model.predict(data)[0]
       probability = model.predict_proba(data) 
    
       if prediction == 1:
           st.error(f"⚠️ Подозрительно! Скорее всего, это фишинг. (Вероятность: {probability[0][1]:.2%})")
       else:
           st.success(f"✅ Безопасно. Модель считает эту ссылку нормальной. (Вероятность: {probability[0][0]:.2%})")

st.info("Модель обучена на 1.2 млн ссылок с точностью ~90%, что не исключает ошибок у модели, проверяйте дополнительно информацию")
