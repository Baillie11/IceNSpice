# Deployment Checklist for Ice n Spice

Use this checklist to ensure a smooth deployment to your web hosting provider.

## Pre-Deployment (Local)

### Configuration
- [ ] Open `config.php` in text editor
- [ ] Change `ADMIN_USERNAME` to your desired admin username
- [ ] Change `ADMIN_PASSWORD` to a strong password
- [ ] Update `ADMIN_EMAIL` to your email address
- [ ] Update `SMTP_USERNAME` to your SMTP email
- [ ] Update `SMTP_PASSWORD` to your email password
- [ ] Save `config.php`

### Assets
- [ ] Add your logo image to `assets/icenspicelogo.png` (optional but recommended)
- [ ] Verify logo is 256x256 pixels or larger
- [ ] Ensure logo has transparent background (PNG format)

### Testing (Optional but Recommended)
- [ ] Open PowerShell/Command Prompt
- [ ] Navigate to project: `cd "C:\Users\Andre\OneDrive\project\IcenSpice"`
- [ ] Start server: `php -S localhost:8000`
- [ ] Test in browser: http://localhost:8000
- [ ] Test admin login works
- [ ] Test adding a player
- [ ] Test starting a game
- [ ] Stop server with Ctrl+C

## Deployment to Hosting

