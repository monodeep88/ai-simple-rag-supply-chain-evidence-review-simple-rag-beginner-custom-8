# Deployment Guide

This guide gives practical deployment paths for **Supply Chain Evidence Review Simple RAG**.

## Option 1: Render

Backend:

1. Create a new Render Web Service from this GitHub repository.
2. Root directory: `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env.example`.

Frontend:

1. Create a new Render Static Site.
2. Root directory: `frontend`
3. Build command: `npm install && npm run build`
4. Publish directory: `dist`
5. Set `VITE_API_URL` to the deployed backend URL.

## Option 2: Railway

1. Create a Railway project from the GitHub repository.
2. Add a PostgreSQL database if you want persistent production storage.
3. Deploy the backend from `backend` using the FastAPI start command.
4. Deploy the frontend from `frontend` using the Vite build.
5. Set `DATABASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL`, and `VITE_API_URL`.

## Option 3: Vercel + Render

1. Deploy the backend to Render or Railway.
2. Deploy `frontend` to Vercel.
3. In Vercel project settings, set `VITE_API_URL` to the backend URL.
4. Rebuild the frontend after setting the variable.

## Docker Deployment

```bash
docker compose up --build
```

## Production Checklist

- Replace sample documents with real domain documents.
- Set `OPENAI_API_KEY` only in the deployment provider secret manager.
- Configure CORS with the final frontend domain.
- Use PostgreSQL for persistent run logs.
- Run `pytest` before deployment.
- Run `npm run build` before deployment.
