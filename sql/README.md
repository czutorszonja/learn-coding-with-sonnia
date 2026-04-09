# SQL Setup Guide

This guide will help you set up SQL on your computer so you can follow along with the lessons.

## What You'll Need

1. **A database server** — MySQL (we recommend this)
2. **A database client** — DBeaver (free, works with many databases)

---

## Step 1: Install MySQL

MySQL is one of the most popular databases in the world. It's free, reliable, and widely used in the industry.

### Download MySQL

1. Go to: https://dev.mysql.com/downloads/mysql/
2. Click **"Download"** for your operating system (Windows, Mac, or Linux)
3. If you see an Oracle account signup page, scroll down and click **"No thanks, just start my download"**
4. Run the installer

### During Installation

**Important:** Remember the **root password** you set! You'll need it later.

Default settings are usually fine. On Windows, you may see an option to install "MySQL Workbench" — you can skip this (we'll use DBeaver instead).

### Verify MySQL is Running

**Windows:**
```cmd
mysql --version
```

**Mac:**
```bash
mysql --version
```

If you see a version number, you're good! If not, MySQL might not be in your system PATH (see troubleshooting below).

---

## Step 2: Install DBeaver

DBeaver is a free, professional database tool that works with MySQL and many other databases. It's what many developers use daily.

### Download DBeaver

1. Go to: https://dbeaver.io/download/
2. Download the **Community Edition** (it's free!)
3. Run the installer

### Alternative Tools (Optional)

If you want to try something else:

| Tool | Best For | Link |
|------|----------|------|
| **MySQL Workbench** | Official MySQL tool | https://dev.mysql.com/downloads/workbench/ |
| **HeidiSQL** | Windows users, lightweight | https://www.heidisql.com/ |
| **TablePlus** | Modern UI (free trial, then paid) | https://tableplus.com/ |

---

## Step 3: Connect DBeaver to MySQL

### Create a New Connection

1. Open DBeaver
2. Click the **plug icon** 🔌 (or go to `Database` → `New Database Connection`)
3. Select **MySQL** from the list
4. Click **Next**

### Connection Settings

Fill in these fields:

| Field | Value |
|-------|-------|
| **Host** | `localhost` |
| **Port** | `3306` (default) |
| **Database** | (leave blank for now) |
| **Username** | `root` |
| **Password** | (the password you set during MySQL installation) |

5. Click **Test Connection**
6. If successful, you'll see "Connected"
7. Click **Finish**

### You're In!

You should now see your MySQL database in DBeaver's left sidebar. You can expand it to see databases, tables, and more.

---

## Troubleshooting Common Issues

### ❌ "Can't connect to MySQL server on 'localhost'"

**Possible causes:**

1. **MySQL isn't running**
   - **Windows:** Open Services (`services.msc`), find "MySQL" or "MySQL80", right-click → Start
   - **Mac:** Open Terminal and run:
     ```bash
     brew services start mysql
     ```
     Or check System Preferences → MySQL

2. **Wrong port**
   - Default MySQL port is `3306`
   - Some installations use `3307` or another port
   - Check your MySQL configuration or try different ports

3. **Firewall blocking**
   - Temporarily disable your firewall to test
   - If this fixes it, add MySQL to your firewall's allowed list

### ❌ "Access denied for user 'root'@'localhost'"

**Causes:**

1. **Wrong password** — Double-check the password you set during installation
2. **Root user doesn't exist** — Some MySQL versions use a different admin user

**Fix:** Try connecting with no password (leave password field empty), or reinstall MySQL and note the password carefully.

### ❌ "Command not found" when running `mysql --version`

**Windows:**
MySQL isn't in your system PATH. You can still use it through DBeaver, or add it to PATH:
1. Find where MySQL is installed (usually `C:\Program Files\MySQL\MySQL Server 8.0\bin`)
2. Add that folder to your System PATH environment variable
3. Restart your terminal

**Mac:**
If you installed via Homebrew:
```bash
export PATH="/usr/local/mysql/bin:$PATH"
```
Add that to your `~/.zshrc` or `~/.bash_profile` to make it permanent.

### ❌ DBeaver says "Driver not found"

DBeaver usually downloads drivers automatically. If it doesn't:

1. In the connection window, click **"Download driver files"**
2. Wait for the download to complete
3. Try connecting again

### ❌ "Too many connections" error

This means MySQL has hit its connection limit.

**Fix:**
1. In DBeaver, close any unused database connections
2. Restart MySQL service
3. If this keeps happening, you may need to increase the `max_connections` setting in MySQL config

---

## Your First Query

Once connected, let's test that everything works:

1. In DBeaver, right-click on your MySQL connection
2. Select **"SQL Editor"** → **"Open SQL Editor"**
3. Type this query:
   ```sql
   SELECT 'Hello, World!' AS greeting;
   ```
4. Click the **orange play button** ▶️ (or press `Ctrl+Enter`)
5. You should see: `Hello, World!`

🎉 **Success!** You're ready to start the SQL lessons!

---

## Quick Reference

| Task | How To |
|------|--------|
| Start MySQL (Windows) | Services → MySQL → Start |
| Start MySQL (Mac) | `brew services start mysql` |
| Stop MySQL | Same as above, but click "Stop" |
| DBeaver shortcut | `Ctrl+Space` for autocomplete |
| Run query | `Ctrl+Enter` |

---

## Need Help?

If you're stuck, don't worry! Common issues:

- **Can't remember root password?** You may need to reset it (Google: "reset MySQL root password [your OS]")
- **Installation fails?** Try an older MySQL version (8.0 is stable)
- **DBeaver keeps disconnecting?** Check if MySQL service is running

Drop a message in the group chat if you need help! 💛
