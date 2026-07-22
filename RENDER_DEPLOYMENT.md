# Deployment Guide - Render

## Prerequisites
- GitHub account with repository pushed
- Render.com account (https://render.com)

## Step-by-Step Deployment

### 1. Connect Repository to Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Select "Build and deploy from a Git repository"
4. Connect your GitHub account
5. Select the `medical-daignosis-system` repository

### 2. Configure Deployment Settings
Fill in these settings:
- **Name**: medical-diagnosis
- **Environment**: Python 3
- **Region**: Choose closest to your users
- **Branch**: main
- **Build Command**: `bash build.sh`
- **Start Command**: `gunicorn doctor.wsgi:application`

### 3. Add Environment Variables
Go to Environment → Add Environment Variable:

```
SECRET_KEY=<generate a secure key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=<Render will provide this if using PostgreSQL>
```

### 4. Create PostgreSQL Database (Optional)
If you want persistent database storage:
1. Create a new PostgreSQL Database on Render
2. Copy the DATABASE_URL
3. Add it to Web Service environment variables

### 5. Deploy
1. Click "Create Web Service"
2. Wait for build to complete (3-5 minutes)
3. Your app will be live at: `https://your-app-name.onrender.com`

## Troubleshooting

### Static files not loading
- Run: `python doctor/manage.py collectstatic`
- Ensure WhiteNoise middleware is enabled (already configured)

### Database connection errors
- Check DATABASE_URL is set correctly
- Run migrations: `python doctor/manage.py migrate`

### Port issues
- Render automatically assigns port via $PORT environment variable
- The Procfile is configured to use this

## Notes
- Free tier goes to sleep after 15 mins of inactivity
- Upgrade to Starter plan ($7/month) for always-on service
- SQLite database is file-based and won't persist (use PostgreSQL for production)
