# Ice n Spice - PHP Version

A fun couples ice breaker game where individuals and couples complete exciting challenges with others.

## Features

- Player setup with orientation and partner preferences
- Random challenge selection based on player compatibility
- 10 rounds with multiple questions per round
- Admin panel for challenge management
- Bulk CSV import for challenges
- Challenge suggestion system via email
- Mobile-friendly responsive design using Tailwind CSS
- SQLite database for easy deployment

## Requirements

- PHP 7.4 or higher
- SQLite3 extension enabled
- Web server (Apache, Nginx, or PHP built-in server)
- Write permissions for the application directory (for database)

## Installation

1. **Upload files to your web hosting provider**
   - Upload all files to your web root directory (e.g., `public_html` or `www`)

2. **Configure settings**
   - Edit `config.php` and update the following:
     - Admin credentials (ADMIN_USERNAME, ADMIN_PASSWORD)
     - Email settings (ADMIN_EMAIL, SMTP_USERNAME, SMTP_PASSWORD)

3. **Set permissions**
   - Ensure the application directory is writable by the web server
   ```bash
   chmod 755 /path/to/IcenSpice
   chmod 666 /path/to/IcenSpice/challenges.db (after first run)
   ```

4. **Add logo image (optional)**
   - Place your logo image at `assets/icenspicelogo.png`

5. **Access the application**
   - Navigate to your domain (e.g., `https://yourdomain.com`)
   - The database will be created automatically on first access

## Admin Panel

- Access: Navigate to `/admin_login.php`
- Default credentials:
  - Username: `admin`
  - Password: `password123`
- **IMPORTANT:** Change these credentials in `config.php` before deploying to production!

## Admin Features

- Add individual challenges
- Edit existing challenges
- Delete challenges
- Bulk import challenges via CSV
- View total challenge count

## CSV Import Format

For bulk importing challenges, create a CSV file with the following headers:
```
challenge_text,intensity,orientation,pairing
```

Example:
```
USERNAME gives PARTNERNAME a massage,3,All,All
USERNAME and PARTNERNAME share a drink,2,Straight,Male to Female
```

### Challenge Text Placeholders
- `USERNAME` - Will be replaced with the current player's name
- `PARTNERNAME` - Will be replaced with the matched partner's name

### Valid Values

**Intensity:** 1-10

**Orientation:** 
- Straight
- Bi
- Gay
- Lesbian
- All

**Pairing:**
- Male to Female
- Female to Male
- Male to Male
- Female to Female
- All

## Game Flow

1. **Home Page** - Welcome screen with game instructions
2. **Player Setup** - Add players with their details (name, sex, orientation, partner)
3. **Randomize** - Players are shuffled randomly
4. **Gameplay** - Players receive challenges based on their preferences
5. **Rounds** - 10 rounds total, each with questions for all players

## Mobile Optimization

The application uses Tailwind CSS and is fully responsive:
- Mobile-first design approach
- Touch-friendly buttons and forms
- Adaptive layouts for different screen sizes
- Optimized text sizes for mobile viewing

## Troubleshooting

### Database errors
- Ensure the application directory is writable
- Check SQLite3 PHP extension is enabled: `php -m | grep sqlite3`

### Email not sending
- Check your hosting provider's email configuration
- Many shared hosts require SMTP authentication
- Consider using a service like SendGrid or Mailgun for reliable email delivery

### Blank pages
- Enable PHP error reporting in development
- Check PHP error logs
- Verify all files were uploaded correctly

## Security Notes

1. **Change default admin credentials** in `config.php`
2. **Use HTTPS** in production
3. **Keep PHP updated** to the latest stable version
4. **Backup your database** regularly
5. **Restrict access** to sensitive files if possible

## File Structure

```
IcenSpice/
├── assets/
│   └── icenspicelogo.png (optional)
├── config.php              # Configuration and database setup
├── index.php              # Home page
├── setup.php              # Player setup
├── randomize.php          # Shuffle players
├── gameplay.php           # Main game screen
├── next_turn.php          # Handle turn progression
├── skip_round.php         # Skip to next round
├── quit.php               # End game
├── admin_login.php        # Admin login
├── admin.php              # Admin panel
├── update_challenge.php   # Update challenge
├── delete_challenge.php   # Delete challenge
├── bulk_import.php        # CSV import
├── admin_logout.php       # Admin logout
├── suggest.php            # Challenge suggestions
├── challenges.db          # SQLite database (auto-created)
└── README.md             # This file
```

## Support

For issues or questions, please contact the administrator.

## License

All rights reserved.
