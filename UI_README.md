# Financial Advisory System - Web UI

A modern, user-friendly web interface for the Financial Advisory System that allows users to input their investment preferences and receive AI-generated investment strategies.

## Features

- **Comprehensive Form**: Input personal profile, portfolio details, tax information, and financial goals
- **Real-time Analysis**: Submit your information and receive a detailed investment strategy
- **Modern UI/UX**: Beautiful, responsive design with smooth animations
- **Detailed Results**: View comprehensive analysis including:
  - Risk Assessment
  - Portfolio Analysis
  - Tax Optimization Opportunities
  - Market Research & Trends
  - Financial Planning
  - Compliance Review

## Running the Application

### Prerequisites

1. Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure your `.env` file is configured with:
   - `FIREWORKS_API_KEY`
   - `VOYAGE_API_KEY`
   - `MONGODB_URL`

### Starting the Server

1. Start the FastAPI server:
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8000
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

### Using the Interface

1. **Fill in Personal Profile**:
   - User ID (unique identifier)
   - Name, Age, Annual Income
   - Risk Tolerance (Conservative, Moderate, or Aggressive)
   - Investment Timeline

2. **Enter Portfolio Information**:
   - Total Portfolio Value
   - Current Holdings (Stocks, Bonds, Cash, Crypto, etc.)
   - Risk Score (optional)

3. **Add Tax Information** (optional):
   - Tax Bracket
   - State
   - Filing Status

4. **Set Financial Goals**:
   - Add one or more financial goals
   - Specify target amount, timeline, and priority
   - Click "+ Add Another Goal" to add more

5. **Generate Strategy**:
   - Click "Generate Investment Strategy"
   - Wait for the analysis to complete (this may take 30-60 seconds)
   - Review your personalized investment strategy

## File Structure

```
static/
├── index.html      # Main HTML page with form
├── styles.css      # Modern CSS styling
└── script.js       # JavaScript for form handling and API calls
```

## API Endpoint

The UI communicates with the backend via:
- **POST** `/api/analyze` - Submits client data and returns analysis results

## Notes

- The analysis process may take 30-60 seconds as it runs through multiple AI agents
- All data is processed securely and stored in MongoDB for future reference
- Results are formatted for easy reading with proper sections and styling
- The interface is fully responsive and works on desktop and mobile devices

## Troubleshooting

### Server Won't Start

1. **Check if dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the test script:**
   ```bash
   python3 test_server.py
   ```

3. **Check if port 8000 is already in use:**
   ```bash
   lsof -i :8000
   ```
   If something is using port 8000, either stop it or use a different port:
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8001
   ```

### Page Won't Load

1. **Check server is running:**
   - Look for "Uvicorn running on http://0.0.0.0:8000" in terminal
   - Try accessing http://127.0.0.1:8000 instead of localhost

2. **Check browser console:**
   - Press F12 to open developer tools
   - Look for errors in the Console tab
   - Check Network tab for failed requests

3. **Verify static files:**
   ```bash
   ls -la static/
   ```
   Should show: index.html, styles.css, script.js

### API Errors

1. **Check MongoDB connection:**
   - Ensure MongoDB is running
   - Verify MONGODB_URL in `.env` is correct

2. **Check API keys:**
   - Verify FIREWORKS_API_KEY and VOYAGE_API_KEY in `.env`
   - Keys should not have quotes around them

3. **Check server logs:**
   - Look at the terminal where uvicorn is running
   - Errors will show the full traceback

### Common Issues

- **ModuleNotFoundError**: Run `pip install -r requirements.txt`
- **Port already in use**: Use `--port 8001` or kill the process using port 8000
- **Static files not found**: Ensure `static/` directory exists with all three files
- **CORS errors**: Should be fixed with the CORS middleware, but check browser console

