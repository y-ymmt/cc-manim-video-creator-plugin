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

### 質問6: エンディング動画（オプション）
- エンディング動画を追加する
- エンディング動画なし

## エンディング動画のディレクトリ構成

エンディング動画は**プラグイン内に共通配置**し、すべてのmanimプロジェクトで共有する：

```
${CLAUDE_PLUGIN_ROOT}/
└── endings/
    ├── 16_9/    # YouTube用（1920x1080）
    │   └── ending.mp4
    ├── 9_16/    # Shorts/TikTok用（1080x1920）
    │   └── ending.mp4
    └── 1_1/     # Instagram用（1080x1080）
        └── ending.mp4
```

**注意:**
- `${CLAUDE_PLUGIN_ROOT}` はプラグインのルートディレクトリ
- 各アスペクト比に対応したエンディング動画を事前に作成しておく
- ファイル名は `ending.mp4` 固定
- 対応するアスペクト比のエンディング動画がない場合はスキップされる

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

## ステップ4.5: シーンレビュー（品質チェック①）

シーンファイル作成後、**必ず** `scene-reviewer` エージェントを使用してコードレビューを実施する。

```
Task ツールを使用:
- subagent_type: "manim-video-creator:scene-reviewer"
- prompt: "scene.py をレビューしてください。タイミング構成、コード品質、アニメーション設計、ナレーション同期、視覚的品質（テキスト/オブジェクトの重なり・画面からのはみ出し）を確認し、問題点があれば報告してください。"
```

**レビュー対象:**
- docstringにタイミング構成が記載されているか
- 各セクションの累計時間が正確か
- run_time パラメータが適切に設定されているか
- 日本語フォント設定があるか
- カラーパレットが定義されているか
- テキストやオブジェクトの重なりがないか
- 要素が画面境界からはみ出していないか

**問題が見つかった場合:**
1. レビュー結果に基づいて scene.py を修正
2. 修正後、再度 scene-reviewer でレビュー
3. 問題がなくなるまで繰り返す

## ステップ5: プレビューレンダリング

低品質でプレビューをレンダリング：

```bash
uv run manim -ql scene.py MyScene --disable_caching
```

## ステップ5.5: タイミング分析（品質チェック②）

プレビューレンダリング後、**必ず** `timing-analyzer` エージェントを使用してナレーションとアニメーションの同期を確認する。

```
Task ツールを使用:
- subagent_type: "manim-video-creator:timing-analyzer"
- prompt: "measure_audio.py（またはgenerate_audio.py）のナレーション台本と、scene.py のタイミングを分析してください。ナレーションとアニメーションの同期のずれがあれば報告し、修正案を提示してください。"
```

**分析対象:**
- 各ナレーションの開始時間と長さ
- アニメーションの累計時間
- ナレーションとアニメーションのずれ（±0.3秒以上は問題）
- ナレーションの重複（次のナレーション開始前に現在のが終わらない）
- 長すぎる無音区間（3秒以上）

**問題が検出された場合:**
1. scene.py の wait() 時間を調整
2. generate_audio.py のタイムスタンプを調整
3. 修正後、再度プレビューをレンダリングして確認
4. timing-analyzer で再分析

## ステップ6: 高品質レンダリング

タイミング分析で問題がないことを確認後、高品質で最終レンダリング：

```bash
uv run manim -qh scene.py MyScene --disable_caching
```

## ステップ7: 音声生成（フル版）

1. `generate_audio.py` でナレーション生成
2. BGM生成（必要な場合）
3. ナレーションとBGMを合成

## ステップ8: 最終合成（エンディング動画結合を含む）

### 8-1: 動画と音声の合成

```bash
ffmpeg -i video.mp4 -i combined_audio.mp3 \
  -c:v copy -c:a aac -b:a 192k \
  -map 0:v:0 -map 1:a:0 \
  -shortest -y main_with_audio.mp4
```

### 8-2: エンディング動画の結合（オプション）

ユーザーがエンディング動画を追加する場合のみ実行：

1. **動画のアスペクト比を判定**

```bash
# 動画の幅と高さを取得
WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 main_with_audio.mp4)
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 main_with_audio.mp4)

# アスペクト比を計算して適切なディレクトリを選択
# WIDTH > HEIGHT → 16:9 (横長)
# WIDTH < HEIGHT → 9:16 (縦長)
# WIDTH == HEIGHT → 1:1 (正方形)
```

2. **アスペクト比に基づいてエンディング動画を選択**

| メイン動画 | エンディング動画パス |
|------------|----------------------|
| 横長 (16:9) | `${CLAUDE_PLUGIN_ROOT}/endings/16_9/ending.mp4` |
| 縦長 (9:16) | `${CLAUDE_PLUGIN_ROOT}/endings/9_16/ending.mp4` |
| 正方形 (1:1) | `${CLAUDE_PLUGIN_ROOT}/endings/1_1/ending.mp4` |

3. **動画の結合**

```bash
# プラグインルートからエンディング動画のパスを設定
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT}"
ENDING_PATH="${PLUGIN_ROOT}/endings/${ASPECT_DIR}/ending.mp4"

# エンディング動画が存在する場合のみ実行
if [ -f "$ENDING_PATH" ]; then
  # 結合用のリストファイルを作成
  echo "file 'main_with_audio.mp4'" > concat_list.txt
  echo "file '$ENDING_PATH'" >> concat_list.txt

  # 動画を結合
  ffmpeg -f concat -safe 0 -i concat_list.txt \
    -c copy -y final_output.mp4

  # クリーンアップ
  rm concat_list.txt main_with_audio.mp4
else
  # エンディング動画がない場合はそのまま使用
  mv main_with_audio.mp4 final_output.mp4
  echo "警告: 対応するエンディング動画が見つかりませんでした: $ENDING_PATH"
fi
```

**注意:**
- メイン動画とエンディング動画のコーデック・解像度・フレームレートが一致している必要がある
- 一致しない場合は再エンコードが必要（処理時間が長くなる）

```bash
# 再エンコードが必要な場合
ffmpeg -f concat -safe 0 -i concat_list.txt \
  -c:v libx264 -preset medium -crf 18 \
  -c:a aac -b:a 192k \
  -y final_output.mp4
```

## ステップ9: 完了報告

動画作成完了時に以下を伝える：
- 出力ファイルの場所
- 動画の長さ
- 著作権に関する注意事項（BGM、TTS音声について）

## 重要な注意事項

### 品質チェックは必須

以下の2つの品質チェックは**スキップ不可**。問題が見つかった場合は必ず修正してから次のステップに進むこと：

1. **ステップ4.5: シーンレビュー（scene-reviewer）**
   - シーンファイル作成直後に実施
   - コード品質、タイミング構成、アニメーション設計を確認
   - 問題があれば修正してから次へ

2. **ステップ5.5: タイミング分析（timing-analyzer）**
   - プレビューレンダリング後に実施
   - ナレーションとアニメーションの同期を確認
   - 問題があれば修正してから高品質レンダリングへ

### その他の注意事項

- 各ステップで進捗を報告する
- タイミングのずれが生じた場合は調整を提案する
- 品質チェックで問題がなくなるまで繰り返し修正を行う
