# API Keys Required

The following API keys are needed for the updated system. Add them to your `.env` file:

## Required API Keys

### 1. Gemini API Key (Required for LLM)
**Purpose**: Replaces Fireworks/Llama for AI-powered financial analysis

**How to get it**:
1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

**Add to .env**:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Optional**: Specify a different Gemini model
```
GEMINI_MODEL=gemini-pro
```

---

### 2. Fastino API Key (Required for User Profiles)
**Purpose**: Replaces MongoDB for storing user profiles, portfolios, and goals

**How to get it**:
1. Sign up at https://fastino.com (or your Fastino provider)
2. Navigate to API settings
3. Generate a new API key
4. Copy the API key

**Add to .env**:
```
FASTINO_API_KEY=your_fastino_api_key_here
```

**Optional**: Custom Fastino endpoint (if using a different provider)
```
FASTINO_BASE_URL=https://api.fastino.com/v1
```

---

### 3. Linkup API Key (Required for Web Searching)
**Purpose**: Enables web searching for investment strategies and market information

**How to get it**:
1. Sign up at https://linkup.com (or your Linkup provider)
2. Navigate to API settings
3. Generate a new API key
4. Copy the API key

**Add to .env**:
```
LINKUP_API_KEY=your_linkup_api_key_here
```

**Optional**: Custom Linkup endpoint (if using a different provider)
```
LINKUP_BASE_URL=https://api.linkup.com/v1
```

---

## Example .env File

```env
# Required - Gemini for AI
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Required - Fastino for user profiles
FASTINO_API_KEY=fastino_XXXXXXXXXXXXXXXXXXXXXXXX

# Required - Linkup for web searching
LINKUP_API_KEY=linkup_XXXXXXXXXXXXXXXXXXXXXXXX

# Optional - Custom endpoints
# GEMINI_MODEL=gemini-pro
# FASTINO_BASE_URL=https://api.fastino.com/v1
# LINKUP_BASE_URL=https://api.linkup.com/v1

# Legacy (optional - for backwards compatibility)
# FIREWORKS_API_KEY=your_old_key
# VOYAGE_API_KEY=your_old_key
# MONGODB_URL=your_old_connection_string
```

---

## Migration Notes

- **Gemini** replaces Fireworks/Llama for all LLM operations
- **Fastino** replaces MongoDB for user profile storage (MongoDB still works as fallback)
- **Linkup** is new and enables real-time web searching for investment strategies

The system will automatically use Fastino if available, and fall back to MongoDB if Fastino is not configured.

---

## Testing Your API Keys

After adding the keys to your `.env` file, you can test them:

```bash
# Test Gemini
python3 -c "from gemini_client import get_gemini_client; print('Gemini OK')"

# Test Fastino
python3 -c "from fastino_client import get_fastino_manager; print('Fastino OK')"

# Test Linkup
python3 -c "from linkup_client import get_linkup_search_client; print('Linkup OK')"
```

---

## Need Help?

If you encounter issues:
1. Verify the API keys are correct (no extra spaces, quotes, etc.)
2. Check that you have sufficient credits/quota for each service
3. Ensure the base URLs are correct if using custom endpoints
4. Check the terminal output for specific error messages

