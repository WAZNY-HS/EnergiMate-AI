# Appendix: Code Structure and Key Components

## Project File Structure

```
EnergiMate Ai/
├── app.py                      # Flask backend API server
├── main.py                     # CLI interface
├── appliances.py               # Appliance monitoring system
├── predictor.py                # Prediction and rules engine
├── tips.py                     # Energy-saving tips system
├── cost_calculator.py          # Cost calculation module
├── requirements.txt            # Python dependencies
├── static/                     # Frontend files
│   ├── index.html              # Main HTML page
│   ├── styles.css              # CSS styling
│   └── app.js                  # Frontend JavaScript
├── start_server.bat            # Windows startup script
├── start_server.sh             # Linux/Mac startup script
└── README.md                   # Project documentation
```

## Key Code Components

### 1. Appliance Monitoring (`appliances.py`)

**Main Classes:**
- `Appliance`: Data class representing an appliance
- `ApplianceMonitor`: Monitors and simulates appliance usage

**Key Methods:**
```python
simulate_daily_usage(days: int) -> List[Dict]
get_weekly_summary() -> Dict
get_current_status() -> Dict
turn_on(name: str) -> bool
turn_off(name: str) -> bool
```

### 2. Prediction Engine (`predictor.py`)

**Main Class:**
- `EnergyPredictor`: Rule-based prediction system

**Key Methods:**
```python
suggest_device_actions() -> List[Dict]
is_peak_hour(current_time) -> bool
predict_weekly_savings() -> Dict
_calculate_savings(appliance, action, hours, peak_multiplier) -> Dict
```

**Rules Implemented:**
1. Excessive usage detection
2. Peak hour optimization
3. Off-peak scheduling
4. Idle device detection

### 3. Tips System (`tips.py`)

**Main Class:**
- `EnergyTips`: Energy-saving tips provider

**Key Methods:**
```python
get_weekly_tips(count: int) -> List[Dict]
get_tips_by_category(category: str) -> List[str]
get_personalized_tip(appliance_name: str) -> str
```

### 4. Cost Calculator (`cost_calculator.py`)

**Main Class:**
- `CostCalculator`: Cost analysis and savings estimation

**Key Methods:**
```python
calculate_current_costs() -> Dict
estimate_savings_from_suggestions() -> Dict
get_cost_breakdown_by_appliance() -> List[Dict]
project_future_savings(months: int) -> Dict
```

### 5. Backend API (`app.py`)

**API Endpoints:**
- `GET /` - Serve web interface
- `GET /api/status` - Get appliance status
- `GET /api/usage` - Get weekly usage summary
- `GET /api/suggestions` - Get energy-saving suggestions
- `GET /api/tips` - Get weekly tips
- `GET /api/costs` - Get cost analysis
- `GET /api/appliances` - List all appliances
- `POST /api/appliances/<name>/turnon` - Turn on appliance
- `POST /api/appliances/<name>/turnoff` - Turn off appliance
- `GET /api/daily-usage` - Get daily usage history

### 6. Frontend (`static/`)

**Files:**
- `index.html`: Main HTML structure with 5 tabs
- `styles.css`: Modern CSS with responsive design
- `app.js`: JavaScript for API communication and UI updates

**Key Functions:**
- `loadDashboard()` - Load dashboard data
- `loadAppliances()` - Load and display appliances
- `loadSuggestions()` - Display AI suggestions
- `loadTips()` - Display weekly tips
- `loadCosts()` - Display cost analysis
- `turnOnAppliance(name)` - Control appliance
- `turnOffAppliance(name)` - Control appliance

## Data Flow

1. **User Request** → Frontend (HTML/JS)
2. **API Call** → Flask Backend (`app.py`)
3. **Business Logic** → Core Modules (appliances, predictor, tips, calculator)
4. **Data Processing** → Simulated data generation and analysis
5. **Response** → JSON data returned to frontend
6. **Display** → User sees results in web interface

## Configuration

**Default Settings:**
- Electricity Rate: $0.15 per kWh
- Peak Hours: 5 PM - 9 PM
- Number of Appliances: 10
- Weekly Tips: 5 tips per week
- Auto-refresh: Every 30 seconds

**Customization:**
All configuration values can be modified in the respective Python files.

