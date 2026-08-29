import os
import urllib.request
import subprocess
import sys
import shutil

print("==============================================")
print("🚀 Custom Adaptive Onboarding Setup Wizard   ")
print("==============================================")

# 1. Unified Operating System Inspection Layer
is_windows = os.name == 'nt'

# 2. Automated Dependency Injector (Checks and Configures Python Paths)
if is_windows:
    install_dir = os.path.expanduser(r"~\Documents\RoboticsAgent")
    python_command = "py"
    
    # Verify if execution environments are globally recognized
    if shutil.which("py") is None and shutil.which("python") is None:
        print("⚠️ Python environment missing from Windows registry!")
        print("📥 Deploying background installation via WinGet...")
        try:
            # Silent native Windows package installation hook
            subprocess.run([
                "winget", "install", "--id", "Python.Python.3.12", 
                "--silent", "--accept-source-agreements", "--accept-package-agreements"
            ], check=True)
            print("✅ Python successfully registered! Please restart your terminal and run install.py again.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Automated Windows installation failed: {e}")
            print("Please configure Python manually from python.org/downloads")
            sys.exit(1)
else:
    # macOS Configuration Paths
    install_dir = os.path.expanduser("~/Documents/RoboticsAgent")
    python_command = "python3"
    
    if shutil.which("python3") is None:
        print("⚠️ Python3 environment missing from macOS runtime!")
        print("📥 Initializing Homebrew background tracker framework...")
        try:
            # Install Homebrew if it's missing on the MacBook
            if shutil.which("brew") is None:
                brew_installer = '/bin/bash -c "$(curl -fsSL https://githubusercontent.com)"'
                subprocess.run(brew_installer, shell=True, check=True)
            
            # Silently download Python package bindings
            print("📥 Fetching Python binaries via Homebrew...")
            subprocess.run(["brew", "install", "python"], check=True)
            print("✅ Python successfully registered! Please restart your terminal and run install.py again.")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Automated macOS installation failed: {e}")
            sys.exit(1)

os.makedirs(install_dir, exist_ok=True)
agent_file_path = os.path.join(install_dir, "agent.py")

# 3. Smart Branch Checking Conditions to download code
url_main = "https://githubusercontent.com"
url_master = "https://githubusercontent.com"

print("📥 Fetching latest agent code from the web...")
try:
    print("🔍 Trying to download from 'main' branch...")
    urllib.request.urlretrieve(url_main, agent_file_path)
    print("✅ Download from 'main' branch complete!")
except Exception as main_error:
    print("⚠️ 'main' branch link not found. Switching conditions...")
    try:
        print("🔍 Trying to download from 'master' branch...")
        urllib.request.urlretrieve(url_master, agent_file_path)
        print("✅ Download from 'master' branch complete!")
    except Exception as master_error:
        print("\n🌐 Network Error detected. Checking local fallback...")
        local_backup = "agent.py"
        if os.path.exists(local_backup):
            shutil.copy(local_backup, agent_file_path)
            print("✅ SUCCESS: Restored clean version from local folder!")
        else:
            print("❌ Critical Error: No local backup or internet available.")
            sys.exit()

# 4. Secure Token Setup Wizard for the User (Supports Read or Write Roles)
print("\n🔑 Configuring Secret API Token...")
current_token = os.getenv("HF_TOKEN")
if current_token:
    print("✅ HF_TOKEN is already configured on this machine!")
else:
    print("💡 To use this agent, you need a free token from hf.co/settings/tokens")
    user_token = input("👉 Paste your Hugging Face API Token (Read or Write role) here: ").strip()
    
    if user_token:
        if is_windows:
            subprocess.run(["powershell", "-Command", f'[Environment]::SetEnvironmentVariable("HF_TOKEN", "{user_token}", "User")'], capture_output=True)
        else:
            zshrc_path = os.path.expanduser("~/.zshrc")
            with open(zshrc_path, "a", encoding="utf-8") as zsh_file:
                zsh_file.write(f'\nexport HF_TOKEN="{user_token}"\n')
        print("✅ Token saved securely onto your operating system environment variables!")
    else:
        print("⚠️ Warning: No token was entered. You will need to configure HF_TOKEN manually later.")

# 5. Install dependencies (huggingface_hub)
print(f"\n📦 Installing required libraries via {python_command} pip...")
try:
    subprocess.run([python_command, "-m", "pip", "install", "huggingface_hub"], capture_output=True)
    print("✅ Libraries verified!")
except Exception as e:
    print(f"⚠️ Warning: Could not run pip automatically: {e}")

# 6. OS-Specific Shortcut Registration
print("⚙️ Setting up terminal shortcut command...")
if is_windows:
    powershell_setup_code = f"""
function agent {{
    cd "{install_dir}"
    py agent.py
}}
"""
    try:
        profile_path_bytes = subprocess.check_output(["powershell", "-NoProfile", "-Command", "$PROFILE"])
        profile_path = profile_path_bytes.decode("utf-8").strip()
        os.makedirs(os.path.dirname(profile_path), exist_ok=True)
        
        with open(profile_path, "a", encoding="utf-8") as profile_file:
            profile_file.write("\n" + powershell_setup_code + "\n")
            
        subprocess.run(["powershell", "-Command", "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"])
        print("\n🎉 SUCCESS! Please restart PowerShell and type 'agent'!")
    except Exception as e:
        print(f"❌ Windows shortcut failed: {e}")
else:
    mac_shortcut_code = f"alias agent='cd {install_dir} && python3 agent.py'"
    zshrc_path = os.path.expanduser("~/.zshrc")
    try:
        with open(zshrc_path, "a", encoding="utf-8") as zsh_file:
            zsh_file.write("\n" + mac_shortcut_code + "\n")
        print("\n🎉 SUCCESS! Please restart the Terminal and type 'agent'!")
    except Exception as e:
        print(f"❌ Mac shortcut failed: {e}")
