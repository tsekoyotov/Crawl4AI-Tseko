# Deploying Crawl4AI on Railway with Nixpacks

This guide explains how to run the API on [Railway](https://railway.app/) using the provided `nixpacks.toml` configuration.

## 1. Prepare Environment Variables

1. Copy the example file:
   ```bash
   cp .llm.env.example .llm.env
   ```
2. Populate `.llm.env` with references to Railway variables:
   ```ini
   OPENAI_API_KEY=${OPENAI_API_KEY}
   DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
   ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
   GROQ_API_KEY=${GROQ_API_KEY}
   TOGETHER_API_KEY=${TOGETHER_API_KEY}
   MISTRAL_API_KEY=${MISTRAL_API_KEY}
   GEMINI_API_TOKEN=${GEMINI_API_TOKEN}
   ```
3. In Railway, create environment variables for each key above and provide your actual API keys.

## 2. Deploy with Nixpacks

Railway automatically detects `nixpacks.toml`. Commit the file and deploy your project. The install phase runs `crawl4ai-setup` and installs all dependencies.

## 3. Using the API from n8n

After deployment, note the Railway service URL. You can call existing endpoints, such as `/crawl`, using n8n's **HTTP Request** node.

```text
POST <your-railway-url>/crawl
```

Set any required headers or parameters as documented in the API.

For example, send a JSON body like:

```json
{
  "urls": ["https://example.com"],
  "browser_config": {},
  "crawler_config": {}
}
```

A 502 response means the target website didn't respond.

