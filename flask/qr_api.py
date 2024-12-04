# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 22:42:51 2024

@author: DELL
"""

from flask import Flask, request, send_file
from flask_cors import CORS
import qrcode
import io

app = Flask("QrApp")
CORS(app)  # CORS'u uygulamaya ekle

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    """
    Öğrenci bilgilerini alır, QR kod oluşturur ve görsel olarak döndürür.
    """

    # Web sitesinden gelen JSON verisini alıyoruz
    data = request.json

    # JSON içinden bilgileri alıyoruz
    name = data.get("name")
    surname = data.get("surname")
    student_id = data.get("student_id")

    # QR kod içeriği
    qr_content = f"Name: {name}, Surname: {surname}, ID: {student_id}"

    # QR kod oluşturma
    qr = qrcode.make(qr_content)

    # Görseli bellekte sakla
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    # Görseli direkt döndür
    return send_file(buffer, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

