# Plant Disease Detection System

A web application that captures plant images, detects diseases using the Plant.id API, and sends email notifications to supervisors when diseases are detected with high confidence (>=85%).

## Features

- Camera capture for plant images
- Automatic location detection
- Plant disease detection using Plant.id API
- Email notifications with detailed reports
- Confidence threshold filtering (85%)
- Local timezone support for timestamps

## Live Demo
[https://plant-disease-report.netlify.app](https://plant-disease-report.netlify.app)

## Technologies Used

- Frontend:
  - HTML/CSS/JavaScript
  - jQuery
  - Deployed on Netlify
- Backend:
  - Python/Flask
  - Plant.id API
  - Gmail SMTP
  - Deployed on Render

## Setup

### Prerequisites

- Python 3.9+
- Gmail account with App Password enabled
- Plant.id API key
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/plant-disease-detector.git
cd plant-disease-detector
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a .env file in the root directory:
```env
GMAIL_USER=your.email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
SUPERVISOR_EMAIL=supervisor@company.com
COMPANY_NAME=Your Company Name
PLANT_ID_API_KEY=your-plant-id-api-key
FLASK_DEBUG=True
PORT=5000
```

### Deployment

#### Backend (Render)
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables in Render dashboard
4. Deploy

#### Frontend (Netlify)
1. Create a new site on Netlify
2. Connect your GitHub repository
3. Configure build settings:
   - Base directory: (leave blank)
   - Build command: (leave blank)
   - Publish directory: frontend
4. Deploy

## Usage

1. Open the web application
2. Allow camera and location access
3. Take a picture of the plant
4. Wait for analysis
5. If a disease is detected with >85% confidence:
   - Supervisor receives email with:
     - Plant image
     - Disease details
     - Location information
     - Treatment recommendations

## Configuration

- CONFIDENCE_THRESHOLD: Set to 0.85 (85%) for disease detection
- Timezone: Currently set to 'America/New_York' (modify in app.py)
- CORS: Update ALLOWED_ORIGINS in app.py with your domains

## Development

To run locally:

1. Start the Flask backend:
```bash
python app.py
```

2. Open frontend/index.html in a browser

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- Plant.id API for plant disease detection
- Netlify for frontend hosting
- Render for backend hosting