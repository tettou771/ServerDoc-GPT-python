# サーバーヘルスチェックプログラム

このPythonプログラムは、サーバの健康状態をチェックし、そのレポートをHTMLメールとして送信します。メールには本文の先頭に埋め込まれた画像が含まれ、本文はMarkdown形式をサポートしています。

## 特徴

- サーバの健康状態をチェック
- 健康レポートをHTMLメールで送信
- メール本文の先頭に画像を埋め込む
- Markdown形式の本文をHTMLに変換

## 必要要件

- Python 3.x
- `smtplib`
- `email` (標準ライブラリ)
- `requests`
- `markdown`

## インストール

1. このリポジトリをクローンします。
2. 必要なPythonパッケージをpipでインストールします。

    ```bash
    pip install requests markdown
    ```

## 使い方

1. `main.py`と`email_sender.py`（または`EmailSender`クラスを含むファイル）が同じディレクトリにあることを確認します。
2. `main.py`スクリプトを実行して、サーバの健康状態をチェックし、レポートをメールで送信します。

    ```bash
    python main.py
    ```

## Configuration

1. `config-example.json`ファイルを`config.json`としてコピーします。

    ```bash
    cp config-example.json config.json
    ```

2. `config.json`ファイルを開き、以下の設定を自分の環境に合わせて編集します。

```json
{
    "email": "your@email.com",
    "gpt_model": "gpt-4",
    "openai_api_key": "your-api-key",
    "smtp": {
        "server": "smtp.server.address",
        "port": 587,
        "from_email": "from_email",
        "password": "password"
    },
    "commands": {
        "Current time": {
            "command": "date",
            "description": "Get current date and time."
        },
        "System uptime": {
            "command": "uptime",
            "description": "Displays how long the system has been running and the load average."
        },
        "CPU usage": {
            "command": "mpstat",
            "description": "Reports detailed CPU usage statistics."
        },
        "Top processes": {
            "command": "top -n 1 -b | head -n 20",
            "description": "Displays the top processes by CPU usage. If you find a problem, please write process name with pid."
        },
        "Disk usage": {
            "command": "df -h",
            "description": "Displays the disk usage for all files and directories in the root directory."
        },
        "Memory usage": {
            "command": "free",
            "description": "Check memory usage."
        },
        "Virtual memory statistics": {
            "command": "vmstat",
            "description": "Provides virtual memory statistics including disk IO, system activity, and CPU activity."
        },
        "IO statistics": {
            "command": "iostat | grep -v loop",
            "description": "Displays CPU statistics and IO statistics for disks, excluding loop devices."
        },
        "Recent Kernel messages": {
            "command": "dmesg -T | tail -30",
            "description": "Displays messages from the kernel, including hardware errors, driver messages, and system errors."
        }
    },
    "prompt": "あなたはサーバー管理者です。サーバの健康状態について日本語でレポートして、オーナーが対応するべきことがあれば教えてください。メールで応答に関して受信するので、JSON形式で、subjectキーにタイトル、bodyキーに本文、dall-e_promptキーに、この状況を説明するためのイラストや図解（写真ではない）生成用のプロンプトをstring形式で入れていください。タイトルは、問題がない場合は PASSED: で開始して、調べたほうがいいことがある時は WARNING: で始まり、至急確認するべき状況なら ERROR: をつけてください。本文はmarkdown形式でお願いします"
}
```

- `email`: 送信元のメールアドレスを指定します。
- `gpt_model`: 使用するOpenAIのGPTモデルを指定します。
- `openai_api_key`: OpenAI APIキーを指定します。
- `smtp`: SMTPサーバーの設定を指定します。
  - `server`: SMTPサーバーのアドレスを指定します。
  - `port`: SMTPサーバーのポート番号を指定します。
  - `from_email`: 送信元のメールアドレスを指定します。
  - `password`: SMTPサーバーのパスワードを指定します。
- `commands`: サーバの健康状態をチェックするために実行するコマンドのリストを指定します。
  - `command`: 実行するコマンドを指定します。
  - `description`: コマンドの説明を指定します。
- `prompt`: サーバの健康状態についてレポートを生成するためのプロンプトを指定します。プロンプトは日本語で記載されていますが、必要に応じて適宜編集してください。

3. 設定が完了したら、`main.py`スクリプトを実行してサーバの健康状態をチェックし、レポートをメールで送信します。

    ```bash
    python main.py
    ```

## 使い方


```
python main.py
```

## License

MIT