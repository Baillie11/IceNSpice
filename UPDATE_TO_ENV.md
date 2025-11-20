# Updating Your Live Site to Use Environment Variables

Your application has been updated to use environment variables for better security. Follow these steps to update your live site at icenspice.com.

## What Changed

- ✅ Credentials now stored in `.env` file instead of hardcoded in `config.php`
- ✅ `.env` file protected by `.htaccess` from browser access
- ✅ New `env_loader.php` handles loading environment variables
- ✅ `.gitignore` added to prevent committing sensitive data

## Quick Update Steps

### 1. Update Your Local .env File

Edit the `.env` file with your real credentials:

```powershell
notepad "C:\Users\Andre\OneDrive\projects\IcenSpice\.env"
```

Change these lines to your actual values:
```env
ADMIN_USERNAME=your_actual_username
ADMIN_PASSWORD=your_strong_password
ADMIN_EMAIL=andrew@clickecommerce.com.au
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### 2. Upload New Files to Server

You need to upload these **new** files:
- ✅ `env_loader.php`
- ✅ `.env`
- ✅ `.env.example`
- ✅ `.gitignore`

And **replace** these existing files:
- ✅ `config.php` (updated version)
- ✅ `.htaccess` (updated to protect .env)

#### Via cPanel File Manager:
1. Login to your cPanel
2. Open File Manager
3. Navigate to your IcenSpice directory
4. Upload the 4 new files
5. Replace config.php and .htaccess (upload will overwrite)

#### Via FTP:
1. Connect to your FTP
2. Navigate to IcenSpice directory
3. Upload all 6 files (new + updated)
4. Confirm overwrite when prompted

### 3. Verify .env File on Server

**Important:** Make sure the `.env` file has your production credentials, not the defaults!

1. Open `.env` file on server (via cPanel File Manager or FTP)
2. Verify it contains your actual username and password
3. Save if you made changes

### 4. Test the Changes

1. **Try logging out** of admin panel (if logged in)
2. **Visit:** https://icenspice.com/admin_login.php
3. **Login with your credentials** from the `.env` file
4. **Verify login works**

### 5. Security Check

Test that .env is protected:

1. **Try accessing:** https://icenspice.com/.env
2. **Should see:** 403 Forbidden error (this is good!)
3. **If you can see the file contents:** Re-upload .htaccess

## Rollback (If Needed)

If something goes wrong, you can rollback:

1. The old `config.php` had hardcoded credentials as defaults
2. Just delete the `.env` file temporarily
3. The app will use the default values from config.php
4. Fix the issue, then add .env back

## Benefits of This Update

1. **More Secure:** Credentials in separate file, not in code
2. **Easier Updates:** Change credentials without editing PHP
3. **Version Control Safe:** .env won't be committed to git
4. **Production Ready:** Follows industry best practices
5. **Multiple Environments:** Easy to have dev/staging/prod configs

## Troubleshooting

### Login doesn't work after update
- Check `.env` file on server has correct credentials
- Make sure no extra spaces in .env file
- Verify .env file is readable by web server

### "Could not load .env file" error
- Ensure `env_loader.php` was uploaded
- Ensure `.env` file exists in same directory as config.php
- Check file permissions (should be at least 644)

### .env file contents visible in browser
- Re-upload `.htaccess` file
- Verify .htaccess is in the same directory as .env
- Check with host that .htaccess files are enabled

## File Checklist

After upload, verify these files exist on your server:

- [ ] config.php (updated version)
- [ ] env_loader.php (new)
- [ ] .env (new, with your credentials)
- [ ] .env.example (new)
- [ ] .htaccess (updated version)
- [ ] .gitignore (new)

## Next Steps

Once everything is working:

1. **Backup your .env file** securely
2. **Test all functionality** (game play, admin panel, etc.)
3. **Update credentials** in .env if needed
4. **Set .env permissions to 600** for maximum security

---

**Need Help?**

If you encounter issues:
1. Check ENV_SETUP.md for detailed documentation
2. Review error logs in cPanel
3. Try the rollback procedure above
4. Contact your hosting provider for .htaccess issues

**Your credentials are now more secure! 🔒**
