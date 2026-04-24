# Python Lesson 17: Virtual Environments and Packages 📦

**← Back to [Lesson 16: Regular Expressions](16-regular-expressions.md)**

---

## What is a Virtual Environment?

**Plain English:** A virtual environment is an isolated space for your Python projects.

**Real-world analogy:** Think of it like separate kitchens for different recipes:
- **Without virtual env** = All ingredients mixed together (chaos!)
- **With virtual env** = Each recipe has its own kitchen with exactly what it needs

---

## Why Use Virtual Environments?

- ✅ Isolate dependencies per project
- ✅ Avoid version conflicts
- ✅ Keep your system Python clean
- ✅ Make projects reproducible
- ✅ Easy to share with others

**Problem without virtual env:**
```
Project A needs: requests==2.28.0
Project B needs: requests==2.31.0
CONFLICT! 💥
```

**Solution with virtual env:**
```
Project A (isolated): requests==2.28.0 ✓
Project B (isolated): requests==2.31.0 ✓
```

---

## Creating a Virtual Environment

### Using `venv` (Built-in)

```bash
# Navigate to your project folder
cd my_project

# Create virtual environment
python -m venv venv
```

**What this creates:**
```
my_project/
├── venv/          # Virtual environment folder
│   ├── bin/       # Scripts (macOS/Linux)
│   ├── Scripts/   # Scripts (Windows)
│   └── ...
├── main.py
└── requirements.txt
```

---

## Activating the Virtual Environment

### macOS/Linux:
```bash
source venv/bin/activate
```

### Windows:
```bash
venv\Scripts\activate
```

**You'll see `(venv)` in your terminal:**
```bash
(venv) $ python --version
Python 3.12.0
```

---

## Installing Packages

```bash
# Make sure venv is activated!
(venv) $ pip install requests
```

**Install specific version:**
```bash
(venv) $ pip install requests==2.31.0
```

**Install multiple packages:**
```bash
(venv) $ pip install requests flask pytest
```

---

## Checking Installed Packages

```bash
# List all installed packages
pip list

# Show package details
pip show requests
```

**Output:**
```
Name: requests
Version: 2.31.0
Summary: Python HTTP for Humans.
Location: /path/to/venv/lib/python3.12/site-packages
```

---

## requirements.txt

A file that lists all project dependencies:

```
requests==2.31.0
flask==3.0.0
pytest==7.4.0
```

### Generate requirements.txt:

```bash
pip freeze > requirements.txt
```

### Install from requirements.txt:

```bash
pip install -r requirements.txt
```

**Why use it?**
- Share dependencies with team
- Deploy to server
- Recreate exact environment

---

## Deactivating the Virtual Environment

```bash
deactivate
```

**Back to normal:**
```bash
$ python --version  # System Python
```

---

## Project Structure Example

```
my_project/
├── venv/              # Virtual environment (don't commit to git!)
├── src/
│   └── main.py
├── tests/
│   └── test_main.py
├── requirements.txt   # List of dependencies
└── README.md
```

**.gitignore (exclude venv):**
```
venv/
__pycache__/
*.pyc
.env
```

---

## Using `pip` Effectively

### Search for packages:
```bash
pip search keyword  # (deprecated, use PyPI website)
```

### Visit PyPI: https://pypi.org/

### Install from GitHub:
```bash
pip install git+https://github.com/user/repo.git
```

### Upgrade a package:
```bash
pip install --upgrade package_name
```

### Uninstall a package:
```bash
pip uninstall package_name
```

---

## Common Issues

### "pip is not recognized"

**Solution:**
```bash
# Activate virtual environment first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

### "Module not found"

**Solution:**
```bash
# Check if package is installed
pip list

# Install if missing
pip install package_name
```

### Conflicting versions:

**Solution:**
```bash
# Create fresh virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Practice Exercise

### Scenario: You're setting up a Python project!

**Your task:**
1. Create a new folder called `scraper_project`
2. Navigate into it
3. Create a virtual environment called `venv`
4. Activate the virtual environment
5. Install `requests` and `beautifulsoup4` packages
6. Generate `requirements.txt` using `pip freeze`
7. View the contents to verify both packages are listed
8. Deactivate and reactivate the virtual environment
9. Reinstall all packages from `requirements.txt`
10. Verify installation with `pip list`

**Try it yourself first!** Scroll down when ready.

---

## Solutions

### Solution 1: Set Up a Complete Python Project

```bash
# Step 1-2: Create and navigate to project folder
mkdir scraper_project
cd scraper_project

# Step 3: Create virtual environment
python -m venv venv

# Step 4: Activate (macOS/Linux)
source venv/bin/activate

# For Windows: venv\Scripts\activate

# Step 5: Install packages
pip install requests
pip install beautifulsoup4

# Step 6: Generate requirements.txt
pip freeze > requirements.txt

# Step 7: View contents
cat requirements.txt
# Should show both packages

# Step 8: Deactivate and reactivate
deactivate
source venv/bin/activate

# Step 9: Reinstall from requirements.txt
pip install -r requirements.txt

# Step 10: Verify installation
pip list
```

**Expected output:**
```
Package          Version
---------------- -------
beautifulsoup4   4.12.0
requests         2.31.0
...
```

---

## Quick Recap

- **Virtual environment** = Isolated Python environment per project
- **`python -m venv venv`** — Create virtual environment
- **`source venv/bin/activate`** — Activate (macOS/Linux)
- **`venv\Scripts\activate`** — Activate (Windows)
- **`pip install`** — Install packages
- **`pip freeze > requirements.txt`** — Save dependencies
- **`pip install -r requirements.txt`** — Install from file
- **`deactivate`** — Exit virtual environment
- **`.gitignore`** — Don't commit `venv/` folder!

---

## What's Next?

Ready for more? Continue to **[Lesson 18: Working with Databases](18-working-with-databases.md)** — learn to use SQLite and SQLAlchemy! 🗄️

---

