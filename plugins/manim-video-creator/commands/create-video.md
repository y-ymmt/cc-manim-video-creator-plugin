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

**重要**: 動画作成を開始する前に、**必ず** `AskUserQuestion` ツールを使用して以下の情報を収集すること。

```
AskUserQuestion ツールを以下のパラメータで呼び出す：

questions:
  - question: "どのような種類の動画を作成しますか？"
    header: "動画種類"
    multiSelect: false
    options:
      - label: "解説・教育動画"
        description: "論文解説、チュートリアル、概念説明など"
      - label: "プレゼンテーション動画"
        description: "スライド形式のプレゼン動画"
      - label: "ロゴアニメーション"
        description: "ロゴや短いモーショングラフィック"
      - label: "アルゴリズム・コード可視化"
        description: "アルゴリズムやデータ構造の動的可視化"

  - question: "作成範囲を選択してください"
    header: "作成範囲"
    multiSelect: false
    options:
      - label: "フル版（Manim + TTSナレーション + BGM）"
        description: "動画、音声、BGMすべてを含む完全版（推奨）"
      - label: "Manim動画 + 台本"
        description: "動画と台本のみ、音声は別途追加"
      - label: "Manim動画のみ"
        description: "音声なしのアニメーション動画のみ"

  - question: "どのプラットフォーム向けに作成しますか？"
    header: "プラットフォーム"
    multiSelect: false
    options:
      - label: "YouTube（16:9, 1920x1080）"
        description: "標準的なYouTube動画向け（推奨）"
      - label: "YouTube Shorts/TikTok（9:16, 1080x1920）"
        description: "縦長のショート動画向け"
      - label: "Instagram投稿（1:1, 1080x1080）"
        description: "正方形のInstagram投稿向け"

  - question: "エンディング動画を追加しますか？"
    header: "エンディング"
    multiSelect: false
    options:
      - label: "エンディング動画を追加する（推奨）"
        description: "プロジェクトまたはプラグインのendingsディレクトリから自動選択"
      - label: "エンディング動画なし"
        description: "メイン動画のみで終了"
```

**フル版選択時のみ追加で確認:**

```
questions:
  - question: "ナレーション音声を選択してください"
    header: "音声"
    multiSelect: false
    options:
      - label: "日本語女性（ja-JP-NanamiNeural）"
        description: "明瞭で聞きやすい日本語女性音声（推奨）"
      - label: "日本語男性（ja-JP-KeitaNeural）"
        description: "落ち着いた日本語男性音声"
      - label: "英語女性（en-US-JennyNeural）"
        description: "ナチュラルな英語女性音声"

  - question: "BGMの種類を選択してください"
    header: "BGM"
    multiSelect: false
    options:
      - label: "自動生成（アンビエント）"
        description: "著作権フリーのアンビエントBGMを自動生成"
      - label: "BGMなし"
        description: "ナレーションのみ"
      - label: "外部BGMを後から追加"
        description: "動画作成後に別途BGMを追加"
```

### ヒアリング結果の記録

ヒアリングで得た回答を以下の形式で記録し、後続のステップで参照する：

```
【ヒアリング結果】
- 動画種類: [解説・教育動画 / プレゼン / ロゴ / アルゴリズム可視化]
- 作成範囲: [フル版 / 動画+台本 / 動画のみ]
- プラットフォーム: [YouTube 16:9 / Shorts 9:16 / Instagram 1:1]
- エンディング動画: [追加する / なし]  ← ステップ8で使用
- ナレーション音声: [音声ID]（フル版のみ）
- BGM: [自動生成 / なし / 外部]（フル版のみ）
```

## エンディング動画のディレクトリ構成

エンディング動画は**以下の優先順位**で検索される：

### 1. プロジェクトディレクトリ（優先）

現在のmanimプロジェクトディレクトリに `endings/` フォルダがある場合、そちらを優先使用：

