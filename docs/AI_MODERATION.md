# AI Comment Moderation Setup

## Overview

The backend now uses OpenAI's Moderation API to automatically filter comments for:
- Hate speech
- Harassment
- Violence
- Sexual content
- Self-harm
- Spam

## Setup

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
```

### 3. Restart Backend

```bash
npm run dev
```

You should see:
```
🚀 Speak Up Backend running on port 3001
```

(No warning about OPENAI_API_KEY)

## Testing

### Test 1: Clean Comment (Should Pass)

```bash
curl -X POST http://localhost:3001/api/petition/comment \
  -H "Content-Type: application/json" \
  -d '{
    "petitionId": 1,
    "nullifier": "0x1234567890123456789012345678901234567890123456789012345678901234",
    "commentText": "This is a great petition! I fully support preserving our local parks."
  }'
```

Should return:
```json
{
  "approved": true,
  "commentHash": "0x...",
  "authData": "0x...",
  "expiry": 1234567890
}
```

### Test 2: Toxic Comment (Should Fail)

```bash
curl -X POST http://localhost:3001/api/petition/comment \
  -H "Content-Type: application/json" \
  -d '{
    "petitionId": 1,
    "nullifier": "0x1234567890123456789012345678901234567890123456789012345678901234",
    "commentText": "I hate everyone and this is stupid"
  }'
```

Should return:
```json
{
  "error": "Comment rejected by moderation",
  "reason": "Comment flagged for: hate"
}
```

## How It Works

1. User submits comment to backend
2. Backend sends to OpenAI Moderation API
3. OpenAI analyzes content and returns scores for:
   - `hate`: Hate speech
   - `harassment`: Harassment/bullying  
   - `violence`: Violence/threats
   - `sexual`: Sexual content
   - `self-harm`: Self-harm instructions
4. If ANY category is flagged, comment is rejected
5. If approved, backend signs attestation
6. User submits on-chain with commentHash

## Fail-Safe Behavior

**If OpenAI API fails:**
- Logs error
- **Allows comment through** (fail open)
- This prevents service disruption if OpenAI is down

**If OPENAI_API_KEY not set:**
- Logs warning: `OPENAI_API_KEY not set - skipping moderation`
- **Allows all comments through**
- Useful for local testing without API key

## Cost

OpenAI Moderation API is **FREE** (as of Jan 2025)!

No cost limits, no usage fees.

## Privacy

- Comment text is sent to OpenAI
- OpenAI may store for 30 days per their policy
- For maximum privacy, consider:
  - Self-hosted moderation (Perspective API, local models)
  - Only moderate after user consent
  - Don't moderate at all (rely on community reporting)

## Future Improvements

- Add custom keyword filtering
- Add minimum/maximum comment length
- Rate limit comments per user
- Store rejected comments for review
- Community-based moderation (upvote/downvote)

## Troubleshooting

### "Invalid API key"
- Check your API key is correct
- Make sure it starts with `sk-`
- No spaces or quotes in .env file

### "Rate limit exceeded"
- Very unlikely (free tier is generous)
- Wait a minute and try again

### "OPENAI_API_KEY not set" warning
- Add the key to `backend/.env`
- Restart backend

## References

- OpenAI Moderation API: https://platform.openai.com/docs/guides/moderation
- Get API key: https://platform.openai.com/api-keys

---

**Setup complete! Comments are now automatically moderated.** ✅
