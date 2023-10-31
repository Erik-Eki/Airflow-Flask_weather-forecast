from flask import render_template, jsonify
import requests
from app import app


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/dag-test', methods=['GET'])
def dag_test():
    # print("REQ:", request)
    # dag_data = request.get_json()

    # Process the DAG data
    # return jsonify(dag_data), 200
    return jsonify({'message': 'Hello, Airflow!'})

@app.route('/weather', methods=['GET'])
def weather():
    api_key = "3620323dabe54a0abb6165945233110"
    location = "kajaani"
    # http://api.weatherapi.com/v1/current.json?key=3620323dabe54a0abb6165945233110&q=kajaani,fi
    # Fetch weather data from a weather API
    response = requests.get(f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location},fi')
    data = response.json()
    
    print("##########", data)

    # Extract relevant data and return it
    current = data['current']
    return jsonify({
        'temperature': current['temp_c'],
        'humidity': current['humidity'],
        'condition': current['condition']['text'],
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)