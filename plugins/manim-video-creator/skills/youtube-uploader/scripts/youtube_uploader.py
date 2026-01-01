#!/usr/bin/env python3
"""
YouTube Video Uploader Skill for Claude Code
Uploads MP4 videos to YouTube with custom metadata using YouTube Data API v3

Usage:
    python youtube_uploader.py /path/to/video.mp4 \
        --title "My Video Title" \
        --description "Video description" \
        --tags "tag1,tag2,tag3" \
        --privacy private \
        --category 22 \
        --credentials /path/to/credentials.json

Metadata Options:
    --title: Video title (required)
    --description: Video description (optional)
    --tags: Comma-separated tags (optional)
    --privacy: private, unlisted, or public (default: private)
    --category: YouTube category ID (default: 22 = People & Blogs)
        See: https://developers.google.com/youtube/v3/docs/videoCategories
    --credentials: Path to OAuth 2.0 credentials JSON file (default: credentials.json)
    --playlist: Add to existing playlist (optional, requires playlist ID)
    --publish-at: Schedule publish time in ISO 8601 format (optional)
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Optional

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


def find_credentials_file(explicit_path: Optional[str] = None) -> str:
    """
    Find credentials.json file with the following priority:
    1. Explicitly specified path (--credentials option)
    2. Current project directory: ./credentials.json
    3. Home directory: ~/credentials.json
    4. Config directory: ~/.config/youtube/credentials.json
    5. Plugin directory: ${CLAUDE_PLUGIN_ROOT}/credentials.json

    Returns:
        Path to the credentials file

    Raises:
        FileNotFoundError: If no credentials file is found
    """
    search_paths = []

    # 1. Explicitly specified path
    if explicit_path and explicit_path != "credentials.json":
        if os.path.exists(explicit_path):
            print(f"Using specified credentials: {explicit_path}")
            return explicit_path
        search_paths.append(explicit_path)

    # 2. Current project directory
    project_creds = Path("./credentials.json")
    if project_creds.exists():
        print(f"Using project credentials: {project_creds.absolute()}")
        return str(project_creds.absolute())
    search_paths.append(str(project_creds))

    # 3. Home directory
    home_creds = Path.home() / "credentials.json"
    if home_creds.exists():
        print(f"Using home directory credentials: {home_creds}")
        return str(home_creds)
    search_paths.append(str(home_creds))

    # 4. Config directory
    config_creds = Path.home() / ".config" / "youtube" / "credentials.json"
    if config_creds.exists():
        print(f"Using config directory credentials: {config_creds}")
        return str(config_creds)
    search_paths.append(str(config_creds))

    # Also check for client_secrets.json in config directory
    config_secrets = Path.home() / ".config" / "youtube" / "client_secrets.json"
    if config_secrets.exists():
        print(f"Using config directory credentials: {config_secrets}")
        return str(config_secrets)
    search_paths.append(str(config_secrets))

    # 5. Plugin directory (via CLAUDE_PLUGIN_ROOT environment variable)
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if plugin_root:
        plugin_creds = Path(plugin_root) / "credentials.json"
        if plugin_creds.exists():
            print(f"Using plugin directory credentials: {plugin_creds}")
            return str(plugin_creds)
        search_paths.append(str(plugin_creds))

    # No credentials found
    raise FileNotFoundError(
        f"credentials.json not found in any of the following locations:\n"
        + "\n".join(f"  - {p}" for p in search_paths)
        + "\n\nPlease place credentials.json in one of these locations:\n"
        + "  1. Current project directory: ./credentials.json\n"
        + "  2. Home directory: ~/credentials.json\n"
        + "  3. Config directory: ~/.config/youtube/credentials.json\n"
        + "  4. Plugin directory: ${CLAUDE_PLUGIN_ROOT}/credentials.json\n"
        + "\nOr specify the path with --credentials option."
    )


class YouTubeUploader:
    """Handles YouTube video uploads with OAuth 2.0 authentication"""

    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    # YouTube category IDs
    CATEGORY_IDS = {
        "film": "1",
        "autos": "2",
        "music": "10",
        "pets": "15",
        "sports": "17",
        "travel": "19",
        "gaming": "20",
        "people": "22",  # People & Blogs (default)
        "comedy": "23",
        "entertainment": "24",
        "news": "25",
        "howto": "26",
        "education": "27",
        "science": "28",
    }

    def __init__(self, credentials_file: str):
        """Initialize uploader with credentials file"""
        self.credentials_file = credentials_file
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API using OAuth 2.0"""
        credentials = None
        token_file = self.credentials_file.replace("credentials.json", "token.json")
        
        # Try to load existing token
        if os.path.exists(token_file):
            credentials = Credentials.from_authorized_user_file(token_file, self.SCOPES)
        
        # Refresh or create new credentials
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        f"Please download it from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                credentials = flow.run_local_server(port=0)
            
            # Save token for future use
            with open(token_file, "w") as f:
                f.write(credentials.to_json())
        
        self.youtube = build(self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials)
    
    def upload(
        self,
        file_path: str,
        title: str,
        description: str = "",
        tags: Optional[list] = None,
        category: int = 22,
        privacy_status: str = "private",
        playlist_id: Optional[str] = None,
        publish_at: Optional[str] = None,
    ) -> str:
        """
        Upload video to YouTube
        
        Args:
            file_path: Path to MP4 video file
            title: Video title
            description: Video description
            tags: List of tags
            category: YouTube category ID (default: 22)
            privacy_status: 'private', 'unlisted', or 'public'
            playlist_id: Optional playlist ID to add video to
            publish_at: Optional ISO 8601 datetime for scheduled publish
        
        Returns:
            Video ID on success
        """
        # Validate file
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Video file not found: {file_path}")
        
        file_size = os.path.getsize(file_path)
        print(f"📹 Uploading: {Path(file_path).name} ({file_size / (1024**2):.1f} MB)")
        
        # Build request body
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags or [],
                "categoryId": str(category),
            },
            "status": {
                "privacyStatus": privacy_status,
            },
        }
        
        # Add scheduled publish time if provided
        if publish_at:
            body["status"]["publishAt"] = publish_at
        
        # Upload video
        media = MediaFileUpload(file_path, chunksize=256 * 1024, resumable=True)
        request = self.youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )
        
        # Execute with progress tracking
        response = None
        while response is None:
            try:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    print(f"⏳ Progress: {progress}%")
            except HttpError as e:
                if e.resp.status in [500, 502, 503, 504]:
                    print("⚠️  Server error, retrying...")
                else:
                    raise
        
        video_id = response["id"]
        print(f"✅ Upload successful! Video ID: {video_id}")
        print(f"   URL: https://www.youtube.com/watch?v={video_id}")
        
        # Add to playlist if specified
        if playlist_id:
            self._add_to_playlist(video_id, playlist_id)
        
        return video_id
    
    def _add_to_playlist(self, video_id: str, playlist_id: str):
        """Add uploaded video to a playlist"""
        try:
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id,
                        },
                    }
                },
            )
            request.execute()
            print(f"✅ Added to playlist: {playlist_id}")
        except HttpError as e:
            print(f"⚠️  Could not add to playlist: {e}")


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Upload MP4 video to YouTube with custom metadata",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload as private video
  python youtube_uploader.py video.mp4 --title "My Video"
  
  # Upload as public with tags
  python youtube_uploader.py video.mp4 \\
    --title "Awesome Video" \\
    --description "This is my awesome video" \\
    --tags "python,youtube,api" \\
    --privacy public
  
  # Schedule publish for specific time
  python youtube_uploader.py video.mp4 \\
    --title "Scheduled Video" \\
    --privacy private \\
    --publish-at "2025-01-15T15:30:00Z"
  
  # Add to playlist
  python youtube_uploader.py video.mp4 \\
    --title "Playlist Video" \\
    --playlist "PLxxxxxxxxxxxx"
        """,
    )
    
    # Required arguments
    parser.add_argument("file", help="Path to MP4 video file")
    
    # Metadata arguments
    parser.add_argument("--title", required=True, help="Video title (required)")
    parser.add_argument("--description", default="", help="Video description")
    parser.add_argument(
        "--tags",
        default="",
        help="Comma-separated tags (e.g., 'python,youtube,api')",
    )
    
    # Status arguments
    parser.add_argument(
        "--privacy",
        choices=["private", "unlisted", "public"],
        default="private",
        help="Privacy status (default: private)",
    )
    parser.add_argument(
        "--category",
        type=int,
        default=22,
        help="YouTube category ID (default: 22 = People & Blogs)",
    )
    parser.add_argument(
        "--publish-at",
        help="Schedule publish (ISO 8601 format, e.g., '2025-01-15T15:30:00Z')",
    )
    
    # Optional arguments
    parser.add_argument(
        "--credentials",
        default="credentials.json",
        help="Path to OAuth 2.0 credentials JSON file",
    )
    parser.add_argument(
        "--playlist",
        help="Playlist ID to add video to (optional)",
    )
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_args()

    try:
        # Parse tags
        tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else []

        # Find credentials file (auto-search if not explicitly specified)
        credentials_path = find_credentials_file(args.credentials)

        # Initialize uploader
        uploader = YouTubeUploader(credentials_path)
        
        # Upload video
        video_id = uploader.upload(
            file_path=args.file,
            title=args.title,
            description=args.description,
            tags=tags,
            category=args.category,
            privacy_status=args.privacy,
            playlist_id=args.playlist,
            publish_at=args.publish_at,
        )
        
        return 0
    
    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1
    except HttpError as e:
        print(f"❌ YouTube API Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
