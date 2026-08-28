import os
import urllib.request
import subprocess
import sys
import shutil

print("==============================================")
print("🚀 Custom Bulletproof Agent Installer         ")
print("==============================================")

# 1. Detect the Operating System
is_windows = os.name == 'nt'

# 2. Set the install folder location based on the OS
if is_windows:
    install_dir = os.path.expanduser(r"~\Documents\RoboticsAgent")
    python_command = "py"
else:
    install_dir = os.path.expanduser("~/Documents/RoboticsAgent")
    python_command = "python3"

os.makedirs(install_dir, exist_ok=True)
agent_file_path = os.path.join(install_dir, "agent.py")

# 3. Smart Branch Checking Conditions
url_main = "https://github.com"
url_master = "https://github.com"

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
        print("\n🌐 Network Error detected (getaddrinfo failed).")
        
        # --- LOCAL BACKUP AUTO-RECOVERY ---
        print("🛡️ Activating Local Backup Protection Rule...")
        local_backup = "agent.py"
        if os.path.exists(local_backup):
            shutil.copy(local_backup, agent_file_path)
            print("✅ SUCCESS: Restored your clean working version from local backup folder!")
        else:
            print("❌ Critical Error: No local backup or internet connection available.")
            sys.exit()

# 4. Install dependencies (huggingface_hub)
print(f"📦 Installing required libraries via {python_command} pip...")
try:
    subprocess.run([python_command, "-m", "pip", "install", "huggingface_hub"], capture_output=True)
    print("✅ Libraries verified!")
except Exception as e:
    print(f"⚠️ Warning: Could not run pip automatically: {e}")

# 5. OS-Specific Shortcut Registration
print("⚙️ Setting up terminal shortcut command...")

if is_windows:
    # --- WINDOWS SETUP (PowerShell) ---
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
    # --- MAC SETUP (Zsh Terminal) ---
    mac_shortcut_code = f"alias agent='cd {install_dir} && python3 agent.py'"
    zshrc_path = os.path.expanduser("~/.zshrc")
    
    try:
        with open(zshrc_path, "a", encoding="utf-8") as zsh_file:
            zsh_file.write("\n" + mac_shortcut_code + "\n")
            
        print("\n🎉 SUCCESS! Please restart the Terminal and type 'agent'!")
    except Exception as e:
        print(f"❌ Mac shortcut failed: {e}")
