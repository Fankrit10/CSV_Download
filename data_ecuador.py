import io
from flask import Flask, jsonify, make_response, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import json
import io
import csv
import pyautogui
import time
import random
import chardet
import brotli


app = Flask(__name__)

url = 'localhost:5000/data'
headers = {
    'Content-Type': 'application/csv',
    'authority': 'www.gob.ec',
    'method': 'GET',
    'path': '/api/v1/instituciones',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'es-ES,es;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': '_ga=GA1.1.1646576769.1677507212; _gid=GA1.1.1815811788.1677507212',
    'if-none-match': 'W/"1677529641"',
    'referer': 'https://www.gob.ec/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
}
url2 = 'https://compensar-sinconvivencia.infomediaservice.online/typedocuments/api/v1/tiposdedocumento'
url='https://www.gob.ec/api/v1/instituciones'

@app.route('/', methods=['GET', 'POST'])
def scrape_instituciones():
    response = requests.get(url, headers=headers)
    #data = response.json()
    return jsonify(response)

path='./data.json'

@app.route('/data')
def read_tiposdedocumento():
        with open('./data.json', "r") as json_file:
            data = json.load(json_file)
            return jsonify(data)
        
@app.route('/download')
def download():
    filename = 'example.txt'
    return send_file(filename, as_attachment=True)

@app.route('/download2')
def prueba():
    download_data_from_endpoint('https://www.gob.ec/api/v1/instituciones', 'example.txt')
    return "Hecho"

def download_data_from_endpoint(endpoint_url, filename):
    response = requests.get(url, headers=headers)
    datos = response.json()
    print("Datos",datos)

    if response.status_code == 200:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(datos))            
            print(datos)        
            print(f'Se descargaron los datos del endpoint en {filename}')
            return send_file(filename, as_attachment=True)
    else:
        print('No se pudo obtener los datos del endpoint')


@app.route('/download/<path:endpoint_url>/<filename>')
def download_data_from_endpoint(endpoint_url, filename):
    response = requests.get(endpoint_url, headers=headers)
    data = response.json()
    if response.status_code == 200:
        # Verificar que las llaves son columnas
        columns = ['institucion_id', 'institucion', 'siglas', 'logo', 'url', 'website', 'tipo', 'descripcion', 'sector', 'modificado', 'publicado']
        for obj in data:
            # Verificar que todas las llaves son columnas
            if not all(key in columns for key in obj.keys()):
                return 'Las llaves del objeto no son válidas'
        # Generar la respuesta con los datos separados por comas
        response_data = '|'.join([column.encode('utf-8').decode('latin-1') for column in columns]) + '\n'
        for obj in data:
            print(obj)
            row = '|'.join([str(obj.get(column, '').replace('\n', ' ').replace('\t', ' ')) for column in columns])
            response_data += f'{row}\n'
        # Crear una respuesta HTTP con los datos
        response = make_response(response_data)
        # Establecer el tipo de contenido de la respuesta
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        # Establecer el encabezado para descargar el archivo
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return 'No se pudieron obtener los datos del endpoint', 404


if __name__ == '__main__':
    app.run(debug=True)