# 🔋 EnergiMate Ai - Smart Energy Saver Assistant

An AI-based home assistant that monitors appliance usage patterns and suggests ways to reduce electricity consumption, helping you save money and energy.

## 🌟 Features

- **Appliance Monitoring**: Tracks usage patterns for common household appliances with simulated data
- **Smart Suggestions**: Uses rule-based predictions to suggest when to turn devices on/off
- **Energy-Saving Tips**: Provides weekly personalized tips to reduce energy consumption
- **Cost Analysis**: Calculates current costs and estimates potential savings
- **Full-Stack Application**: Modern web interface + RESTful API backend
- **Interactive CLI**: Command-line interface also available

## 📋 Requirements

- Python 3.7 or higher
- Flask 3.0.0+ (for web interface)
- flask-cors 4.0.0+ (for CORS support)

## 🚀 Installation

1. Clone or download this repository
2. Ensure Python 3.7+ is installed on your system
3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## 💻 Usage

### Web Interface (Recommended)

Start the Flask server:

```bash
python app.py
```

Then open your web browser and navigate to:
```
http://localhost:5000
```

The web interface provides:
- **Dashboard**: Overview of energy usage, costs, and active appliances
- **Appliances**: View and control all appliances (turn on/off)
- **Suggestions**: AI-powered energy-saving recommendations
- **Tips**: Weekly energy-saving tips
- **Costs**: Detailed cost breakdown and savings estimates

### Command-Line Interface

Alternatively, you can use the CLI version:

```bash
python main.py
```

### Available CLI Commands

- `status` - View current status of all appliances
- `usage` - View weekly energy usage summary
- `suggestions` - Get AI-powered energy-saving suggestions
- `tips` - View weekly energy-saving tips
- `costs` - View cost breakdown and potential savings
- `turnon <appliance>` - Turn on a specific appliance
- `turnoff <appliance>` - Turn off a specific appliance
- `appliances` - List all available appliances
- `help` - Show the command menu
- `exit` - Exit the application

## 🌐 API Endpoints

The backend provides RESTful API endpoints:

- `GET /api/status` - Get current appliance status
- `GET /api/usage` - Get weekly energy usage summary
- `GET /api/suggestions` - Get energy-saving suggestions
- `GET /api/tips?count=5` - Get weekly energy-saving tips
- `GET /api/costs` - Get cost analysis and savings
- `GET /api/appliances` - List all appliances
- `POST /api/appliances/<name>/turnon` - Turn on an appliance
- `POST /api/appliances/<name>/turnoff` - Turn off an appliance
- `GET /api/daily-usage?days=7` - Get daily usage history

## 🏗️ Project Structure

```
EnergiMate Ai/
├── app.py                  # Flask backend API server
├── main.py                 # CLI interface (alternative)
├── appliances.py           # Appliance monitoring system
├── predictor.py            # Prediction and rules engine
├── tips.py                 # Energy-saving tips system
├── cost_calculator.py      # Cost calculation and savings estimation
├── static/                 # Frontend files
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Modern CSS styling
│   └── app.js              # Frontend JavaScript
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎨 User Interface Features

The web interface includes:
- **Modern Design**: Clean, responsive UI with gradient backgrounds
- **Real-time Updates**: Auto-refreshes every 30 seconds
- **Interactive Controls**: Turn appliances on/off with one click
- **Visual Feedback**: Color-coded status indicators and priority badges
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Toast Notifications**: Real-time feedback for user actions

## 🧠 How It Works

### Appliance Monitoring
- Simulates usage patterns for 10 common household appliances
- Tracks power consumption, usage hours, and on/off status
- Generates weekly usage history with realistic patterns

### Prediction Engine
The system uses rule-based logic to make suggestions:
- **Idle Device Detection**: Identifies devices left on unnecessarily
- **Peak Hour Optimization**: Suggests turning off high-consumption devices during peak hours (5 PM - 9 PM)
- **Off-Peak Scheduling**: Recommends using high-consumption appliances during off-peak hours
- **Usage Pattern Analysis**: Compares current usage against typical patterns

### Energy Tips
- Categorized tips (General, Appliances, Heating/Cooling, Electronics, Seasonal)
- Weekly rotation of tips
- Personalized recommendations based on specific appliances

### Cost Calculation
- Calculates current energy costs based on usage patterns
- Estimates potential savings from following suggestions
- Provides breakdowns by appliance and time period

## 📊 Default Appliances

The system comes pre-configured with these appliances:
- Air Conditioner (3500W)
- Refrigerator (150W)
- Washing Machine (2000W)
- Television (150W)
- LED Lights (50W)
- Laptop (50W)
- Electric Heater (2000W)
- Microwave (1000W)
- Dishwasher (1800W)
- Gaming Console (200W)

## ⚙️ Configuration

You can modify the following in the code:
- **Electricity Rate**: Default is $0.15 per kWh (in `predictor.py` and `cost_calculator.py`)
- **Peak Hours**: Default is 5 PM - 9 PM (in `predictor.py`)
- **Appliances**: Add or modify appliances in `appliances.py`
- **Server Port**: Default is 5000 (in `app.py`)

## 🖥️ Screenshots

The web interface features:
- **Dashboard Tab**: Overview with summary cards, active appliances, and top consumers
- **Appliances Tab**: Complete list with on/off controls
- **Suggestions Tab**: Prioritized recommendations with savings estimates
- **Tips Tab**: Weekly energy-saving tips by category
- **Costs Tab**: Detailed cost analysis and breakdown

## 🎯 Future Enhancements

Potential improvements for the system:
- Real-time data integration from smart home devices
- Machine learning models for better predictions
- Historical data analysis and trends
- Charts and graphs for visualization
- Mobile app version
- Integration with actual smart home APIs
- Weather-based suggestions
- Personalized usage profiles
- User authentication and multiple homes

## 📝 License

This project is created for educational purposes as part of the EEX6340 AI Techniques & Agent Technology course.

## 👨‍💻 Author

Developed as a mini project for Smart Energy Saver scenario.

---

**Stay Energy-Efficient! 🌱**
