# MariaDB Setup Guide for News Application

This guide provides detailed instructions for setting up MariaDB for the News Application.

## 📋 Prerequisites

- MariaDB 10.5+ or MySQL 8.0+ installed on your system
- Administrative access to create databases and users

## 🚀 Installation Steps

### Windows

1. **Download MariaDB:**
   - Visit: https://mariadb.org/download/
   - Download the MSI installer for Windows
   - Run the installer

2. **During Installation:**
   - Choose "Use UTF8 as default server's character set"
   - Set a root password (remember this!)
   - Check "Enable access from remote machines" if needed
   - Complete the installation

3. **Verify Installation:**
   ```cmd
   mysql --version
   ```

### macOS

1. **Install via Homebrew:**
   ```bash
   brew install mariadb
   ```

2. **Start MariaDB Service:**
   ```bash
   brew services start mariadb
   ```

3. **Secure Installation:**
   ```bash
   mysql_secure_installation
   ```
   - Set root password
   - Remove anonymous users (Y)
   - Disallow root login remotely (Y)
   - Remove test database (Y)
   - Reload privilege tables (Y)

### Linux (Ubuntu/Debian)

1. **Update Package Index:**
   ```bash
   sudo apt-get update
   ```

2. **Install MariaDB:**
   ```bash
   sudo apt-get install mariadb-server
   ```

3. **Start MariaDB Service:**
   ```bash
   sudo systemctl start mariadb
   sudo systemctl enable mariadb
   ```

4. **Secure Installation:**
   ```bash
   sudo mysql_secure_installation
   ```
   - Set root password
   - Follow the prompts (answer Y to all for security)

## 🗄️ Database Setup

### Step 1: Access MariaDB Shell

**Windows:**
```cmd
mysql -u root -p
```

**macOS/Linux:**
```bash
mysql -u root -p
```

Enter your root password when prompted.

### Step 2: Create Database

```sql
CREATE DATABASE news_app_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**What this does:**
- Creates a database named `news_app_db`
- Uses UTF-8 character encoding (supports emojis, international characters)
- Uses Unicode collation for proper sorting

### Step 3: Create Database User

```sql
CREATE USER 'news_app_user'@'localhost' IDENTIFIED BY 'news_app_password';
```

**What this does:**
- Creates a user `news_app_user`
- Restricts access to localhost only (security)
- Sets password to `news_app_password`

**⚠️ IMPORTANT:** For production, use a strong password!

### Step 4: Grant Privileges

```sql
GRANT ALL PRIVILEGES ON news_app_db.* TO 'news_app_user'@'localhost';
```

**What this does:**
- Gives `news_app_user` full access to `news_app_db`
- Only affects this specific database (security)

### Step 5: Flush Privileges

```sql
FLUSH PRIVILEGES;
```

**What this does:**
- Reloads privilege tables
- Applies changes immediately

### Step 6: Verify Setup

```sql
SHOW DATABASES;
```

You should see `news_app_db` in the list.

```sql
SELECT User, Host FROM mysql.user WHERE User='news_app_user';
```

You should see your user listed.

### Step 7: Exit MariaDB

```sql
EXIT;
```

## ✅ Verify Connection

Test the database connection:

```bash
mysql -u news_app_user -p news_app_db
```

Enter password: `news_app_password`

If you successfully connect, the setup is complete!

## 🔧 Custom Configuration (Optional)

If you want to use different credentials:

### 1. Create Custom Database and User

```sql
CREATE DATABASE your_custom_db_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'your_custom_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON your_custom_db_name.* TO 'your_custom_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 2. Update Django Settings

Edit `news_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_custom_db_name',
        'USER': 'your_custom_user',
        'PASSWORD': 'your_strong_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

## 🐛 Troubleshooting

### Issue: "Access denied for user 'root'@'localhost'"

**Solution 1 - Reset Root Password (MariaDB):**
```bash
sudo systemctl stop mariadb
sudo mysqld_safe --skip-grant-tables &
mysql -u root
```

```sql
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
EXIT;
```

```bash
sudo systemctl restart mariadb
```

**Solution 2 - Use sudo on Linux:**
```bash
sudo mysql
```

### Issue: "Can't connect to local MySQL server"

**Check if MariaDB is running:**

**Windows:**
```cmd
sc query MariaDB
```
If not running:
```cmd
net start MariaDB
```

**macOS:**
```bash
brew services list
```
If not running:
```bash
brew services start mariadb
```

**Linux:**
```bash
sudo systemctl status mariadb
```
If not running:
```bash
sudo systemctl start mariadb
```

### Issue: Port 3306 already in use

**Check what's using the port:**

**Windows:**
```cmd
netstat -ano | findstr :3306
```

**macOS/Linux:**
```bash
lsof -i :3306
```

**Solution:** Stop the conflicting service or change MariaDB port in `/etc/mysql/my.cnf`

### Issue: "Unknown database 'news_app_db'"

**Solution:** The database wasn't created. Run Step 2 again.

### Issue: Character encoding problems

**Check database charset:**
```sql
SHOW CREATE DATABASE news_app_db;
```

**Fix charset:**
```sql
ALTER DATABASE news_app_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 📊 Useful MariaDB Commands

### Show All Databases
```sql
SHOW DATABASES;
```

### Show All Users
```sql
SELECT User, Host FROM mysql.user;
```

### Show User Privileges
```sql
SHOW GRANTS FOR 'news_app_user'@'localhost';
```

### Check Database Size
```sql
SELECT 
    table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = 'news_app_db';
```

### Show All Tables
```sql
USE news_app_db;
SHOW TABLES;
```

### Backup Database
```bash
mysqldump -u news_app_user -p news_app_db > backup.sql
```

### Restore Database
```bash
mysql -u news_app_user -p news_app_db < backup.sql
```

## 🔒 Security Best Practices

1. **Use Strong Passwords:**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Avoid common words

2. **Restrict User Access:**
   - Only grant necessary privileges
   - Use `localhost` instead of `%` for host

3. **Regular Backups:**
   - Schedule automated backups
   - Test restore procedures

4. **Keep MariaDB Updated:**
   ```bash
   # Check version
   mysql --version
   
   # Update (method varies by OS)
   # Ubuntu:
   sudo apt-get update && sudo apt-get upgrade mariadb-server
   
   # macOS:
   brew upgrade mariadb
   ```

5. **Monitor Logs:**
   - Check `/var/log/mysql/error.log` for issues
   - Monitor slow query log for performance

## 🎯 Next Steps

After completing the MariaDB setup:

1. Return to the main README.md
2. Continue with Step 4: Apply Migrations
3. Complete the remaining setup steps

## 📞 Need Help?

- MariaDB Documentation: https://mariadb.com/kb/en/documentation/
- MySQL Documentation: https://dev.mysql.com/doc/
- Django Database Setup: https://docs.djangoproject.com/en/stable/ref/databases/

## ✅ Verification Checklist

- [ ] MariaDB installed and running
- [ ] Database `news_app_db` created
- [ ] User `news_app_user` created with password
- [ ] Privileges granted to user
- [ ] Connection test successful
- [ ] Django settings.py updated with correct credentials
- [ ] Ready to run migrations!
