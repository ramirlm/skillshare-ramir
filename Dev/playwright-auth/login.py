#!/usr/bin/env python3
"""Save browser authentication for any website using Playwright"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Pre-configured login URLs
LOGIN_URLS = {
    "twitter": "https://twitter.com/login",
    "linkedin": "https://linkedin.com/login",
    "facebook": "https://facebook.com/login",
    "instagram": "https://instagram.com/accounts/login",
    "github": "https://github.com/login",
    "reddit": "https://reddit.com/login",
}

def main():
    if len(sys.argv) < 2:
        print("🔐 Playwright Authentication Saver")
        print("=" * 60)
        print("\nUsage: python3 login.py <site-name> [login-url]")
        print("\nPre-configured sites:")
        for site in LOGIN_URLS.keys():
            print(f"  • {site}")
        print("\nExamples:")
        print("  python3 login.py twitter")
        print("  python3 login.py mysite https://example.com/login")
        print("\nSaves to: ~/web-auth/<site-name>.json")
        sys.exit(1)
    
    site_name = sys.argv[1]
    login_url = sys.argv[2] if len(sys.argv) > 2 else LOGIN_URLS.get(site_name)
    
    if not login_url:
        print(f"❌ No login URL found for '{site_name}'")
        print(f"   Provide URL: python3 login.py {site_name} https://example.com/login")
        sys.exit(1)
    
    # Create auth directory
    auth_dir = Path.home() / "web-auth"
    auth_dir.mkdir(exist_ok=True)
    auth_file = auth_dir / f"{site_name}.json"
    
    print(f"🔐 Saving authentication for: {site_name}")
    print(f"   Login URL: {login_url}")
    print("=" * 60)
    
    with sync_playwright() as p:
        # Launch browser with visible window
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # Open login page
        page.goto(login_url)
        print("✓ Browser window opened!")
        print("\n⏸️  Login manually in the browser window")
        print("   Press ENTER here when you're logged in...")
        
        # Wait for user
        input()
        
        # Save authentication
        context.storage_state(path=str(auth_file))
        print(f"\n✅ Authentication saved!")
        print(f"   File: {auth_file}")
        
        # Test
        print(f"\n🧪 Testing authentication...")
        page.reload()
        page.wait_for_load_state("networkidle")
        
        # Screenshot
        screenshot_path = f"/tmp/{site_name}-auth.png"
        page.screenshot(path=screenshot_path)
        print(f"✓ Screenshot saved: {screenshot_path}")
        
        browser.close()
        
        print(f"\n🎉 Done!")
        print(f"\nUse this file in your scripts:")
        print(f"  storage_state='{auth_file}'")

if __name__ == "__main__":
    main()
