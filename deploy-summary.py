#!/usr/bin/env python3
"""
🚀 DEPLOYMENT SUMMARY SCRIPT

Shows the user exactly what they need to do to deploy to GitHub and Vercel.

Author: Ether (Crypto Trading Swarm Agent)
"""

import os
import subprocess
from pathlib import Path

def check_command(cmd):
    """Check if a command exists"""
    try:
        subprocess.run([cmd, '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🚀 PREDICTION VENUE DEPLOYMENT SUMMARY")
    print("=" * 45)
    print()
    
    print("📁 Current Status:")
    print("-" * 17)
    
    # Check git status
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            if result.stdout.strip():
                print("   📝 Git: Changes need to be committed")
            else:
                print("   ✅ Git: Repository is clean and ready")
        else:
            print("   ❌ Git: Not a git repository")
    except FileNotFoundError:
        print("   ❌ Git: Git is not installed")
    
    # Check GitHub CLI
    if check_command('gh'):
        print("   ✅ GitHub CLI: Available for automated setup")
    else:
        print("   ⚠️  GitHub CLI: Not installed (manual setup required)")
    
    # Check Vercel CLI
    if check_command('vercel'):
        print("   ✅ Vercel CLI: Available for automated deployment")
    else:
        print("   ⚠️  Vercel CLI: Not installed")
    
    # Check Node.js
    if check_command('node'):
        print("   ✅ Node.js: Available")
    else:
        print("   ❌ Node.js: Required for frontend build")
    
    print()
    print("🎯 DEPLOYMENT STEPS:")
    print("-" * 19)
    print()
    
    print("1️⃣ GITHUB DEPLOYMENT")
    print("    🐙 Upload your code to GitHub")
    print()
    if check_command('gh'):
        print("    🚀 Automatic (GitHub CLI available):")
        print("       ./github-setup.sh")
        print()
        print("    📖 Manual alternative:")
        print("       1. Go to https://github.com/new")
        print("       2. Create 'prediction-trading-venue' repository")
        print("       3. Follow the setup instructions")
    else:
        print("    📖 Manual setup required:")
        print("       1. Install GitHub CLI: brew install gh")
        print("       2. Login: gh auth login")
        print("       3. Run: ./github-setup.sh")
        print()
        print("    📖 OR manual setup:")
        print("       1. Go to https://github.com/new")
        print("       2. Create 'prediction-trading-venue' repository")
        print("       3. git remote add origin https://github.com/USERNAME/prediction-trading-venue.git")
        print("       4. git push -u origin main")
    
    print()
    print("2️⃣ VERCEL DEPLOYMENT")
    print("    🌐 Deploy frontend dashboard to Vercel")
    print()
    
    if check_command('vercel'):
        print("    🚀 Automatic (Vercel CLI available):")
        print("       ./deploy-to-vercel.sh")
    else:
        print("    📦 Install Vercel CLI first:")
        print("       npm install -g vercel")
        print("       ./deploy-to-vercel.sh")
    
    print()
    print("    📖 Alternative: Vercel Dashboard")
    print("       1. Go to https://vercel.com")
    print("       2. Click 'New Project'")
    print("       3. Import your GitHub repository")
    print("       4. Set Root Directory: 'frontend'")
    print("       5. Deploy!")
    
    print()
    print("🎯 WHAT YOU'LL GET:")
    print("-" * 17)
    print()
    print("   🐙 GitHub Repository:")
    print("      • Complete source code")
    print("      • Documentation")
    print("      • Issue tracking")
    print("      • Collaboration tools")
    print()
    print("   🌐 Live Vercel Dashboard:")
    print("      • Real-time prediction markets")
    print("      • Trading performance analytics")
    print("      • AI agent network monitoring")
    print("      • System health dashboard")
    print("      • Responsive mobile design")
    print()
    print("   ⚡ Features:")
    print("      • Automatic deployments on git push")
    print("      • SSL certificates")
    print("      • Global CDN")
    print("      • Performance optimization")
    print("      • Custom domain support")
    
    print()
    print("🚀 READY TO DEPLOY?")
    print("-" * 17)
    print()
    print("   Quick start:")
    print("   1. ./github-setup.sh       # Upload to GitHub")
    print("   2. ./deploy-to-vercel.sh    # Deploy to Vercel")
    print()
    print("   📖 Need help? Check DEPLOYMENT_GUIDE.md")
    print()
    print("⚡ Built by Ether - Crypto Trading Swarm Agent")
    print("🏛️ Ready to share your prediction venue with the world!")

if __name__ == "__main__":
    main()