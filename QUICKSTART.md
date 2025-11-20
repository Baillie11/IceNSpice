# Quick Start Guide

Get Ice n Spice up and running in minutes!

## Prerequisites

- PHP 7.4 or higher installed
- SQLite3 extension enabled (check with `php -m | findstr sqlite3`)

## Option 1: Test Locally (Windows)

1. **Open PowerShell or Command Prompt**

2. **Navigate to the project directory:**
   ```powershell
   cd "C:\Users\Andre\OneDrive\project\IcenSpice"
   ```

3. **Start PHP built-in server:**
   ```powershell
   php -S localhost:8000
   ```

4. **Open your browser:**
   - Navigate to: http://localhost:8000
   - You should see the Ice n Spice home page

5. **Test the application:**
   - Click "Start a New Game"
   - Add 2-3 players
   - Click "Start Game"
   - Try a few challenges

6. **Test admin panel:**
   - Go to: http://localhost:8000/admin_login.php
   - Username: `admin`
   - Password: `password123`
   - Try adding a challenge or importing the sample CSV

## Option 2: Upload to Web Hosting

### For cPanel Hosting:

1. **Login to cPanel**

2. **Open File Manager**

3. **Navigate to public_html**

4. **Upload all files from IcenSpice folder**

5. **Edit config.php** (click Edit)
   - Change admin credentials
   - Update email settings
   - Save changes

6. **Visit your domain**
   - Should work immediately!

### For FTP Upload:

1. **Connect via FTP client** (FileZilla, WinSCP)

2. **Upload entire IcenSpice folder** to web root

3. **Edit config.php** via FTP or hosting file manager

4. **Set permissions** (if needed):
   - Directory: 755
   - Files: 644

5. **Test the site**

## First-Time Setup Steps

### 1. Configure Admin Access
Edit `config.php` and change:
```php
define('ADMIN_USERNAME', 'your-username');
define('ADMIN_PASSWORD', 'your-secure-password');
```

### 2. Configure Email
Update these in `config.php`:
```php
define('ADMIN_EMAIL', 'your-email@example.com');
define('SMTP_USERNAME', 'your-email@example.com');
define('SMTP_PASSWORD', 'your-email-password');
```

### 3. Add Logo (Optional)
- Place your logo at: `assets/icenspicelogo.png`
- Recommended size: 256x256 pixels

### 4. Import Sample Challenges
1. Login to admin panel
2. Scroll to "Bulk Import Challenges"
3. Select `sample_challenges.csv`
4. Click Import
5. You should see 10 challenges imported

## Quick Test Checklist

Test these features to ensure everything works:

- [ ] Home page loads
- [ ] Can add players
- [ ] Game starts and shows challenges
- [ ] Next button advances turn
- [ ] Skip round works
- [ ] Quit game returns to home
- [ ] Admin login works
- [ ] Can add challenge manually
- [ ] Can edit existing challenge
- [ ] Can delete challenge
- [ ] CSV import works
- [ ] Suggest challenge form works

## Common Issues

### "SQLite3 not found"
**Solution:** Enable SQLite extension in php.ini
```ini
extension=sqlite3
```

### "Permission denied" on database
**Solution:** Make directory writable
```bash
chmod 755 /path/to/IcenSpice
```

### Pages show PHP code instead of rendering
**Solution:** 
- Ensure you're accessing via web server (http://localhost:8000)
- Don't open PHP files directly in browser

### Email not sending
**Solution:** 
- Check spam folder
- Verify SMTP settings in config.php
- Some hosts block mail() function

## Next Steps

1. **Read README.md** for detailed documentation
2. **Read DEPLOYMENT.md** for production deployment
3. **Customize** challenges for your needs
4. **Add your logo** to make it yours
5. **Backup** your database regularly

## Getting Help

- Check documentation files in the project
- Review PHP error logs
- Ensure PHP version is 7.4+
- Test with sample data first

## Security Reminder

Before going live:
- [ ] Change admin username
- [ ] Change admin password
- [ ] Configure real email settings
- [ ] Enable HTTPS
- [ ] Test all functionality

## Ready to Play!

Once setup is complete:
1. Visit your site
2. Click "Start a New Game"
3. Add players (name, sex, orientation)
4. Click "Start Game"
5. Enjoy the challenges!

---

**Note:** For local testing, press `Ctrl+C` in the terminal to stop the PHP server.
