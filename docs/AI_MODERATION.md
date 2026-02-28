# AI Comment Moderation (Future Feature — Not in MVP Baseline)

## Overview

**M2-only MVP baseline:** comments are currently **disabled**.  
This document is retained as a future design note for when comments are re-enabled.

When comments return, moderation can be used to filter:
- Hate speech
- Harassment
- Violence
- Sexual content
- Self-harm
- Spam

Important: the M2-only MVP has **no attesters** and **no backend-signed authorizations**.
If moderation is used in the future, it should be treated as an application-layer policy
(e.g., accept/reject storing or displaying comments), not as a cryptographic gate.

## Setup (Future)

### 1. Get OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-...`)

### 2. Add to Backend .env

```bash
cd /home/oem/Documents/Coding/Speak-up-appV3/backend

# Edit .env
nano .env

# Add this line:
OPENAI_API_KEY=sk-your-actual-key-here