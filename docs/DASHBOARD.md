# HTML Dashboard

The iRacing Telemetry API now includes a web-based dashboard for viewing telemetry data in your browser.

## Accessing the Dashboard

Once the server is running, open your browser and navigate to:

```
http://localhost:9000/dashboard
```

## Features

### 📊 Real-time Data Display

The dashboard shows:

- **Driver Information**
  - Name
  - Car Number
  - License Class
  - iRating

- **Session Statistics**
  - Driver Incidents
  - Team Incidents
  - Laps Completed
  - Total Laps

- **Camera Information**
  - Current Camera
  - Camera Target

### 🔄 Auto-Refresh

When connected to iRacing, the dashboard automatically refreshes every 5 seconds to show the latest data.

### 🎨 Modern UI

- Responsive design that works on desktop and mobile
- Beautiful gradient background
- Card-based layout
- Color-coded connection status
- Manual refresh button

## Connection States

### ✅ Connected to iRacing
- Status badge shows green "Connected"
- All telemetry data is displayed
- Page auto-refreshes every 5 seconds

### ❌ Not Connected to iRacing
- Status badge shows red "Not Connected"
- All fields show "N/A"
- No auto-refresh (prevents unnecessary requests)

## Testing the Dashboard

You can test the dashboard with this curl command:

```bash
curl http://localhost:9000/dashboard
```

Or simply open it in your browser for the full interactive experience.

## Customization

The dashboard is located in `src/server/dashboard.py`. You can customize:

- **Styling**: Modify the CSS in the `<style>` section
- **Data Fields**: Add or remove data rows in the HTML
- **Auto-refresh Rate**: Change the timeout value (currently 5000ms)
- **Layout**: Adjust the grid layout or add new cards

### Example: Adding a New Data Field

```python
# In the HTML section, add a new data row:
<div class="data-row">
    <span class="data-label">Your Label:</span>
    <span class="data-value">{your_variable}</span>
</div>
```

### Example: Changing Auto-Refresh Rate

```python
# Change from 5 seconds to 10 seconds:
setTimeout(() => location.reload(), 10000);
```

## API Endpoints

The dashboard complements the existing JSON API endpoints:

| Endpoint | Type | Description |
|----------|------|-------------|
| `/` | JSON | API information |
| `/dashboard` | HTML | Interactive dashboard |
| `/api/driver` | JSON | Driver data |
| `/api/camera` | JSON | Camera info |

## Screenshots

The dashboard features:
- Purple gradient background
- White cards with rounded corners
- Color-coded status indicators
- Responsive grid layout
- Clean, modern typography

## Browser Compatibility

The dashboard works in all modern browsers:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Opera

## Mobile Support

The dashboard is fully responsive and works on mobile devices. The grid layout automatically adjusts to smaller screens.

