# 👤 How to Add Another Admin User

This guide shows you how to add additional admin users to your Django backend.

---

## Method 1: Using `createsuperuser` Command (Recommended)

**This is the simplest and most common way.**

### Steps:

1. **Activate your virtual environment** (if not already active):
   ```cmd
   venv\Scripts\activate
   ```

2. **Run the createsuperuser command**:
   ```cmd
   python manage.py createsuperuser
   ```

3. **Follow the prompts**:
   ```
   Username: admin2
   Email address: admin2@example.com
   Password: ********
   Password (again): ********
   ```

4. **Success!** You should see: `Superuser created successfully.`

---

## Method 2: Using Django Shell (Programmatic)

**Use this if you want to create admin users programmatically or in scripts.**

1. **Open Django shell**:
   ```cmd
   python manage.py shell
   ```

2. **Run this code**:
   ```python
   from apps.accounts.models import User
   
   # Create a new superuser
   User.objects.create_superuser(
       username='admin2',
       email='admin2@example.com',
       password='your-secure-password-here'
   )
   
   # Exit shell
   exit()
   ```

---

## Method 3: Promote Existing User to Admin

**Use this if you want to make an existing user an admin.**

1. **Open Django shell**:
   ```cmd
   python manage.py shell
   ```

2. **Find and promote the user**:
   ```python
   from apps.accounts.models import User
   
   # Find the user by email or username
   user = User.objects.get(email='user@example.com')
   # OR
   user = User.objects.get(username='someuser')
   
   # Make them a superuser and staff
   user.is_staff = True
   user.is_superuser = True
   user.save()
   
   print(f"User {user.username} is now an admin!")
   
   # Exit shell
   exit()
   ```

---

## Method 4: Using Django Admin Panel (If you're already an admin)

**If you're already logged in as an admin:**

1. Go to: `http://localhost:8000/admin/`
2. Navigate to: **Users** → **Add user**
3. Fill in the form:
   - Username
   - Password
   - Email (optional)
4. **Important:** After creating the user, click on the user to edit them
5. Check the boxes:
   - ✅ **Staff status** (gives access to admin panel)
   - ✅ **Superuser status** (gives full admin permissions)
6. Click **Save**

---

## Quick Reference

### What's the difference?

- **Staff status** (`is_staff=True`): User can access the admin panel
- **Superuser status** (`is_superuser=True`): User has full admin permissions (can do everything)

**For full admin access, you need BOTH:**
```python
user.is_staff = True
user.is_superuser = True
```

---

## Verify Admin Access

After creating an admin user, test it:

1. **Log out** of current admin session (if logged in)
2. Go to: `http://localhost:8000/admin/`
3. **Log in** with the new admin credentials
4. You should see the Django admin dashboard

---

## List All Admin Users

To see all admin users in your system:

```cmd
python manage.py shell
```

```python
from apps.accounts.models import User

# List all superusers
admins = User.objects.filter(is_superuser=True)
for admin in admins:
    print(f"Username: {admin.username}, Email: {admin.email}, Staff: {admin.is_staff}")

exit()
```

---

## Troubleshooting

### "Username already exists"
- Choose a different username
- Or use Method 3 to promote the existing user

### "Password too common"
- Use a stronger password
- Django has password validators enabled

### "Cannot access admin panel"
- Make sure `is_staff=True` is set
- Make sure `is_superuser=True` is set
- Try logging out and logging back in

---

**Need help?** Check the main setup guide or Django admin documentation.

