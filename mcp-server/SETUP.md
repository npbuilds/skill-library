# Setup Guide — Skill Library MCP Server

This connects your skill library to Claude Desktop so you can use your skills in the desktop app.

## Step 1: Install the MCP Python package

Open Terminal and run:

```
pip3 install "mcp>=1.0.0"
```

If that doesn't work, try:

```
python3 -m pip install "mcp>=1.0.0"
```

## Step 2: Test that the server starts

Run this in Terminal to make sure it works:

```
cd "/Users/nirav/Desktop/Claude Playground/Skill Building/mcp-server"
python3 server.py
```

You should see it start without errors. Press `Ctrl+C` to stop it.

## Step 3: Connect to Claude Desktop

1. Open **Claude Desktop**
2. Go to **Settings** (gear icon) → **Developer** → **Edit Config**
3. This opens a file called `claude_desktop_config.json`
4. Add the following to the file:

```json
{
  "mcpServers": {
    "skill-library": {
      "command": "python3",
      "args": ["/Users/nirav/Desktop/Claude Playground/Skill Building/mcp-server/server.py"]
    }
  }
}
```

> **Important:** If you already have other MCP servers in this file, just add the `"skill-library": { ... }` block inside the existing `"mcpServers"` object. Don't replace what's already there.

5. Save the file and **restart Claude Desktop**

## Step 4: Add the orchestration instructions

1. In Claude Desktop, create a new **Project** (or open an existing one)
2. Click on **Project Instructions** (or Custom Instructions)
3. Open the file `project-instructions.md` in this folder
4. Copy everything under "Instructions to paste:" and paste it into the project instructions
5. Save

## Step 5: Verify it works

Start a new conversation in Claude Desktop and try:

> "What skills do you have access to in my library?"

Claude should call the `list_skills` tool and return a list of your skills. If it does, everything is working.

## Troubleshooting

**"mcp not found" or "cannot import FastMCP" error:**
- Make sure you installed it with the same Python that Claude Desktop is using
- Try: `python3 -m pip install --upgrade "mcp>=1.0.0"`

**Claude Desktop doesn't show the tools:**
- Make sure you restarted Claude Desktop after editing the config
- Check that the file path in the config is exactly right
- Look for a hammer icon (tools) in the chat — it should show "Skill Library" tools

**Skills not showing up:**
- Make sure `data/registry.json` exists and has content
- The server reads from the project folder, so the file paths need to be correct

## How it works (plain English)

1. Claude Desktop starts your server automatically when you open the app
2. When you ask a question, Claude can call tools like "search skills for color"
3. The server reads your registry.json and skill files from disk
4. It sends the results back to Claude Desktop
5. Claude uses that knowledge to answer your question

The server runs locally on your machine — nothing goes to the internet. Your skills stay private.
