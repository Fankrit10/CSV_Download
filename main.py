from flask import Flask, jsonify, request, send_file
import requests
import json
import csv
import pyautogui
import time
import random


pyautogui.FAILSAFE = False

app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get('https://www.gob.ec/api/v1/instituciones?page=0')
    return jsonify(response.text)
    #print(response)
    """with open('datos.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data[0].keys())
        for item in data:
            writer.writerow(item.values())
    return response"""
    #return send_file('datos.csv', mimetype='text/csv', as_attachment=True, attachment_filename='instituciones.csv')


if __name__ == '__main__':  
    while True:
        print("correr")
        time.sleep(15)
        pyautogui.hotkey('tab', 'alt')
        pyautogui.scroll(-1)
        time.sleep(15)
        for i in range (0,10):
            pyautogui.moveTo(0,i*50)
            time.sleep(random.uniform(0.1, 0.5)) # agregar un pequeño retraso aleatorio
            pyautogui.click(button='right')  
            time.sleep(random.uniform(0.1, 0.5)) # agregar un pequeño retraso aleatorio
    app.run(debug=True)