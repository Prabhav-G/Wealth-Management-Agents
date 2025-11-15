# Quick Start Guide

## Starting the Server

### Method 1: Using the Startup Script (Recommended)
```bash
./start_server.sh
```

### Method 2: Manual Start
```bash
# Activate virtual environment
source venv/bin/activate

# Start the server
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## Accessing the Web Interface

Once the server is running, open your browser and go to:
- **http://localhost:8000** or
- **http://127.0.0.1:8000**

## Important Notes

1. **Virtual Environment**: Always activate the virtual environment first:
   ```bash
   source venv/bin/activate
   ```

2. **Port Already in Use**: If port 8000 is busy, use a different port:
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8001
   ```

3. **Environment Variables**: Make sure your `.env` file has:
   - `FIREWORKS_API_KEY=your_key_here`
   - `VOYAGE_API_KEY=your_key_here`
   - `MONGODB_URL=your_mongodb_connection_string`

4. **MongoDB**: The server will start even if MongoDB isn't configured, but you'll need it for the analysis to work.

## Troubleshooting

If you see "Safari Can't Open the Page" or connection errors:

1. **Check if server is running**: Look for "Uvicorn running on..." in terminal
2. **Check port**: Make sure nothing else is using port 8000
3. **Try 127.0.0.1**: Use `http://127.0.0.1:8000` instead of `localhost:8000`
4. **Check browser console**: Press F12 to see any JavaScript errors

