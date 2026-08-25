# CyberShield AI Deployment Guide

Follow these steps to deploy CyberShield AI on a Cloud VPS (e.g., DigitalOcean, AWS, Linode).

## Prerequisites
1. Rent a Linux VPS (Ubuntu 22.04 recommended) with at least 2GB of RAM.
2. Install **Docker** and **Docker Compose** on the server.
3. (Optional) Point a domain name to your server's IP address.

## Step 1: Transfer Files to the Server
Upload the entire `CyberShield AI` project folder to your VPS. You can do this via `git clone` (if you pushed to GitHub) or by using `scp`/SFTP.

## Step 2: Configure Environment Variables
On your server, copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Edit the `.env` file using a text editor like `nano`:
```bash
nano .env
```
- Change `DOMAIN` to your server's public IP address or your actual domain name.
- Change `SECRET_KEY` to a random, secure string.
- (Optional) Add your VirusTotal and Google Safe Browsing API keys.

## Step 3: Start the Production Server
Start the Docker containers in the background using the production compose file:
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
Your Next.js dashboard will now be accessible online via port 80/443 (handled by Nginx), and the FastAPI backend will be securely reverse-proxied.

## Step 4: Update the Chrome Extension
Before you install the Chrome Extension on your personal browser, you need to tell it where to find your new live cloud server!

1. Open `apps/extension/popup.js` and change `const API_BASE = "http://localhost:8000/api/v1";` to your new cloud server's domain/IP.
2. Do the exact same thing in `apps/extension/background.js` (for `API_BASE_URL`).
3. In Chrome, go to `chrome://extensions`, click **Load unpacked**, and select the `apps/extension` folder.

You're done! Your ML model, Web Dashboard, and Chrome Extension are now online 24/7.
