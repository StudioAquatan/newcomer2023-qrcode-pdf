from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageOps
import io

OUTPUT_DIR = Path(__file__).parent / "output"

SOFT_TENNIS_ID = "63f60f12af238fb2881bd542"

OUTPUT_IMG_SIZE = 1000
BORDER_WIDTH = 100

if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()


URL = "https://newcomer2023-api-dev.studioaquatan.workers.dev/orgs"


def main() -> None:
    res = requests.get(URL)
    data = res.json()
    for org in data:
        print(org["fullName"])
        id = org["id"]
        src = org["stampBackground"]["src"]

        # 画像を取得
        res_logo = requests.get(src)

        # バイナリから画像を生成
        img = Image.open(io.BytesIO(res_logo.content)).convert("RGBA")

        # なんか回転してるので回転
        if id == SOFT_TENNIS_ID:
            # 回転
            img = img.rotate(-90, expand=True)

        # 出力画像サイズに収まるサイズにリサイズ
        img = ImageOps.contain(
            img,
            (OUTPUT_IMG_SIZE - BORDER_WIDTH * 2, OUTPUT_IMG_SIZE - BORDER_WIDTH * 2),
        )
        width, height = img.size
        # 同じサイズの画像を作ってそこに貼り付ける
        # Image.alpha_compositeは同じサイズの画像しか貼り付けられない
        logo_background = Image.new(
            "RGBA", (OUTPUT_IMG_SIZE, OUTPUT_IMG_SIZE), (255, 255, 255, 0)
        )
        logo_background.paste(
            img, ((OUTPUT_IMG_SIZE - width) // 2, (OUTPUT_IMG_SIZE - height) // 2)
        )

        # リサイズ後の画像サイズを取得
        width, height = img.size

        # 正方形の背景にロゴを貼り付ける
        thumbnail = Image.new(
            "RGBA", (OUTPUT_IMG_SIZE, OUTPUT_IMG_SIZE), (255, 255, 255, 255)
        )
        thumbnail = Image.alpha_composite(thumbnail, logo_background)

        # 角を丸くするためのマスクを作成
        mask = Image.new("L", (OUTPUT_IMG_SIZE, OUTPUT_IMG_SIZE), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle(
            (0, 0, OUTPUT_IMG_SIZE, OUTPUT_IMG_SIZE), radius=100, fill=255
        )

        # 角を丸くする
        masked_thumbnail = Image.composite(
            thumbnail,
            Image.new("RGB", (OUTPUT_IMG_SIZE, OUTPUT_IMG_SIZE), (255, 255, 255)),
            mask,
        )

        # 縁取り
        draw = ImageDraw.Draw(masked_thumbnail)
        draw.rounded_rectangle(
            (0, 0, OUTPUT_IMG_SIZE, OUTPUT_IMG_SIZE),
            radius=100,
            outline="black",
            width=BORDER_WIDTH,
        )

        # thumbnail = ImageOps.contain(img, (max_size, max_size))
        masked_thumbnail.save(OUTPUT_DIR / f"{id}.png")


if __name__ == "__main__":
    main()
