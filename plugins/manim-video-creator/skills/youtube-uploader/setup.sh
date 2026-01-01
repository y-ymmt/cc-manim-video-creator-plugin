#!/bin/bash
# YouTube Uploader Setup Script for macOS

echo "🚀 YouTube Data API Setup Script"
echo "================================"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first:"
    echo "   brew install python3"
    exit 1
fi

echo "✅ Python 3 detected: $(python3 --version)"

# Install required packages
echo ""
echo "📦 Installing required packages..."
pip3 install -q google-auth-oauthlib google-api-python-client

if [ $? -eq 0 ]; then
    echo "✅ Packages installed successfully"
else
    echo "❌ Failed to install packages"
    exit 1
fi

# Check credentials file
CREDS_FILE="${1:-credentials.json}"

if [ ! -f "$CREDS_FILE" ]; then
    echo ""
    echo "⚠️  Credentials file not found: $CREDS_FILE"
    echo ""
    echo "📋 To get your credentials:"
    echo "   1. Go to: https://console.cloud.google.com"
    echo "   2. Create a new project"
    echo "   3. Enable YouTube Data API v3"
    echo "   4. Create OAuth 2.0 Client ID (Desktop app)"
    echo "   5. Download the JSON file and save as: $CREDS_FILE"
    echo ""
    echo "After downloading credentials, run this script again."
else
    echo ""
    echo "✅ Credentials file found: $CREDS_FILE"
    echo ""
    echo "🎉 Setup complete! You can now use youtube_uploader.py"
    echo ""
    echo "Usage examples:"
    echo ""
    echo "1. Upload as private video:"
    echo "   python3 youtube_uploader.py ~/Videos/my_video.mp4 --title 'My Video'"
    echo ""
    echo "2. Upload as public with tags:"
    echo "   python3 youtube_uploader.py ~/Videos/my_video.mp4 \\"
    echo "     --title 'Awesome Video' \\"
    echo "     --description 'Check this out!' \\"
    echo "     --tags 'python,youtube,api' \\"
    echo "     --privacy public"
    echo ""
    echo "3. Schedule publish for specific time:"
    echo "   python3 youtube_uploader.py ~/Videos/my_video.mp4 \\"
    echo "     --title 'Scheduled Video' \\"
    echo "     --privacy private \\"
    echo "     --publish-at '2025-01-15T15:30:00Z'"
fi

echo ""
