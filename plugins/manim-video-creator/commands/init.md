---
description: 新規Manimプロジェクトをセットアップする
argument-hint: "[project-name]"
allowed-tools:
  - Bash
  - Write
  - Read
  - AskUserQuestion
---

# Manim Project Initialization

新規のManimプロジェクトを作成し、必要な依存関係をセットアップする。

## 手順

1. **プロジェクト名の確認**
   - 引数でプロジェクト名が指定されていない場合は `AskUserQuestion` で確認する
   - デフォルト: `manim-project`

2. **uvでプロジェクトを初期化**
   ```bash
   uv init --python 3.12 <project-name>
   cd <project-name>
   ```

3. **依存関係を追加**
   ```bash
   uv add manim edge-tts pydub
   ```

4. **OS検出とシステム依存パッケージの案内**
   - macOS: `brew install pkg-config cairo pango ffmpeg && brew install --cask mactex`
   - Linux: `sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg texlive-full`
   - Windows: MiKTeX と FFmpeg のインストールを案内

5. **基本ファイルを作成**
   - `scene.py`: 基本的なシーンテンプレート
   - `README.md`: プロジェクトの説明

6. **セットアップの確認**
   ```bash
   uv run manim checkhealth
   ```

## scene.py テンプレート

```python
from manim import *

# Japanese font setting
# config.font = "Hiragino Sans"  # macOS
# config.font = "Noto Sans CJK JP"  # Linux
# config.font = "Yu Gothic"  # Windows

# Dark mode (recommended)
config.background_color = "#1a1a2e"

# Color palette
PRIMARY = "#4fc3f7"
SECONDARY = "#81c784"
ACCENT = "#ffb74d"
HIGHLIGHT = "#f06292"


class MyScene(Scene):
    """
    Basic scene template.

    Render commands:
    - Preview: uv run manim -ql scene.py MyScene --disable_caching
    - High quality: uv run manim -qh scene.py MyScene --disable_caching
    """

    def construct(self):
        title = Text("Hello, Manim!", font_size=48, color=PRIMARY)
        self.play(Write(title))
        self.wait(2)
        self.play(FadeOut(title))
```

## 完了メッセージ

プロジェクトのセットアップが完了したら、以下を伝える：
- プロジェクトディレクトリの場所
- 基本的なレンダリングコマンド
- 動画作成を開始するには `/manim:create-video` を使用できること
