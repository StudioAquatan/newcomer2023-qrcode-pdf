# newcomer2023-qrcode-pdf

新歓 2023 企画用の、各団体のスタンプ獲得用URLを埋め込んだPDFを生成するスクリプト

## 依存パッケージのインストール

```bash
poetry install
```

## 各団体のスタンプ獲得用URLを用意する

`tokens_sample.csv` を参考に、作成した各団体のスタンプ獲得用URLを `tokens.csv` として配置する。

## 1. 正方形のロゴ画像を生成する

QRコードの中心に埋め込まれるロゴ画像を生成する。

```bash
poetry run python logo/main.py
```

## 2. QRコードを生成する

`tokens.csv` の短縮URLからQRコードを生成し、QRコードの中心にロゴ画像を埋め込んだ画像を生成する。

```bash
poetry run python pdf/main.py
```

## 3. PDFを生成する

QRコードと団体名を配置したPDFを生成する。

```bash
poetry run python pdf/main.py
```
