# Plant Disease Detection System

A web application that captures plant images, detects diseases using the Plant.id API, and sends email notifications to supervisors when diseases are detected with high confidence.

## Features

- Camera capture interface
- Location detection
- Plant disease detection using Plant.id API
- Email notifications for diseased plants
- Confidence threshold filtering (85%)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/plant-disease-detector.git
cd plant-disease-detector
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file with your credentials:
```
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
SUPERVISOR_EMAIL=supervisor@company.com
COMPANY_NAME=Your Company Name
PLANT_ID_API_KEY=your-plant-id-api-key
FLASK_DEBUG=True
PORT=5000
```

5. Run the application:
```bash
python app.py
```

6. Open `index.html` in your web browser

## Configuration

- CONFIDENCE_THRESHOLD: Set to 0.85 (85%) for disease detection
- Plant.id API settings can be modified in the `analyze_plant_disease` function
- Email template can be customized in the `send_email_alert` function

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.