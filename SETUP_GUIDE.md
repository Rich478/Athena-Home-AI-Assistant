# Setup Guide for Athena AI Family Life Planning Assistant

## Getting Started with Web Search

To enable Athena's web search capabilities, you'll need to get a free Tavily API key.

### Step 1: Get Your Tavily API Key

1. **Visit Tavily**: Go to [https://tavily.com/](https://tavily.com/)
2. **Sign Up**: Click "Get Started" or "Sign Up" for a free account
3. **Get API Key**: After signing up, you'll receive a free API key
4. **Copy the Key**: Copy your API key (it starts with `tvly-`)

### Step 2: Add the API Key to Your Environment

1. **Open your `.env` file** in the project root
2. **Add the Tavily API key**:
   ```
   TAVILY_API_KEY=tvly-your-actual-api-key-here
   ```
3. **Save the file**

### Step 3: Test the Setup

1. **Test web search functionality**:
   ```bash
   python test_search.py
   ```

2. **Run the enhanced chatbot**:
   ```bash
   python chatbot_with_tools.py
   ```

### Step 4: Verify Web Search is Working

When you run the enhanced chatbot, you should see:
```
🤖 Welcome to Athena - Your Family Life Planning Assistant!
🔍 Web search enabled - I can find current information for you!
```

### Example Questions to Test Web Search

Once web search is enabled, try asking Athena:

- "What are the latest parenting trends for 2024?"
- "Find me healthy meal planning ideas for busy families"
- "What are some good family activities in [your city]?"
- "What's the latest research on screen time for kids?"
- "Find me tips for organizing a family calendar"

### Troubleshooting

**If you see "Web search disabled"**:
- Make sure your Tavily API key is correctly added to the `.env` file
- Verify the key starts with `tvly-`
- Check that there are no extra spaces or characters

**If search fails**:
- Verify your Tavily account is active
- Check your API usage limits (free tier has limits)
- Ensure you have an internet connection

### Free Tier Limits

Tavily's free tier includes:
- 1,000 searches per month
- Basic search functionality
- Perfect for personal use and testing

### Next Steps

Once web search is working, you can:
1. Ask Athena about current events and trends
2. Get up-to-date information for family planning
3. Find local activities and events
4. Research the latest parenting advice and research

## Support

If you encounter any issues:
1. Check the [Tavily documentation](https://tavily.com/docs)
2. Verify your API key is correct
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
