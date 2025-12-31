# Manim Video Creator Plugin

Manim（Mathematical Animation Engine）を使用してTTSナレーション・BGM付きのアニメーション動画を作成するClaude Codeプラグイン。

## 機能

- **2D/3Dアニメーション**: Manim Community ライブラリを使用
- **TTSナレーション**: edge-tts による高品質音声合成
- **BGM生成**: 著作権フリーのアンビエントBGM自動生成
- **タイミング同期**: ナレーションとアニメーションの自動同期

## 使用例

- 解説動画・教育コンテンツ
- プレゼンテーション動画
- ロゴアニメーション
- インフォグラフィック
- アルゴリズム・データ構造の可視化
- 3Dアニメーション

## インストール

```bash
# プラグインをインストール
claude plugin install manim-video-creator
```

## コマンド

### `/manim:init [project-name]`

新規Manimプロジェクトをセットアップします。

```bash
# 使用例
/manim:init my-video-project
```

- uvでプロジェクトを初期化
- manim, edge-tts, pydub を依存関係に追加
- 基本的なシーンテンプレートを作成

### `/manim:create-video`

動画作成ワークフローを開始します。

```bash
# 使用例
/manim:create-video
```

1. ヒアリング（動画の種類、音声設定など）
2. 台本作成
3. シーン設計
4. レンダリング
5. 音声生成・合成

## エージェント

### scene-reviewer

Manimシーンのコードレビューを行います。

- タイミング構成の確認
- ベストプラクティスへの準拠
- 潜在的な問題の検出

### timing-analyzer

ナレーションとアニメーションのタイミング同期を分析します。

- ナレーション長の測定
- ずれの検出
- 修正提案

## システム要件

### 必須

- Python 3.12+
- uv（推奨パッケージマネージャー）
- FFmpeg

### OS別依存パッケージ

**macOS:**
```bash
brew install pkg-config cairo pango ffmpeg
brew install --cask mactex
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libcairo2-dev libpango1.0-dev ffmpeg texlive-full
```

**Windows:**
- MiKTeX: https://miktex.org/download
- FFmpeg: https://ffmpeg.org/download.html

## ファイル構成

```
manim-video-creator-plugin/
├── .claude-plugin/
│   └── plugin.json          # プラグインマニフェスト
├── skills/
│   └── manim-video-creator/
│       ├── SKILL.md          # メインスキル
│       ├── references/       # 参照ドキュメント
│       │   ├── animations.md
│       │   ├── mobjects.md
│       │   ├── text-and-math.md
│       │   ├── 3d-scenes.md
│       │   └── graphing.md
│       └── templates/        # テンプレート
│           ├── scene_template.py
│           ├── measure_audio.py
│           └── generate_audio.py
├── commands/
│   ├── init.md               # プロジェクト初期化コマンド
│   └── create-video.md       # 動画作成コマンド
├── agents/
│   ├── scene-reviewer.md     # シーンレビューエージェント
│   └── timing-analyzer.md    # タイミング分析エージェント
└── README.md
```

## 著作権に関する注意

### BGM
- 自動生成BGMは著作権フリーで商用・非商用問わず使用可能
- 外部BGMを使用する場合は各サイトの利用規約を確認

### TTSナレーション
- edge-tts で生成した音声はMicrosoftの利用規約に従う
- 商用利用の場合はAzure Speech Servicesの有料プランを検討
