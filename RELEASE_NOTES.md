# 🚀 Release Notes - Version 1.1.0

## 🛡️ Critical Security & Global Deployment Update

This production update patch eliminates hardcoded system assets and transitions the architecture to a secure environment variable pattern.

### ⚙️ What's New
- 🔒 **Zero-Trust Token Security**: Hardcoded strings removed from `agent.py`. The engine now dynamically streams tokens using `os.getenv`.
- 🔑 **Interactive Onboarding**: `install.py` now includes an interactive setup wizard prompt that guides users to save their tokens securely.
- 🎯 **API Syntax Fix**: Patched choice index tracking layout with `choices[0]` array handling.
