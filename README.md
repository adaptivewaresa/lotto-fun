### **Predictive Entropic Nexus (PEN) Lotto API**

The **PEN Lotto API** is a Flask-based web application that dynamically generates lotto numbers based on statistical draw frequencies fetched in real-time from an external source. By leveraging techniques like chaos theory, frequency analysis, and balance enforcement, the API provides users with unique and optimized lotto predictions.

---

### **Features**
- **Dynamic Data Fetching**: Scrapes live lotto number frequencies from [National Lottery Hot Numbers](https://za.national-lottery.com/lotto/hot-numbers).
- **Algorithmic Number Selection**:
  - *Lucky Echo Bias*: Prioritizes frequently drawn numbers.
  - *Inverse Fortuna Boost*: Boosts underdog (less frequent) numbers.
  - *Chaos Jitter*: Adds randomization for unpredictability.
  - *Universal Balance Enforcement*: Ensures a balanced final selection.
- **RESTful API**: Exposes an endpoint (`/generate`) for easy integration.

---

### **Project Structure**
```
flask_app/
├── app/
│   ├── __init__.py        # App factory for initializing Flask app
│   ├── routes.py          # API endpoints
│   ├── services.py        # Business logic and scraping functions
│   └── config.py          # Configurations for dev/production
├── tests/
│   ├── test_routes.py     # API endpoint tests
│   └── test_services.py   # Service layer tests
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables
├── .gitignore             # Ignored files for Git
└── run.py                 # Application entry point
```
---

### **Endpoints**
1. **Generate Lotto Numbers**
   - **URL**: `/generate`
   - **Method**: `GET`
   - **Response**:
     ```json
     {
       "numbers": [7, 14, 22, 30, 35, 49],
       "reasons": [
         "Selected most frequently drawn numbers: 7, 22, 49",
         "Boosted least frequently drawn numbers: 14, 35",
         "Generated random chaotic numbers: 30",
         "Enforced universal balance: 7, 14, 22, 30, 35, 49"
       ]
     }
     ```

---

### **Tech Stack**
- **Backend**: Python (Flask)
- **Web Scraping**: BeautifulSoup, Requests
- **Testing**: Unittest
- **Environment Management**: `.env` file for configurations

---
### **License**
This project is licensed under the MIT License. See the LICENSE file for details.
