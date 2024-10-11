from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from data_analysis import perform_soil_moisture_analysis

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/soil-analysis')
def soil_analysis():
    return render_template('soil-analysis.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        crop_name = request.form.get('crop_name').strip()
        crop_age = int(request.form.get('crop_age'))
        soil_type = request.form.get('soil_type').strip()

        result = perform_soil_moisture_analysis(crop_name, soil_type, latitude, longitude, crop_age)
        return render_template('result.html', message=result)

    except ValueError:
        return render_template('result.html', message="Error: Please ensure all inputs are valid.")
    except Exception as e:
        return render_template('result.html', message=f"An unexpected error occurred: {str(e)}")

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

# Add these new routes
@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/references')
def references():
    return render_template('references.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)