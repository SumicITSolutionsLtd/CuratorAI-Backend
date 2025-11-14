# Test Static Files Locally

## Steps to Test:

1. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

2. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Check if staticfiles directory was created:**
   ```bash
   dir staticfiles
   ```

4. **Run development server:**
   ```bash
   python manage.py runserver
   ```

5. **Visit admin panel:**
   - Go to: http://localhost:8000/admin/
   - Check if CSS is loading (right-click page → Inspect → Network tab)
   - Look for 404 errors on CSS files

6. **Check browser console:**
   - Press F12
   - Go to Console tab
   - Look for errors about missing CSS files

## If static files work locally but not on Vercel:

The issue is with Vercel's static file serving configuration.

