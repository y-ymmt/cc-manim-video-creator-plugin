---
description: 動画作成ワークフローを開始する（ヒアリング→台本→シーン→音声→合成）
allowed-tools:
  - Bash
  - Write
  - Read
  - Edit
  - AskUserQuestion
  - Glob
  - Grep
---

# Manim Video Creation Workflow

TTSナレーション・BGM付きのManimアニメーション動画を作成するための包括的なワークフロー。

## ステップ1: ヒアリング

`AskUserQuestion` ツールを使用して以下の情報を収集する：

### 質問1: 動画の種類
- 解説・教育動画（論文解説、チュートリアル等）
- プレゼンテーション動画
- ロゴアニメーション
- インフォグラフィック・データ可視化
- アルゴリズム・コード可視化
- その他

### 質問2: 作成範囲
- Manim動画のみ（音声なし）
- Manim動画 + 台本
- フル版（Manim + TTSナレーション + BGM）

### 質問3: ナレーション音声（フル版の場合）
- 日本語女性（ja-JP-NanamiNeural）- 推奨
- 日本語男性（ja-JP-KeitaNeural）
- 英語女性（en-US-JennyNeural）
- 英語男性（en-US-GuyNeural）

### 質問4: BGMの種類（フル版の場合）
- 自動生成（アンビエント）- 著作権フリー
- BGMなし
- 外部BGMを後から追加

### 質問5: プラットフォーム/アスペクト比
- YouTube（16:9, 1920x1080）- 推奨
- YouTube Shorts/TikTok（9:16, 1080x1920）
- Instagram投稿（1:1, 1080x1080）
- カスタム

## ステップ2: コンテンツ確認

ユーザーから動画の内容について詳細を確認：
- 主なトピック
- 説明したいポイント
- 参考資料（論文、ウェブページなど）

## ステップ3: 台本作成

1. ナレーション台本を作成
2. 各セグメントのテキストをリスト化
3. `measure_audio.py` を使用して各セグメントの長さを測定

```python
# measure_audio.py を使用
NARRATIONS = [
    "最初のナレーション。",
    "2番目のナレーション。",
    # ...
]
```

## ステップ4: シーン設計

1. タイミング構成を設計（ナレーション長に基づく）
2. 各セクションの開始・終了時間を計算
3. シーンスクリプトを作成

```python
class MyScene(Scene):
    """
    タイミング構成:
    - セクション1: 0-8秒
    - セクション2: 8-20秒
    ...
    """
    def construct(self):
        self.section1()  # 8秒
        self.section2()  # 12秒
```

## ステップ5: レンダリング

1. 低品質でプレビュー
   ```bash
   uv run manim -ql scene.py MyScene --disable_caching
   ```

2. タイミングを確認・調整

3. 高品質で最終レンダリング
   ```bash
   uv run manim -qh scene.py MyScene --disable_caching
   ```

## ステップ6: 音声生成（フル版）

1. `generate_audio.py` でナレーション生成
2. BGM生成（必要な場合）
3. ナレーションとBGMを合成

## ステップ7: 最終合成

```bash
ffmpeg -i video.mp4 -i combined_audio.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 \
  -shortest -y final_output.mp4
```

## ステップ8: 完了報告

動画作成完了時に以下を伝える：
- 出力ファイルの場所
- 動画の長さ
- 著作権に関する注意事項（BGM、TTS音声について）

## 重要な注意事項

- 各ステップで進捗を報告する
- タイミングのずれが生じた場合は調整を提案する
- scene-reviewer エージェントを使用してシーンをレビューする
- timing-analyzer エージェントを使用してタイミングを分析する
