from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
import PyPDF2


QR_CODE_DIR = Path(__file__).parent.parent / "qr" / "output"
QR_CODE_SIZE = 15 * cm

TOKEN_PATH = Path(__file__).parent.parent / "tokens.csv"
OUTPUT_DIR = Path(__file__).parent / "output"

GENJYUU_GOTHIC_P_BOLD_PATH = Path(__file__).parent / "GenJyuuGothic-P-Bold.ttf"


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

        pdfFile = canvas.Canvas(str(OUTPUT_DIR / f"{orgName}.pdf"))
        pdfFile.saveState()

        pdfFile.setAuthor("StudioAquatan")
        pdfFile.setTitle("ここに団体名")

        # A4
        pdfFile.setPageSize(A4)

        # QRコードを中央に配置
        page_width, page_height = A4
        pdfFile.drawImage(
            QR_CODE_DIR / f"{orgId}.png",
            page_width / 2 - QR_CODE_SIZE / 2,
            page_height / 2 - QR_CODE_SIZE / 2,
            width=QR_CODE_SIZE,
            height=QR_CODE_SIZE,
        )

        pdfmetrics.registerFont(
            TTFont("GenJyuuGothic-P-Bold", GENJYUU_GOTHIC_P_BOLD_PATH)
        )
        pdfFile.setFont("GenJyuuGothic-P-Bold", 40)
        pdfFile.drawCentredString(page_width / 2, 25 * cm, "全団体同時開催個別説明会")
        pdfFile.drawCentredString(page_width / 2, 23 * cm, "スタンプラリー")
        pdfFile.setFont("GenJyuuGothic-P-Bold", 26)
        pdfFile.drawCentredString(page_width / 2, 4 * cm, f"{orgName}")

        pdfFile.restoreState()
        pdfFile.save()

    merger = PyPDF2.PdfMerger()
    for path in OUTPUT_DIR.glob("*.pdf"):
        merger.append(str(path))

    merger.write(OUTPUT_DIR / "all.pdf")
    merger.close()


if __name__ == "__main__":
    main()
