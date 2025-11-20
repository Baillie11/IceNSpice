# Deployment Guide for Ice n Spice

This guide will help you deploy the PHP version of Ice n Spice to your web hosting provider.

## Pre-Deployment Checklist

1. **Edit config.php**
   - Change `ADMIN_USERNAME` and `ADMIN_PASSWORD`
   - Update email settings (ADMIN_EMAIL, SMTP_USERNAME, SMTP_PASSWORD)
   - Consider using password_hash() for admin password in production

2. **Add your logo**
   - Place logo image at `assets/icenspicelogo.png`

3. **Test locally (optional)**
   - Use PHP built-in server: `php -S localhost:8000`
   - Visit http://localhost:8000

## Deployment Methods

### Method 1: FTP/SFTP Upload

1. **Connect to your hosting provider via FTP**
   - Use FileZilla, WinSCP, or your hosting provider's file manager

2. **Upload all files**
   - Upload entire IcenSpice folder to your web root (e.g., `public_html`, `www`, `htdocs`)
   - Ensure all PHP files are uploaded in ASCII/text mode
   - Ensure .htaccess is uploaded (it's a hidden file)

3. **Set permissions**
   - Set directory permissions to 755
   - Set file permissions to 644
   - Ensure the web server can write to create the database file

4. **Access your site**
   - Navigate to your domain (e.g., `https://yourdomain.com`)

### Method 2: cPanel File Manager

1. **Login to cPanel**
2. **Navigate to File Manager**
3. **Go to public_html directory**
4. **Upload ZIP file** (if you compressed the files)
5. **Extract the archive**
6. **Set permissions as needed**

### Method 3: Git Deployment

1. **Initialize git repository**
   ```bash
   cd IcenSpice
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to hosting provider**
   - Follow your hosting provider's git deployment instructions
   - Many providers support deployment via git push

## Common Hosting Providers

### cPanel Hosting (Bluehost, HostGator, etc.)

1. Upload files to `public_html` directory
2. Database will be created automatically (SQLite)
3. Email configuration may require SMTP authentication
4. Check PHP version in cPanel (requires PHP 7.4+)

### SiteGround

1. Use File Manager or SFTP
2. Upload to `public_html`
3. Enable PHP extensions if needed via Site Tools
4. Configure email in config.php

### DigitalOcean / VPS

1. SSH into your server
2. Place files in `/var/www/html` or your configured web root
3. Install PHP and required extensions:
   ```bash
   sudo apt update
   sudo apt install php php-sqlite3 php-mbstring
   ```
4. Configure Apache/Nginx virtual host
5. Set proper permissions:
   ```bash
   sudo chown -R www-data:www-data /path/to/IcenSpice
   sudo chmod -R 755 /path/to/IcenSpice
   ```

## Post-Deployment Steps

1. **Test the application**
   - Visit your domain
   - Try adding players
   - Test gameplay
   - Login to admin panel

2. **Import initial challenges**
   - Login to admin panel
   - Use bulk import with sample_challenges.csv
   - Or add challenges manually

3. **Configure SSL/HTTPS**
   - Enable SSL certificate (Let's Encrypt is free)
   - Uncomment HTTPS redirect in .htaccess if needed

4. **Test email functionality**
   - Try submitting a challenge suggestion
   - Verify email is received

## Troubleshooting

### Issue: White screen / blank page
**Solution:** 
- Enable PHP error reporting temporarily
- Check error logs in cPanel or hosting control panel
- Verify all files uploaded correctly

### Issue: Database errors
**Solution:**
- Ensure directory is writable by web server
- Check SQLite3 extension is enabled
- Try creating an empty challenges.db file and set permissions to 666

### Issue: Email not sending
**Solution:**
- Many shared hosts block mail() function
- Consider using PHPMailer with SMTP
- Alternative: Use email service like SendGrid
- Check spam folder

### Issue: Session not persisting
**Solution:**
- Check PHP session configuration
- Ensure /tmp or session directory is writable
- May need to configure session.save_path in php.ini

### Issue: File upload not working (CSV import)
**Solution:**
- Check upload_max_filesize in php.ini
- Check post_max_size in php.ini
- Verify file permissions on upload directory

## Security Recommendations

1. **Change default credentials** immediately
2. **Use strong passwords** for admin account
3. **Enable HTTPS** (SSL certificate)
4. **Keep PHP updated** to latest stable version
5. **Regular backups** of challenges.db
6. **Restrict access** to config.php via .htaccess
7. **Monitor logs** for suspicious activity
8. **Consider using** password_hash() for admin password

## Performance Optimization

1. **Enable PHP OpCache** if available
2. **Use CDN** for Tailwind CSS (already configured)
3. **Enable gzip compression** (in .htaccess)
4. **Add browser caching** (in .htaccess)
5. **Optimize images** before uploading logo

## Backup Strategy

### Manual Backup
1. Download challenges.db file regularly
2. Keep local copies of custom challenges

### Automated Backup
1. Use hosting provider's backup service
2. Or set up cron job to copy database daily:
   ```bash
   0 2 * * * cp /path/to/challenges.db /path/to/backups/challenges-$(date +\%Y\%m\%d).db
   ```

## Migration from Flask Version

If you have existing challenges in the Flask SQLite database:

1. Download the challenges.db from Flask version
2. Upload it to the PHP version directory
3. The schema is identical, so it should work directly
4. Test by viewing challenges in admin panel

## Getting Support

- Check README.md for general information
- Review PHP error logs for detailed error messages
- Contact your hosting provider for server-specific issues
- Ensure PHP version is 7.4 or higher

## Maintenance

### Regular Tasks
- Backup database monthly
- Review and update challenges
- Check for PHP updates
- Monitor disk space
- Test functionality after hosting updates

### Updates
- When updating files, always backup first
- Test changes in staging environment if possible
- Clear browser cache after updates

## Additional Resources

- PHP Documentation: https://www.php.net/manual/
- SQLite Documentation: https://www.sqlite.org/docs.html
- Tailwind CSS: https://tailwindcss.com/docs

---

**Note:** Always test thoroughly before deploying to production. Keep backups of your database and configuration files.
