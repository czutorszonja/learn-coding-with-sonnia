# Python Setup Guide 🐍

**New to Python? Start here!** This guide will walk you through installing Python and setting up your code editor.

---

## Step 1: Install Python

### Windows

1. Go to [python.org](https://www.python.org/downloads/)
2. Click "Download Python" (latest version)
3. Run the installer
4. **IMPORTANT:** Check the box that says "Add Python to PATH" before installing!
5. Click "Install Now"
6. Wait for installation to complete

**Verify installation:**
Open Command Prompt and type:
```bash
python --version
```
You should see something like `Python 3.12.x`

---

### macOS

**Option 1: Using Homebrew (recommended)**
1. Install Homebrew from [brew.sh](https://brew.sh) (if you don't have it)
2. Open Terminal and run:
   ```bash
   brew install python
   ```

**Option 2: Download from python.org**
1. Go to [python.org](https://www.python.org/downloads/)
2. Download the latest version for macOS
3. Run the installer
4. Follow the installation steps

**Verify installation:**
Open Terminal and type:
```bash
python3 --version
```
You should see something like `Python 3.12.x`

---

### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

**Verify installation:**
```bash
python3 --version
```

---

## Step 2: Choose a Code Editor

You can write Python in any text editor, but these are the best options:

### 🏆 Visual Studio Code (VS Code) — **RECOMMENDED**

**Why:** Free, lightweight, powerful, great Python support

**Download:** [code.visualstudio.com](https://code.visualstudio.com)

**Setup:**
1. Install VS Code
2. Open VS Code
3. Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
4. Search for "Python" (by Microsoft)
5. Click "Install"

**Pros:**
- ✅ Free and open-source
- ✅ Fast and lightweight
- ✅ Excellent Python extensions
- ✅ Built-in terminal
- ✅ Great for beginners and pros

**Cons:**
- ⚠️ Requires some setup (extensions)

---

### PyCharm Community Edition

**Why:** Full-featured IDE designed specifically for Python

**Download:** [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/download)

**Setup:**
1. Download PyCharm Community Edition (free)
2. Run the installer
3. Follow the installation steps
4. Open PyCharm and create a new project

**Pros:**
- ✅ Designed for Python (everything built-in)
- ✅ Smart code completion
- ✅ Great debugger
- ✅ Project management features

**Cons:**
- ⚠️ Heavier than VS Code
- ⚠️ Can be overwhelming for beginners

---

### Other Options

**Sublime Text:** Fast, lightweight, but requires setup for Python
**Atom:** Free, customizable (being discontinued by GitHub)
**Vim/Neovim:** Powerful but steep learning curve

---

## Step 3: Test Your Setup

### Create a test file:

1. Create a new folder on your computer (e.g., `python_test`)
2. Open it in your code editor
3. Create a new file called `test.py`
4. Type this code:

```python
print("Hello, Python!")
name = input("What's your name? ")
print(f"Nice to meet you, {name}!")
```

5. Save the file

### Run the code:

**VS Code:**
- Right-click in the editor and select "Run Python File in Terminal"
- OR press Ctrl+F5 (Cmd+F5 on Mac)
- OR open the terminal (Ctrl+` or Cmd+`) and type: `python test.py`

**PyCharm:**
- Right-click in the editor and select "Run 'test'"
- OR press Shift+F10
- OR click the green play button at the top

**Terminal/Command Prompt:**
```bash
python test.py
# or on macOS/Linux:
python3 test.py
```

**Expected output:**
```
Hello, Python!
What's your name? [Your Name]
Nice to meet you, [Your Name]!
```

---

## Step 4: Start Coding!

You're all set! Now you can:

1. **Follow along with the lessons** in this course
2. **Create your own `.py` files** and experiment
3. **Run your code** using your editor or terminal

---

## Tips for Beginners

### 💡 Tip 1: Use the Terminal

Learn to run Python from the terminal:
```bash
python your_file.py
```

It gives you more control and helps you understand how Python works!

### 💡 Tip 2: Install Extensions (VS Code)

These VS Code extensions are helpful:
- **Python** (by Microsoft) — Essential!
- **Pylance** — Better code completion
- **Python Indent** — Proper indentation
- **Code Runner** — Quick way to run code

### 💡 Tip 3: Use Virtual Environments (Later)

Once you start bigger projects, learn about virtual environments:
```bash
python -m venv myenv
source myenv/bin/activate  # macOS/Linux
myenv\Scripts\activate     # Windows
```

### 💡 Tip 4: Don't Fear Errors

Error messages are your friends! They tell you what went wrong. Read them carefully — they usually point to the exact line with the problem!

---

## Troubleshooting

### "python is not recognized" (Windows)

1. Make sure you checked "Add Python to PATH" during installation
2. Restart your computer
3. If still not working, reinstall Python and check the PATH option

### "python3: command not found" (macOS/Linux)

Try `python` instead of `python3`:
```bash
python --version
```

### Code won't run in VS Code

1. Make sure you have the Python extension installed
2. Check that Python is installed (`python --version` in terminal)
3. Try running from the terminal instead

### Still stuck?

Google is your friend! Search for your error message — someone has probably had the same problem before!

---

## What's Next?

Once you're set up, head back to the lessons and start coding! 🚀

**Lesson 1:** [Variables Explained](01-variables-explained.md)

Happy coding! 💛
