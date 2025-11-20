# Environment Variables Setup Guide

The application now uses environment variables for sensitive configuration data. This is more secure than hardcoding credentials in the config file.

## How It Works

1. **`.env` file** - Contains your actual credentials (NOT committed to version control)
2. **`.env.example` file** - Template showing what variables are needed
3. **`env_loader.php`** - Loads variables from .env file
4. **`.gitignore`** - Ensures .env is never committed to git

## Initial Setup

### Step 1: Create Your .env File

On your **local machine**, the `.env` file has been created. Before deploying, update it with your real credentials:

```bash
# Edit the .env file
notepad C:\Users\Andre\OneDrive\projects\IcenSpice\.env
```

Update these values:
```env
ADMIN_USERNAME=your_chosen_username
ADMIN_PASSWORD=your_strong_password
ADMIN_EMAIL=your_email@example.com
SMTP_USERNAME=your_smtp_email@gmail.com
SMTP_PASSWORD=your_smtp_app_password
APP_SECRET=generate_random_string_here
```

### Step 2: Generate a Secure App Secret

For `APP_SECRET`, generate a random string. You can use:

**PowerShell:**
```powershell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**Or online:** https://randomkeygen.com/

### Step 3: Deploy to Server

When deploying to your web server:

#### Option A: Upload .env file (Recommended)
1. Upload all files including `.env`
2. Make sure `.env` has your production credentials
3. Verify `.htaccess` is uploaded (protects .env from browser access)

#### Option B: Create .env on Server
1. Upload all files EXCEPT `.env`
2. Login to cPanel File Manager or FTP
3. Create new file named `.env`
4. Copy contents from `.env.example`
5. Fill in your production values
6. Save

## Security Benefits

✅ **Credentials outside version control** - .env is in .gitignore  
✅ **Protected from browser access** - .htaccess blocks direct access  
✅ **Easy to update** - Just edit .env, no code changes needed  
✅ **Separate dev/production configs** - Different .env files per environment  
✅ **No accidental commits** - Credentials won't be exposed in git history  

## File Permissions

Ensure `.env` has restricted permissions on your server:

**Via FTP/cPanel:**
- Set permissions to `600` (owner read/write only)

**Via SSH:**
```bash
chmod 600 .env
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| ADMIN_USERNAME | Admin login username | `admin` |
| ADMIN_PASSWORD | Admin login password | `SecurePass123!` |
| ADMIN_EMAIL | Email for receiving suggestions | `you@example.com` |
| SMTP_SERVER | SMTP server address | `smtp.gmail.com` |
| SMTP_PORT | SMTP port number | `587` |
| SMTP_USERNAME | SMTP authentication username | `you@gmail.com` |
| SMTP_PASSWORD | SMTP authentication password | `app_password_here` |
| APP_SECRET | Random secret for sessions | `random_string_32_chars` |

## Updating Configuration

To change any setting:

1. **Edit `.env` file** (on server)
2. **Save changes**
3. **Refresh browser** (no code changes needed!)

## Troubleshooting

### Issue: "Could not load .env file"
**Solution:** 
- Ensure `.env` file exists in the same directory as `config.php`
- Check file permissions (should be readable by web server)

### Issue: Using default values instead of .env values
**Solution:**
- Check `.env` file syntax (KEY=VALUE, no spaces around =)
- Ensure no quotes around values (unless part of the value)
- Check for typos in variable names

### Issue: .env file accessible via browser
**Solution:**
- Verify `.htaccess` file is uploaded and working
- Test by visiting: `https://yourdomain.com/.env` (should get 403 Forbidden)

## Best Practices

1. ✅ **Never commit .env to version control**
2. ✅ **Use strong passwords** (12+ characters, mixed case, numbers, symbols)
3. ✅ **Different credentials per environment** (dev vs production)
4. ✅ **Regularly rotate passwords**
5. ✅ **Backup .env file securely** (encrypted backup)
6. ✅ **Restrict file permissions** (600 on server)
7. ✅ **Use app-specific passwords** for SMTP (not your main email password)

## Migration from Old Config

If you're updating from the old hardcoded config.php:

1. ✅ Update done! Your old credentials are now defaults
2. Create `.env` file with your actual credentials
3. The app will use `.env` values if present, or defaults if not
4. Once verified working, remove defaults from `config.php`

## For Development Team

When sharing the project:

1. **Share `.env.example`** (template with no real credentials)
2. **Each developer creates their own `.env`** file
3. **Never share actual `.env` file**
4. **Document any new variables** in .env.example

---

**Security Note:** The .env file contains sensitive credentials. Keep it secure and never share it publicly or commit it to version control.
