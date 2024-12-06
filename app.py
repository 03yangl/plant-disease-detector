from flask import Flask, request, jsonify, make_response
from datetime import datetime
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import base64
import traceback
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
SUPERVISOR_EMAIL = os.getenv('SUPERVISOR_EMAIL')
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Plant Disease Detection System')
PLANT_ID_API_KEY = os.getenv('PLANT_ID_API_KEY')
CONFIDENCE_THRESHOLD = 0.85

def analyze_plant_disease(image_data):
    try:
        # Remove data URL prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        # Prepare the data for the Plant.id API
        data = {
            'api_key': PLANT_ID_API_KEY,
            'images': [image_data],
            'modifiers': ["disease"],
            'plant_language': 'en',
            'disease_details': ["description", "treatment"]
        }

        print("Making request to Plant.id API...")
        response = requests.post(
            'https://api.plant.id/v2/health_assessment',
            json=data
        )

        if response.status_code != 200:
            raise Exception(f"Plant.id API error: {response.text}")

        result = response.json()
        print("Plant.id API Response:", result)

        health_assessment = result.get('health_assessment', {})
        is_healthy = health_assessment.get('is_healthy', True)
        diseases = health_assessment.get('diseases', [])

        if not is_healthy and diseases:
            # Get the most probable disease
            top_disease = diseases[0]
            probability = top_disease.get('probability', 0)

            print(f"Detected disease: {top_disease.get('name')} with probability: {probability}")

            # Only consider it diseased if probability is above threshold
            if probability >= CONFIDENCE_THRESHOLD:
                return {
                    'isDiseased': True,
                    'disease': top_disease.get('name', 'Unknown Disease'),
                    'confidence': probability,
                    'description': top_disease.get('disease_details', {}).get('description', ''),
                    'treatment': top_disease.get('disease_details', {}).get('treatment', ''),
                    'debug_info': {'raw_probability': probability}
                }
            else:
                print(f"Disease detected but confidence ({probability}) below threshold ({CONFIDENCE_THRESHOLD})")

        # If healthy or confidence below threshold, return healthy status
        return {
            'isDiseased': False,
            'disease': 'Plant appears healthy',
            'confidence': 1.0,
            'description': 'No significant disease symptoms detected or confidence level too low.',
            'treatment': 'No treatment needed at this time.',
            'debug_info': {'is_healthy': is_healthy}
        }

    except Exception as e:
        print(f"Error in disease detection: {str(e)}")
        raise

def send_email_alert(image_data, location, disease_info):
    try:
        if not all([GMAIL_USER, GMAIL_APP_PASSWORD, SUPERVISOR_EMAIL]):
            raise ValueError("Missing email configuration. Check your .env file.")

        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = SUPERVISOR_EMAIL
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg['Subject'] = f'Plant Disease Alert - {timestamp}'

        html_content = f"""
            <html>
            <body>
                <h2>{COMPANY_NAME} - Disease Detection Report</h2>
                <p><strong>Time:</strong> {timestamp}</p>
                <p><strong>Location:</strong> {location['latitude']}, {location['longitude']}</p>
                <p><strong>Disease:</strong> {disease_info['disease']}</p>
                <p><strong>Confidence:</strong> {disease_info['confidence']*100:.1f}%</p>
                <p><strong>Description:</strong> {disease_info.get('description', 'N/A')}</p>
                <p><strong>Recommended Treatment:</strong> {disease_info.get('treatment', 'N/A')}</p>
                <p><strong>Google Maps Link:</strong> 
                    <a href="https://www.google.com/maps?q={location['latitude']},{location['longitude']}">
                        View Location
                    </a>
                </p>
            </body>
            </html>
        """
        
        msg.attach(MIMEText(html_content, 'html'))

        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = MIMEImage(image_bytes)
        image.add_header('Content-Disposition', 'attachment', 
                        filename=f'plant-disease-{timestamp}.jpg')
        msg.attach(image)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        return True

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        print(traceback.format_exc())
        raise

@app.route('/api/report-disease', methods=['POST', 'OPTIONS'])
def report_disease():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        data = request.json
        
        image_data = data.get('image')
        location = data.get('location')
        
        if not all([image_data, location]):
            missing_fields = []
            if not image_data: missing_fields.append('image')
            if not location: missing_fields.append('location')
            
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
            print(error_message)
            
            response = jsonify({
                'success': False,
                'message': error_message
            })
            response.status_code = 400
        else:
            try:
                # Analyze the plant using Plant.id API
                disease_info = analyze_plant_disease(image_data)
                
                # Only send email if plant is diseased
                if disease_info['isDiseased']:
                    send_email_alert(image_data, location, disease_info)
                    message = 'Disease detected and report sent'
                else:
                    message = 'Plant appears healthy, no alert needed'
                
                response = jsonify({
                    'success': True,
                    'message': message,
                    'disease_info': disease_info
                })
                response.status_code = 200
                
            except Exception as e:
                error_message = str(e)
                print(f"Error processing request: {error_message}")
                response = jsonify({
                    'success': False,
                    'message': f'Error: {error_message}'
                })
                response.status_code = 500

    except Exception as e:
        error_message = str(e)
        print(f"Error processing request: {error_message}")
        print(traceback.format_exc())
        response = jsonify({
            'success': False,
            'message': f'Error processing request: {error_message}'
        })
        response.status_code = 500

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    # Verify environment variables at startup
    print("Checking environment variables...")
    missing_vars = []
    if not GMAIL_USER: missing_vars.append('GMAIL_USER')
    if not GMAIL_APP_PASSWORD: missing_vars.append('GMAIL_APP_PASSWORD')
    if not SUPERVISOR_EMAIL: missing_vars.append('SUPERVISOR_EMAIL')
    if not PLANT_ID_API_KEY: missing_vars.append('PLANT_ID_API_KEY')
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
    else:
        print("Environment variables loaded successfully")
        print(f"Confidence threshold set to: {CONFIDENCE_THRESHOLD*100}%")

    # Use port 5000 explicitly
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)