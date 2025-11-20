# 🧊🌶️ Ice n Spice

A fun couples ice breaker game where individuals and couples complete exciting challenges together. Break the ice, connect, and spice things up!

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![PHP Version](https://img.shields.io/badge/PHP-7.4%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)

## 🎮 Live Demo

**Play now:** [icenspice.com](https://icenspice.com)

## ✨ Features

- 🎲 **Random Challenge Selection** - Challenges matched to player compatibility
- 👥 **Player Management** - Support for individuals and couples with orientation preferences
- 🎯 **10 Rounds of Fun** - Multiple questions per round
- 📱 **Mobile Responsive** - Beautiful design on all devices
- 🔐 **Admin Panel** - Full CRUD operations for challenge management
- 📊 **CSV Bulk Import** - Easy challenge data management
- 💡 **Challenge Suggestions** - Users can submit ideas via email
- 🌈 **Inclusive** - Supports all orientations and pairing preferences

## 🚀 Quick Start

### Option 1: Clone and Deploy

```bash
# Clone the PHP version
git clone -b php-version https://github.com/Baillie11/IceNSpice.git
cd IceNSpice

# Configure credentials
cp .env.example .env
nano .env  # Edit with your credentials

# Upload to your web host (via FTP/cPanel)
# Visit your domain - that's it!
```

### Option 2: Download ZIP

1. Download the [latest release](https://github.com/Baillie11/IceNSpice/archive/refs/heads/php-version.zip)
2. Extract and upload to your web host
3. Configure `.env` file
4. Done!

## 📋 Requirements

- **PHP** 7.4 or higher
- **SQLite3** extension (usually enabled by default)
- **Web Server** - Apache (with mod_rewrite) or Nginx
- **Hosting** - Any standard PHP shared hosting works

## 🏗️ Project Structure

```
IcenSpice/
├── 📄 Core Application (16 PHP files)
│   ├── config.php              # Configuration
│   ├── index.php               # Home page
│   ├── setup.php               # Player registration
│   ├── gameplay.php            # Main game
│   ├── admin.php               # Admin panel
│   └── ...
├── 📚 Documentation (8 files)
│   ├── README.md               # Main docs
│   ├── QUICKSTART.md           # 5-min setup
│   ├── DEPLOYMENT.md           # Deploy guide
│   └── ...
├── 🎨 Assets
│   └── icenspicelogo.png       # Game logo
├── 🔒 Security
│   ├── .htaccess               # Apache config
│   ├── .env.example            # Config template
│   └── env_loader.php          # Env handler
└── 📊 Sample Data
    └── sample_challenges.csv   # Example challenges
```

## 🎯 How to Play

1. **Setup** - Each player enters their name, sex, and orientation
2. **Start** - Game randomly assigns player order
3. **Play** - Complete fun challenges with matched partners
4. **Enjoy** - 10 rounds of exciting ice breaker activities!

## 🔐 Admin Panel

Access the admin panel at `/admin_login.php`

**Default credentials:**
- Username: `admin`
- Password: `password123`

⚠️ **Important:** Change these immediately in your `.env` file!

### Admin Features

- ✅ Add/Edit/Delete challenges
- ✅ Bulk CSV import
- ✅ View challenge statistics
- ✅ Manage all game content

## 📦 Installation

See detailed installation guides:
- [Quick Start Guide](QUICKSTART.md) - Get running in 5 minutes
- [Deployment Guide](DEPLOYMENT.md) - Complete deployment instructions
- [Deployment Checklist](DEPLOYMENT_CHECKLIST.md) - Step-by-step checklist

## 🔒 Security Features

- ✅ **Environment Variables** - Credentials in `.env` file
- ✅ **PDO Prepared Statements** - SQL injection prevention
- ✅ **XSS Prevention** - Output escaping with htmlspecialchars()
- ✅ **Protected Files** - .htaccess restrictions
- ✅ **Session Security** - Secure session configuration

## 📱 Mobile Support

Fully responsive design using Tailwind CSS:
- Touch-friendly buttons
- Adaptive layouts for all screen sizes
- Optimized for portrait and landscape
- Works great on phones, tablets, and desktops

## 🌟 Technology Stack

- **Backend:** Native PHP (no framework)
- **Database:** SQLite3
- **Frontend:** Tailwind CSS (via CDN)
- **Session Management:** PHP native sessions
- **Security:** PDO, .htaccess, environment variables

## 📖 Documentation

Comprehensive documentation included:

| File | Description |
|------|-------------|
| [README.md](README.md) | Main usage documentation |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Complete deployment guide |
| [ENV_SETUP.md](ENV_SETUP.md) | Environment variables |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Step-by-step checklist |
| [CONVERSION_NOTES.md](CONVERSION_NOTES.md) | Technical details |
| [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) | Flask to PHP migration |

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎭 Game Mechanics

### Challenge Matching

The game intelligently matches challenges based on:
- Player orientation (Straight, Bi, Gay, Lesbian, All)
- Sex (Male, Female)
- Partner preferences (optional)
- Challenge intensity (1-10 scale)

### Rounds System

- **10 Rounds** total
- **2 questions per player** per round
- **Random player order** each game
- **Skip round** option available
- **Quit anytime** feature

## 🔧 Configuration

All configuration via `.env` file:

```env
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
ADMIN_EMAIL=your_email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_email
SMTP_PASSWORD=your_smtp_password
```

## 🌐 Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers (iOS Safari, Chrome Mobile)

## 📊 Database Schema

Simple SQLite schema for easy portability:

```sql
CREATE TABLE challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intensity INTEGER NOT NULL CHECK(intensity BETWEEN 1 AND 10),
    orientation TEXT NOT NULL,
    pairing TEXT NOT NULL,
    challenge_text TEXT NOT NULL
);
```

## 🚦 Version Information

This is the **PHP version** of Ice n Spice.

### Branches

- **`main`** - Original Flask/Python version
- **`php-version`** - Native PHP version (recommended)

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for differences.

## 💡 Why PHP Version?

- ✅ **Easier Deployment** - Works on any PHP hosting
- ✅ **Lower Costs** - Cheaper hosting options
- ✅ **Better Performance** - Lower memory usage
- ✅ **Wider Compatibility** - 99% of shared hosts support it
- ✅ **Same Features** - All Flask functionality preserved

## 📞 Support

- 📧 **Email:** [Contact via GitHub](https://github.com/Baillie11)
- 🐛 **Issues:** [GitHub Issues](https://github.com/Baillie11/IceNSpice/issues)
- 📖 **Docs:** See documentation files in repository

## 🙏 Acknowledgments

- Original Flask version by Andrew
- PHP conversion completed November 2025
- Tailwind CSS for beautiful, responsive design
- SQLite for simple, portable database

## 🎉 Features Roadmap

Future enhancements being considered:

- [ ] Challenge categories/themes
- [ ] Player statistics tracking
- [ ] Dark mode theme
- [ ] Multi-language support
- [ ] Challenge rating system
- [ ] Social media sharing
- [ ] PWA capabilities

## 📸 Screenshots

Visit [icenspice.com](https://icenspice.com) to see the game in action!

---

**⭐ If you enjoy Ice n Spice, please consider giving it a star on GitHub!**

Made with ❤️ for couples and friends looking to have fun together.
