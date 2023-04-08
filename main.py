from pathlib import Path
import qrcode

OUTPUT_DIR = Path(__file__).parent / "output"

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()


def main() -> None:
    tokens = []
    with open("tokens.csv", "r") as f:
        for line in f:
            tokens.append(line.strip(","))

    # ヘッダーをスキップ
    tokens = tokens[1:]

    for token in tokens:
        orgId, orgName, visitedUrl, shortUrl = token.split(",")
        print(f"団体名: {orgName}")
        img = qrcode.make(shortUrl)
        img.save(OUTPUT_DIR / f"{orgId}.png")


if __name__ == "__main__":
    main()
