from pathlib import Path
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

LOGO_DIR = Path(__file__).parent.parent / "logo" / "output"
TOKEN_PATH = Path(__file__).parent.parent / "tokens.csv"
OUTPUT_DIR = Path(__file__).parent / "output"

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()


def main() -> None:
    tokens = []
    with open(TOKEN_PATH, "r") as f:
        for line in f:
            tokens.append(line.strip(","))

    # ヘッダーをスキップ
    tokens = tokens[1:]

    for token in tokens:
        orgId, orgName, visitedUrl, shortUrl = token.split(",")
        print(f"団体名: {orgName}")
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=30,
        )
        qr.add_data(shortUrl)
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
            fill_color="black",
            back_color="white",
            embeded_image_path=LOGO_DIR / f"{orgId}.png",
        )
        img.save(OUTPUT_DIR / f"{orgId}.png")


if __name__ == "__main__":
    main()
