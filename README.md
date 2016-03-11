# BingImageDownload
Bing画像検索APIを用いて、最大50件画像を保存する

## 使い方
```
> python BingImageDownload.py キーワード < password.txt
```

password.txtは、BingAPIに登録を行った際のメールアドレスとパスワードを記載ください。

カレントディレクトリにキーワードディレクトリを作成し、
その中に連番でファイルを保存していきます。

BingAPIは、5000トランザクション/月まで無料です。計画的に使用してください。

## 制限事項
キーワードによっては、取得できない画像があるようです。

原因調査中です。

## 動作確認
以下の環境で確認しました。

* Windows7 + python2.7.11

* Windows7 + python3.5.1