### Method 1: cPanel Upload
- [ ] Login to your cPanel account
- [ ] Open File Manager
- [ ] Navigate to `public_html` directory
- [ ] Click "Upload" button
- [ ] Select all files from IcenSpice folder
- [ ] Wait for upload to complete (may take 1-2 minutes)
- [ ] Verify all files uploaded (check file count)
- [ ] Ensure `.htaccess` file was uploaded (it's hidden by default)

### Method 2: FTP Upload
- [ ] Open FTP client (FileZilla, WinSCP, etc.)
- [ ] Connect to your hosting account
  - [ ] Host: your-domain.com or FTP address
  - [ ] Username: your FTP username
  - [ ] Password: your FTP password
  - [ ] Port: 21 (or 22 for SFTP)
- [ ] Navigate to web root on remote (usually `public_html` or `www`)
- [ ] Navigate to IcenSpice folder on local
- [ ] Upload all files and folders
- [ ] Verify upload completed successfully
- [ ] Check `.htaccess` was uploaded

### Method 3: Git Deployment
- [ ] Initialize git in local folder
- [ ] Add all files to git
- [ ] Commit changes
- [ ] Add remote repository
- [ ] Push to hosting provider
- [ ] SSH into server
- [ ] Pull latest changes
- [ ] Verify files are in web root

## Post-Deployment

### Verify Files
- [ ] Check that all PHP files are present
- [ ] Verify `.htaccess` file exists
- [ ] Confirm `assets` folder exists
- [ ] Check `config.php` has correct settings

### File Permissions (if needed)
- [ ] Set directory permission to 755
- [ ] Set file permissions to 644
- [ ] Ensure web server can write to directory (for database creation)

### Initial Testing
- [ ] Visit your domain in browser
- [ ] Verify home page loads without errors
- [ ] Check that logo displays (or placeholder if not added)
- [ ] Click "Start a New Game"
- [ ] Add 2-3 test players
- [ ] Start the game
- [ ] Verify challenges display
- [ ] Test "Next" button
- [ ] Test "Skip Round" button
- [ ] Test "Quit Game" button

### Admin Panel Testing
- [ ] Go to: yourdomain.com/admin_login.php
- [ ] Login with your new credentials
- [ ] Verify admin panel loads
- [ ] Try adding a test challenge
- [ ] Verify challenge appears in list
- [ ] Edit the test challenge
- [ ] Delete the test challenge

### Import Sample Data
- [ ] Login to admin panel
- [ ] Scroll to "Bulk Import Challenges"
- [ ] Click "Choose File"
- [ ] Select `sample_challenges.csv`
- [ ] Click "Import"
- [ ] Verify "Successfully imported 10 challenges" message
- [ ] Check challenges appear in list

### Challenge Suggestion Testing
- [ ] Go to home page
- [ ] Click "Suggest a Challenge"
- [ ] Submit a test suggestion
- [ ] Check your email for the suggestion
- [ ] Check spam folder if not received

### Mobile Testing
- [ ] Open site on mobile phone
- [ ] Test portrait orientation
- [ ] Test landscape orientation
- [ ] Verify buttons are easily tappable
- [ ] Check text is readable
- [ ] Test full game flow on mobile

## Security Configuration

### SSL/HTTPS
- [ ] Install SSL certificate (free with Let's Encrypt)
- [ ] Test HTTPS connection: https://yourdomain.com
- [ ] If working, uncomment HTTPS redirect in `.htaccess`:
  ```apache
  RewriteCond %{HTTPS} off
  RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
  ```
- [ ] Verify HTTP redirects to HTTPS

### Additional Security
- [ ] Verify config.php cannot be accessed via browser
- [ ] Test that `.htaccess` is working (should deny access to config.php)
- [ ] Consider using password_hash() for admin password (advanced)
- [ ] Review PHP error display settings (should be off in production)

## Final Checks

### Functionality
- [ ] Complete full game with 3+ players
- [ ] Test all 10 rounds
- [ ] Verify partner matching works correctly
- [ ] Test orientation filtering
- [ ] Confirm challenges display appropriate pairings

### Performance
- [ ] Check page load speed (should be under 2 seconds)
- [ ] Test with multiple browser tabs
- [ ] Verify no memory errors in logs
- [ ] Check database was created successfully

### Monitoring
- [ ] Note location of PHP error logs
- [ ] Check error logs for any warnings
- [ ] Set up monitoring/alerts if available
- [ ] Plan regular backups (weekly recommended)

## Backup Strategy

### Initial Backup
- [ ] Download copy of `challenges.db`
- [ ] Save copy of `config.php`
- [ ] Keep local copy of all files

### Regular Backups (Weekly)
- [ ] Download latest `challenges.db`
- [ ] Store in safe location
- [ ] Consider using automated backup service

## Documentation

### For Future Reference
- [ ] Note admin login credentials (secure location)
- [ ] Document any custom changes made
- [ ] Save hosting provider details
- [ ] Note PHP version being used
- [ ] Record database location

## Launch!

### Go Live
- [ ] Remove any test data
- [ ] Clear test player sessions
- [ ] Import production challenges
- [ ] Announce to users
- [ ] Monitor for first few days

### Marketing (Optional)
- [ ] Share link with friends/users
- [ ] Post on social media
- [ ] Add to relevant directories
- [ ] Consider SEO optimization

## Troubleshooting

If something doesn't work:

### White Screen/Blank Page
- [ ] Check PHP error logs
- [ ] Verify PHP version is 7.4+
- [ ] Check file permissions
- [ ] Ensure SQLite3 extension is enabled

### Database Errors
- [ ] Check directory is writable
- [ ] Try creating empty `challenges.db` file
- [ ] Set `challenges.db` permissions to 666
- [ ] Verify SQLite3 extension in PHP

### Email Not Sending
- [ ] Check spam folder
- [ ] Verify SMTP credentials in config.php
- [ ] Check if hosting blocks mail() function
- [ ] Consider using PHPMailer

### Session Issues
- [ ] Check /tmp directory is writable
- [ ] Verify session configuration in php.ini
- [ ] Check session.save_path

### Admin Can't Login
- [ ] Verify credentials in config.php match what you're entering
- [ ] Check for extra spaces in config.php
- [ ] Clear browser cache and cookies
- [ ] Try different browser

## Post-Launch Maintenance

### Daily (First Week)
- [ ] Check error logs
- [ ] Monitor user feedback
- [ ] Test functionality

### Weekly
- [ ] Backup database
- [ ] Review challenge suggestions
- [ ] Add new challenges if needed

### Monthly
- [ ] Review and update challenges
- [ ] Check for PHP updates
- [ ] Verify backups are working
- [ ] Test all functionality

### Quarterly
- [ ] Security review
- [ ] Performance optimization
- [ ] User feedback review
- [ ] Consider new features

## Getting Help

If you need assistance:

1. **Check documentation:**
   - README.md - General usage
   - DEPLOYMENT.md - Detailed deployment guide
   - QUICKSTART.md - Quick setup guide
   - CONVERSION_NOTES.md - Technical details

2. **Review error logs:**
   - PHP error log (check cPanel or hosting control panel)
   - Web server error log

3. **Contact hosting provider:**
   - PHP configuration questions
   - Server permissions issues
   - Email configuration help

4. **Common solutions:**
   - Clear browser cache
   - Check file permissions
   - Verify PHP version
   - Review configuration settings

---

## Completion

Once all items are checked:

✅ Your Ice n Spice game is successfully deployed!  
✅ Users can access and play  
✅ Admin panel is functional  
✅ Security measures in place  
✅ Backups configured  
✅ Monitoring established  

**Congratulations on your successful deployment!**

---

**Last Updated:** November 20, 2025  
**Version:** 1.0
