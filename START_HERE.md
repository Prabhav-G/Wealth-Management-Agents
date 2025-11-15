# 🚀 START HERE - Quick Server Start Guide

## ✅ The server is now ready to start!

The API has been fixed to start even without MongoDB configured. You can now start the server and access the web interface.

## Step-by-Step Instructions

### 1. Open Terminal
Open Terminal (or your terminal application)

### 2. Navigate to Project Directory
```bash
cd /Users/prabhavgoel/Documents/GitHub/mongodb-hacks
```

### 3. Activate Virtual Environment
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 4. Start the Server

**Easiest way:**
```bash
./start_server.sh
```

**Or manually:**
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 5. Wait for This Message
You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### 6. Open Your Browser
Go to: **http://localhost:8000** or **http://127.0.0.1:8000**

## ✅ Success!

You should now see the Financial Advisory System web interface with the form to input your investment preferences.

## ⚠️ Important Notes

1. **Keep the terminal open** - The server runs in the terminal. Closing it stops the server.

2. **MongoDB Configuration** - The server will start without MongoDB, but you'll need it configured in your `.env` file to actually run financial analyses. The web interface will load and show the form, but submitting will require MongoDB.

3. **To stop the server** - Press `Ctrl+C` in the terminal.

4. **Port already in use?** - Use port 8001:
   ```bash
   uvicorn api:app --reload --host 0.0.0.0 --port 8001
   ```

## 🐛 Still Having Issues?

If you still see connection errors:
1. Make sure you see "Application startup complete" in the terminal
2. Try `http://127.0.0.1:8000` instead of `localhost:8000`
3. Check that nothing else is using port 8000: `lsof -i :8000`
4. Check browser console (F12) for any errors

