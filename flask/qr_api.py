# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 22:42:51 2024

@author: DELL
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import qrcode
import io
from datetime import datetime

app = Flask("QrApp")
CORS(app)  # CORS'u uygulamaya ekle


def get_login_data():
    """
    Giriş sayfasından gerekli token ve cookie bilgilerini çeker.
    """
    aksis_url = "https://aksis.istanbul.edu.tr/Account/LogOn"
    session = requests.Session()

    # Giriş sayfasına GET isteği gönder
    response = session.get(aksis_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Hidden input içindeki token değerini al
    token = soup.find("input", {"name": "__RequestVerificationToken"})['value']
    cookies = session.cookies.get_dict()

    return token, cookies


@app.route('/login', methods=['POST'])
def login():
    """
    Kullanıcı girişini kontrol eder.
    """
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Giriş için gerekli token ve cookie bilgilerini çek
    token, cookies = get_login_data()

    # Giriş isteği URL'si
    aksis_login_url = "https://aksis.istanbul.edu.tr/Account/LogOn"
    aksis_check_url = "https://aksis.istanbul.edu.tr/Home/Check667ForeignStudent"

    # Header ve Payload bilgileri
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://aksis.istanbul.edu.tr/Account/LogOn",
        "Origin": "https://aksis.istanbul.edu.tr"
    }

    login_payload = {
        "__RequestVerificationToken": token,
        "UserName": username,
        "Password": password,
        "IpAddr": ""
    }

    # Giriş yapma
    try:
        session = requests.Session()
        login_response = session.post(aksis_login_url, headers=headers, data=login_payload, cookies=cookies)
        cookies.update(session.cookies.get_dict())  # Güncellenen cookie bilgileri

        if login_response.status_code == 200:
            # Giriş başarılı ise kullanıcıyı doğrula
            check_response = session.post(aksis_check_url, headers=headers, cookies=cookies)
            print(f"Check Response: {check_response.status_code}, {check_response.text}")

            if check_response.json().get("IsSuccess"):
                return jsonify({"success": True, "message": "Login successful!", "cookies": cookies})
            else:
                return jsonify({"success": False, "message": "Invalid user or not authorized!"}), 401

        else:
            return jsonify({"success": False, "message": "Login failed!"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    """
    Öğrenci bilgilerini alır, ders durumunu kontrol eder,
    ders varsa QR kod oluşturur, aksi halde uyarı döndürür.
    """
    data = request.json
    cookies = data.get("cookies")
    student_id = data.get("student_id")
    birim_id = data.get("birim_id")
    yil = data.get("year", 2024)
    donem = data.get("term", 1)

    # Ders programı URL'si
    schedule_url = f"https://obs.istanbul.edu.tr/OgrenimBilgileri/DersProgramiYeni/Plans_Read?OgrenciId={student_id}&BirimId={birim_id}&Yil={yil}&Donem={donem}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Referer": "https://obs.istanbul.edu.tr/OgrenimBilgileri/DersProgramiYeni/Index",
        "Origin": "https://obs.istanbul.edu.tr",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        # Ders programını çek
        session = requests.Session()
        response = session.post(schedule_url, headers=headers, cookies=cookies)

        if response.status_code == 200:
            schedule_data = response.json()

            # Ders kontrolü
            current_lesson = None
            for event in schedule_data.get("Data", []):
                start = event.get("start")
                end = event.get("end")
                lesson_name = event.get("DersAdi")

                # Başlangıç ve bitiş saatlerini kontrol et
                if is_current_time_in_range(start, end):
                    current_lesson = lesson_name
                    break

            if current_lesson:
                # Ders varsa QR kod oluştur
                name = data.get("name")
                surname = data.get("surname")

                qr_content = f"Name: {name}, Surname: {surname}, ID: {student_id}, Lesson: {current_lesson}"
                qr = qrcode.make(qr_content)

                # Görseli bellekte sakla
                buffer = io.BytesIO()
                qr.save(buffer, format="PNG")
                buffer.seek(0)

                # QR kodu döndür
                return send_file(buffer, mimetype='image/png')
            else:
                # Ders yoksa uyarı döndür
                return jsonify({"success": False, "message": "Şu an dersiniz yok."})

        else:
            return jsonify({"success": False, "message": "Ders programını çekerken hata oluştu."}), 500

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


def is_current_time_in_range(start_time, end_time):
    """
    Şu anki saatin verilen zaman aralığında olup olmadığını kontrol eder.
    """
    try:
        now = datetime.now()
        start = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        end = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")

        return start <= now <= end
    except Exception as e:
        print(f"Time parsing error: {e}")
        return False


if __name__ == '__main__':
    app.run(debug=True)

