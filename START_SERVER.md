# How to Start the Server

## The server is NOT running yet. Follow these steps:

### Step 1: Open a Terminal

Open Terminal (or your preferred terminal application) and navigate to the project directory:
```bash
cd /Users/prabhavgoel/Documents/GitHub/mongodb-hacks
```

### Step 2: Activate Virtual Environment

```bash
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

### Step 3: Start the Server

**Option A: Using the startup script**
```bash
./start_server.sh
```

**Option B: Manual start**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Wait for Server to Start

You should see output like this:
```
INFO:     Will watch for changes in these directories: ['/Users/prabhavgoel/Documents/GitHub/mongodb-hacks']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 5: Open Your Browser

Once you see "Application startup complete", open your browser and go to:
- **http://localhost:8000** or
- **http://127.0.0.1:8000**

## Important Notes

1. **Keep the terminal open** - The server runs in the terminal. If you close it, the server stops.

2. **To stop the server** - Press `Ctrl+C` in the terminal where it's running.

3. **If you see errors** - Check that:
   - You activated the virtual environment (`source venv/bin/activate`)
   - Your `.env` file exists (though the server should start even without it)
   - Port 8000 is not already in use

4. **Port already in use?** - Use a different port:
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8001
   ```

## Quick Test

To verify everything is set up correctly, run:
```bash
source venv/bin/activate
python3 -c "from api import app; print('✓ Server can start!')"
```

If you see the checkmark, you're ready to start the server!