```
./                          # 現在のプロジェクトディレクトリ
└── endings/
    ├── 16_9/
    │   └── ending.mp4
    ├── 9_16/
    │   └── ending.mp4
    └── 1_1/
        └── ending.mp4
```

### 2. プラグインディレクトリ（フォールバック）

プロジェクトにエンディング動画がない場合、プラグインディレクトリから取得：

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
- プロジェクト固有のエンディングがある場合は `./endings/` に配置
- 共通のエンディングは `${CLAUDE_PLUGIN_ROOT}/endings/` に配置
- 各アスペクト比に対応したエンディング動画を事前に作成しておく
- ファイル名は `ending.mp4` 固定
- どちらにもエンディング動画がない場合はスキップされる

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

### 8-2: エンディング動画の結合

**重要**: ステップ1のヒアリングで「エンディング動画を追加する」を選択した場合のみ実行する。

```
【ヒアリング結果の確認】
ステップ1で記録した「エンディング動画」の回答を確認：
- 「追加する」の場合 → 以下の処理を実行
- 「なし」の場合 → このステップをスキップし、main_with_audio.mp4 を final_output.mp4 としてリネーム
```

#### エンディング動画の結合手順

1. **動画のアスペクト比を判定**

```bash
# 動画の幅と高さを取得
WIDTH=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 main_with_audio.mp4)
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 main_with_audio.mp4)

# アスペクト比を判定
if [ "$WIDTH" -gt "$HEIGHT" ]; then
  ASPECT_DIR="16_9"
elif [ "$WIDTH" -lt "$HEIGHT" ]; then
  ASPECT_DIR="9_16"
else
  ASPECT_DIR="1_1"
fi
```

2. **エンディング動画を検索（優先順位順）**

以下の順序でエンディング動画を探す：

| 優先度 | 検索場所 | パス |
|--------|----------|------|
| 1 | プロジェクトディレクトリ | `./endings/${ASPECT_DIR}/ending.mp4` |
| 2 | プラグインディレクトリ | `${CLAUDE_PLUGIN_ROOT}/endings/${ASPECT_DIR}/ending.mp4` |

```bash
# エンディング動画のパスを決定（プロジェクト優先、プラグインフォールバック）
PROJECT_ENDING="./endings/${ASPECT_DIR}/ending.mp4"
PLUGIN_ENDING="${CLAUDE_PLUGIN_ROOT}/endings/${ASPECT_DIR}/ending.mp4"

if [ -f "$PROJECT_ENDING" ]; then
  ENDING_PATH="$PROJECT_ENDING"
  echo "プロジェクトのエンディング動画を使用: $ENDING_PATH"
elif [ -f "$PLUGIN_ENDING" ]; then
  ENDING_PATH="$PLUGIN_ENDING"
  echo "プラグインのエンディング動画を使用: $ENDING_PATH"
else
  ENDING_PATH=""
  echo "警告: エンディング動画が見つかりませんでした"
  echo "  - プロジェクト: $PROJECT_ENDING"
  echo "  - プラグイン: $PLUGIN_ENDING"
fi
```

3. **動画の結合**

```bash
# エンディング動画が見つかった場合のみ結合
if [ -n "$ENDING_PATH" ] && [ -f "$ENDING_PATH" ]; then
  # 結合用のリストファイルを作成（絶対パスを使用）
  echo "file '$(realpath main_with_audio.mp4)'" > concat_list.txt
  echo "file '$(realpath "$ENDING_PATH")'" >> concat_list.txt

  # 動画を結合
  ffmpeg -f concat -safe 0 -i concat_list.txt \
    -c copy -y final_output.mp4

  # クリーンアップ
  rm concat_list.txt main_with_audio.mp4
  echo "エンディング動画を結合しました: final_output.mp4"
else
  # エンディング動画がない場合はそのまま使用
  mv main_with_audio.mp4 final_output.mp4
  echo "エンディング動画なしで完了: final_output.mp4"
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
