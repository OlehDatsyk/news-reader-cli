# 📰 News Reader CLI

A professional, terminal-based news reader built with Python. Search for news by keyword, browse top headlines by country or category, and read beautifully formatted articles - all from your terminal, powered by [NewsAPI.org](https://newsapi.org) and [Rich](https://github.com/Textualize/rich).

This README is written for someone who has **never run a Python project before** and has **only installed Visual Studio Code**. Follow it from top to bottom and you will end up with a fully working application. No prior experience is assumed.

---

## Table of Contents

1. [What You Need Before Starting](#1-what-you-need-before-starting)
2. [Step 1 - Install Python](#step-1--install-python)
3. [Step 2 - Install Git (Optional but Recommended)](#step-2--install-git-optional-but-recommended)
4. [Step 3 - Get the Project Files into VS Code](#step-3--get-the-project-files-into-vs-code)
5. [Step 4 - Open the Project in VS Code](#step-4--open-the-project-in-vs-code)
6. [Step 5 - Open the VS Code Terminal](#step-5--open-the-vs-code-terminal)
7. [Step 6 - Create a Virtual Environment](#step-6--create-a-virtual-environment)
8. [Step 7 - Activate the Virtual Environment](#step-7--activate-the-virtual-environment)
9. [Step 8 - Install Project Dependencies](#step-8--install-project-dependencies)
10. [Step 9 - Get a Free NewsAPI.org API Key](#step-9--get-a-free-newsapiorg-api-key)
11. [Step 10 - Set Up Your `.env` File](#step-10--set-up-your-env-file)
12. [Step 11 - Run the Application](#step-11--run-the-application)
13. [Using the Application](#using-the-application)
14. [Project Structure](#project-structure)
15. [Expected Terminal Output Examples](#expected-terminal-output-examples)
16. [Common Errors and Their Solutions](#common-errors-and-their-solutions)
17. [Useful VS Code Terminal Commands Reference](#useful-vs-code-terminal-commands-reference)
18. [License](#license)

---

## 1. What You Need Before Starting

- A Windows, macOS, or Linux computer.
- [Visual Studio Code](https://code.visualstudio.com/) already installed (you said you have this ✅).
- An internet connection (to install Python packages and call the News API).
- About 15 minutes.

You do **not** need to know how to code to follow this guide - just copy and paste the commands exactly as shown.

---

## Step 1 - Install Python

This project requires **Python 3.12 or newer**.

### Check if Python is already installed

1. Open VS Code.
2. Open the built-in terminal: go to the top menu and click **Terminal -> New Terminal** (or press `` Ctrl+` `` on Windows/Linux, `` Cmd+` `` on macOS).
3. In the terminal that appears at the bottom of VS Code, type the following and press **Enter**:

   ```bash
   python3 --version
   ```

   On Windows, also try:

   ```bash
   python --version
   ```

4. If you see something like `Python 3.12.4` or higher, you're done - skip to [Step 2](#step-2--install-git-optional-but-recommended).
5. If you see an error like `command not found` or `'python' is not recognized`, you need to install Python (next section).

### Installing Python

**Windows:**
1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Click the yellow **Download Python 3.12.x** button.
3. Run the downloaded installer.
4. ⚠️ **Very important:** On the first installer screen, check the box that says **"Add python.exe to PATH"** before clicking "Install Now".
5. Once installation finishes, close and reopen VS Code completely (this refreshes the terminal's environment).
6. Verify by opening a new terminal and running `python --version`.

**macOS:**
1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/).
2. Download the macOS installer and run it, following the on-screen instructions.
3. Alternatively, if you have [Homebrew](https://brew.sh/) installed, run in the terminal:
   ```bash
   brew install python@3.12
   ```
4. Close and reopen VS Code, then verify with `python3 --version`.

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```
Then verify with `python3 --version`.

---

## Step 2 - Install Git (Optional but Recommended)

Git is only needed if you plan to clone this project from a repository (e.g., GitHub) instead of downloading a ZIP file. If you already have the project folder on your computer, you can **skip this step**.

1. Go to [https://git-scm.com/downloads](https://git-scm.com/downloads).
2. Download and run the installer for your operating system, accepting the default options.
3. Verify installation by opening a VS Code terminal and running:
   ```bash
   git --version
   ```
   You should see something like `git version 2.44.0`.

---

## Step 3 - Get the Project Files into VS Code

You should have a folder named `news-reader-cli/` containing all the project files (`main.py`, `news_service.py`, `config.py`, `utils.py`, `requirements.txt`, `README.md`, `.env.example`, `.gitignore`).

- If you downloaded this as a ZIP file, **extract it** to a location you'll remember (e.g., your Desktop or Documents folder).
- If you're using Git, clone it with:
  ```bash
  git clone <your-repository-url>
  cd news-reader-cli
  ```

Make sure all files listed above are directly inside the `news-reader-cli` folder (not nested in an extra subfolder).

---

## Step 4 - Open the Project in VS Code

1. Open VS Code.
2. Go to **File -> Open Folder...** (macOS: **File -> Open...**).
3. Navigate to and select the `news-reader-cli` folder.
4. Click **Select Folder** (or **Open** on macOS).
5. You should now see all the project files listed in the **Explorer** panel on the left side of VS Code.

---

## Step 5 - Open the VS Code Terminal

All the remaining commands in this guide are typed into the **VS Code integrated terminal**, not a separate application.

1. Open the menu **Terminal -> New Terminal** at the top of VS Code.
2. A terminal panel will appear at the bottom, already pointed at your project folder (you should see `news-reader-cli` somewhere in the prompt).

> 💡 Tip: If you ever get lost, run `pwd` (macOS/Linux) or `cd` (Windows) to see your current folder, and make sure it ends in `news-reader-cli`.

---

## Step 6 - Create a Virtual Environment

A **virtual environment** is an isolated space for this project's Python packages, so they don't interfere with other projects on your machine. We'll create one called `venv`.

In the VS Code terminal, run:

**Windows:**
```bash
python -m venv venv
```

**macOS/Linux:**
```bash
python3 -m venv venv
```

After a few seconds, a new `venv/` folder will appear in your project (you may need to click the refresh icon in the Explorer panel to see it). This is normal - it contains a private copy of Python and pip for this project only.

---

## Step 7 - Activate the Virtual Environment

Activating the virtual environment tells your terminal to use the isolated Python/pip inside `venv/` instead of your system-wide installation.

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```
> If PowerShell blocks the script with an execution policy error, see [Common Errors](#common-errors-and-their-solutions) below.

**macOS/Linux (bash/zsh):**
```bash
source venv/bin/activate
```

✅ **How to know it worked:** Your terminal prompt will now show `(venv)` at the very beginning, like this:

```
(venv) user@computer news-reader-cli %
```

You'll need to activate the virtual environment every time you open a new terminal to work on this project. VS Code often does this automatically if it detects the `venv/` folder - but it's good to check.

---

## Step 8 - Install Project Dependencies

With the virtual environment activated (you should see `(venv)` in your prompt), install all required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

This installs:
- **requests** - for making HTTP calls to the News API.
- **rich** - for the colorful, professional terminal output.
- **python-dotenv** - for loading your API key from the `.env` file.

You should see output ending with something like:
```
Successfully installed requests-2.31.0 rich-13.7.1 python-dotenv-1.0.1 ...
```

> 💡 If `pip` isn't recognized, try `pip3` or `python -m pip install -r requirements.txt` instead.

---

## Step 9 - Get a Free NewsAPI.org API Key

This application fetches real news using [NewsAPI.org](https://newsapi.org), which requires a free API key.

1. Go to [https://newsapi.org/register](https://newsapi.org/register).
2. Fill in the registration form (name, email, password) and submit it.
3. Check your email if verification is required, then log in.
4. Once logged in, go to your account page - your **API key** will be displayed. It looks something like:
   ```
   a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```
5. Copy this key - you'll paste it into your `.env` file in the next step.

> ⚠️ The free tier of NewsAPI.org has request limits (e.g., 100 requests/day and some restrictions on production use). This is perfectly fine for learning and personal use.

---

## Step 10 - Set Up Your `.env` File

Your API key is a secret and should **never** be typed directly into the code or committed to Git. Instead, it goes into a `.env` file that stays on your computer only.

1. In the VS Code Explorer panel, find the file `.env.example`.
2. Make a copy of it and rename the copy to exactly `.env` (no `.example` at the end). You can do this:
   - **In VS Code:** Right-click `.env.example` -> **Copy**, then right-click the folder -> **Paste**, then rename the new file to `.env`.
   - **Or via terminal:**
     ```bash
     # macOS/Linux
     cp .env.example .env

     # Windows
     copy .env.example .env
     ```
3. Open the new `.env` file in VS Code (click it in the Explorer panel).
4. Replace the placeholder with your real API key:
   ```env
   NEWS_API_KEY=your_api_key_here
   ```
   becomes, for example:
   ```env
   NEWS_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```
5. Save the file (`Ctrl+S` / `Cmd+S`).

> 🔒 The `.gitignore` file already excludes `.env` from Git, so your key will never be accidentally uploaded if you push this project to GitHub.

---

## Step 11 - Run the Application

With your virtual environment activated and dependencies installed, run:

**Windows:**
```bash
python main.py
```

**macOS/Linux:**
```bash
python3 main.py
```

You should see a colorful banner and a main menu appear in your terminal. 🎉

---

## Using the Application

Once running, you'll see a menu like this:

```
1  Search news by keyword
2  Top headlines by country
3  Top headlines by category
4  View supported categories
5  View supported countries
0  Exit
```

Type the number of the option you want and press **Enter**, then follow the on-screen prompts:

- **Option 1 (Search by keyword):** Type any topic (e.g., `artificial intelligence`), choose a sort order, and how many articles to fetch.
- **Option 2 (Top headlines by country):** Enter a two-letter country code (e.g., `us`, `gb`, `in`).
- **Option 3 (Top headlines by category):** Enter a category (e.g., `technology`, `sports`) and a country code.
- **Option 4 / 5:** View the full list of supported categories or countries.
- **Option 0:** Exit the application.

Each article is displayed with its **title, description, source, author, published date, and a clickable URL** to read the full story.

---

## Project Structure

```
news-reader-cli/
│
├── main.py              # Application entry point - CLI menu, Rich UI, orchestration
├── news_service.py       # NewsService class - all NewsAPI.org HTTP communication
├── config.py              # Settings, environment loading, constants (categories/countries)
├── utils.py                # Input validation and text/date formatting helpers
├── requirements.txt         # Python package dependencies
├── .env.example               # Template for your local .env file (safe to commit)
├── .env                         # Your real API key (created by you - never commit this)
├── .gitignore                    # Files/folders Git should ignore (.env, venv/, etc.)
└── README.md                       # This guide
```

**Why this structure?**
- `config.py` centralizes all settings so there's a single source of truth.
- `news_service.py` isolates all network/API logic - if NewsAPI.org changed its API, only this file would need updates.
- `utils.py` keeps validation and formatting logic reusable and testable, separate from the UI.
- `main.py` focuses purely on presentation and user interaction (Rich menus, prompts, panels).

---

## Expected Terminal Output Examples

**Main menu:**

```
╭──────────────────────────────╮
│      📰  NEWS READER CLI      │
│      Powered by NewsAPI.org   │
╰──────────────────────────────╯
╭──────────────── Main Menu ─────────────────╮
│  1   Search news by keyword                 │
│  2   Top headlines by country               │
│  3   Top headlines by category              │
│  4   View supported categories              │
│  5   View supported countries               │
│  0   Exit                                   │
╰──────────────────────────────────────────────╯
Select an option [0]:
```

**A search result article panel:**

```
╭─ 1. OpenAI announces new model update ────────────────────────╮
│ A brief summary of the article appears here, truncated to a   │
│ reasonable length for easy scanning...                        │
│                                                                │
│ Source: TechCrunch    Author: Jane Doe                        │
│ Published: Jul 08, 2026 - 14:23 UTC                           │
│ URL: https://techcrunch.com/example-article                   │
╰────────────────────────────────────────────────────────────────╯
```

**A configuration error (missing API key):**

```
╭───────────────────────────────────────────────────────────╮
│ Configuration error: NEWS_API_KEY is missing. Create a     │
│ '.env' file (see '.env.example') and set                   │
│ NEWS_API_KEY=<your_api_key>.                                │
╰───────────────────────────────────────────────────────────╯
```

---

## Common Errors and Their Solutions

| Error Message | Cause | Solution |
|---|---|---|
| `python: command not found` / `'python' is not recognized` | Python isn't installed or not added to PATH | Reinstall Python and check "Add python.exe to PATH" (Windows), or use `python3` instead of `python` (macOS/Linux) |
| `ModuleNotFoundError: No module named 'rich'` (or `requests`/`dotenv`) | Dependencies not installed, or virtual environment not activated | Activate your venv (Step 7), then run `pip install -r requirements.txt` again |
| `Configuration error: NEWS_API_KEY is missing` | No `.env` file, or it's empty | Copy `.env.example` to `.env` and add your real API key (Step 10) |
| `Configuration error: NEWS_API_KEY is still set to a placeholder value` | You didn't replace `your_api_key_here` | Open `.env` and paste your actual key from NewsAPI.org |
| `API error: Your API key is invalid` | Typo in the API key, or extra spaces/quotes around it | Re-copy the key exactly from your NewsAPI.org account page, no quotes needed |
| `API error: Your API key has exhausted its daily request quota` | Free tier daily limit (100 requests/day) reached | Wait until the quota resets (24 hours) or upgrade your NewsAPI.org plan |
| `The request to NewsAPI.org timed out` | Slow or no internet connection | Check your Wi-Fi/network connection and try again |
| PowerShell: `...cannot be loaded because running scripts is disabled on this system` | Windows execution policy blocks venv activation script | Run PowerShell as Administrator and execute: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then retry activation |
| `pip: command not found` | pip isn't available under that name | Try `pip3` or `python -m pip install -r requirements.txt` |
| Terminal doesn't show `(venv)` after activation | Wrong activation command for your OS/shell | Re-check Step 7 and match the command to your exact OS and shell (cmd vs PowerShell vs bash) |
| `No articles were found for this request` | Keyword too specific, or category/country combination has no current headlines | Try a broader keyword or a different country/category |

---

## Useful VS Code Terminal Commands Reference

| Command | Purpose |
|---|---|
| `python3 --version` | Check installed Python version |
| `python3 -m venv venv` | Create a virtual environment named `venv` |
| `source venv/bin/activate` | Activate venv (macOS/Linux) |
| `venv\Scripts\activate.bat` | Activate venv (Windows Command Prompt) |
| `venv\Scripts\Activate.ps1` | Activate venv (Windows PowerShell) |
| `deactivate` | Exit the virtual environment |
| `pip install -r requirements.txt` | Install all project dependencies |
| `pip list` | Show installed packages in the current environment |
| `python3 main.py` | Run the application |
| `pwd` | Show current directory (macOS/Linux) |
| `cd news-reader-cli` | Move into the project folder |
| `git clone <url>` | Download the project from a Git repository |

---

## License

This project is provided as-is for educational and personal use. You are free to modify and extend it. Please review [NewsAPI.org's terms of service](https://newsapi.org/terms) regarding acceptable use of their API.
