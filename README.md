# Mental Health Trend Analyzer

A comprehensive mental health sentiment analysis platform that converts raw text and unstructured social media feeds into standard sentiment vectors using local linguistic models.

## Features

- **Text Analysis Engine**: Process raw text and social media feeds for sentiment analysis
- **Real-time Analytics Dashboard**: View sentiment distributions and mental health trends
- **Risk Assessment**: Categorize content by mental health risk levels (Low, Moderate, High)
- **PDF Report Generation**: Export analytical reports in PDF format
- **Secure Authentication**: User-based authentication and session management
- **Historical Trend Tracking**: Analyze patterns over time

## Tech Stack

### Backend
- **Flask** - Python web framework
- **SQLite3** - Database
- **TextBlob & NLTK** - Natural Language Processing
- **ReportLab** - PDF Generation
- **Scikit-learn** - Machine Learning

### Frontend
- **HTML5** - Markup
- **Vanilla JavaScript** - Interactive features
- **Chart.js** - Data visualization
- **CSS3** - Glassmorphism UI design

## Project Structure

```
Mental-health-trend-Analyzer/
├── backend/
│   ├── app.py              # Flask application
│   ├── database.py         # Database models
│   ├── models.py           # NLP models
│   ├── utils.py            # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── venv/               # Virtual environment
├── frontend/
│   ├── index.html          # Home page
│   ├── dashboard.html      # Analytics dashboard
│   ├── analyzer.html       # Sentiment analyzer
│   ├── trends.html         # Trend visualization
│   ├── login.html          # Authentication
│   ├── about.html          # System info
│   ├── contact.html        # Contact form
│   ├── static/
│   │   ├── css/            # Stylesheets
│   │   └── js/             # JavaScript files
│   └── reports/            # Generated PDF reports
└── README.md
```

## Installation

### Backend Setup

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

The Flask server will run on `http://127.0.0.1:5000`

### Frontend Setup

You can use Live Server or any HTTP server:

```bash
# Using VS Code Live Server extension
# Open frontend/index.html and click "Go Live"
```

Frontend will run on `http://127.0.0.1:5500`

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Analytics
- `GET /api/dashboard-stats` - Get dashboard metrics
- `POST /api/analyze` - Analyze sentiment of text
- `GET /api/trends` - Get historical trends
- `GET /api/user/<user_id>/report/pdf` - Generate PDF report

### Health Check
- `GET /api/health-check` - Server status

## Usage

1. **Register/Login** - Create account or login with credentials
2. **Analyze Text** - Input text or social media content for analysis
3. **View Dashboard** - Check sentiment distributions and risk levels
4. **Download Reports** - Generate PDF reports with detailed analytics
5. **Track Trends** - Monitor historical patterns and changes

## Key Features Explained

### Sentiment Analysis
- Converts text into sentiment vectors
- Categories: Positive, Negative, Neutral
- Confidence scoring

### Risk Assessment
- Low Risk: Positive mental state
- Moderate Risk: Some concerns present
- High Risk: Significant mental health concerns

### Dashboard Metrics
- Total logs processed
- Prevailing risk factor
- Positive ratio density
- Sentiment proportions chart
- Mental health threat categorization

## Database Schema

### Users Table
- id (PRIMARY KEY)
- username (TEXT, UNIQUE)
- email (TEXT, UNIQUE)
- password (TEXT - hashed)
- created_at (TIMESTAMP)

### Analyses Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- text_content (TEXT)
- sentiment (TEXT: positive, negative, neutral)
- emotion (TEXT)
- risk_level (TEXT: low_risk, mod_risk, high_risk)
- confidence (FLOAT)
- created_at (TIMESTAMP)

## Security Features

- SHA256 password hashing
- JWT-based session tokens
- CORS enabled for secure API communication
- Local sandbox execution environment

## Future Enhancements

- Advanced NLP models (BERT, GPT-based)
- Real-time streaming analysis
- Multi-language support
- Advanced visualizations
- Mobile application
- Cloud deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Commit with descriptive messages
5. Push to the branch
6. Create a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please contact:
- Email: support@mentalhealth-trend-analyzer.com
- GitHub Issues: [Report an issue](https://github.com/HARINARAYAN-2027/Mental-health-trend-Analyzer/issues)

---

**Built with ❤️ for mental health awareness**
