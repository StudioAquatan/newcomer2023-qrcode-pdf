from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


QR_CODE_PATH = (
    Path(__file__).parent.parent / "qr" / "output" / "63f4acebe439114a775ab2b6.png"
)
QR_CODE_SIZE = 15 * cm


GENJYUU_GOTHIC_P_BOLD_PATH = Path(__file__).parent / "GenJyuuGothic-P-Bold.ttf"


def main() -> None:
    pdfFile = canvas.Canvas("./python.pdf")
    pdfFile.saveState()

    pdfFile.setAuthor("StudioAquatan")
    pdfFile.setTitle("ここに団体名")

    # A4
    pdfFile.setPageSize(A4)

    # QRコードを中央に配置
    page_width, page_height = A4
    pdfFile.drawImage(
        QR_CODE_PATH,
        page_width / 2 - QR_CODE_SIZE / 2,
        page_height / 2 - QR_CODE_SIZE / 2,
        width=QR_CODE_SIZE,
        height=QR_CODE_SIZE,
    )

    pdfmetrics.registerFont(TTFont("GenJyuuGothic-P-Bold", GENJYUU_GOTHIC_P_BOLD_PATH))
    pdfFile.setFont("GenJyuuGothic-P-Bold", 40)
    pdfFile.drawCentredString(page_width / 2, 25 * cm, "全団体同時開催個別説明会")
    pdfFile.drawCentredString(page_width / 2, 23 * cm, "スタンプラリー")
    pdfFile.setFont("GenJyuuGothic-P-Bold", 26)
    pdfFile.drawCentredString(page_width / 2, 4 * cm, "科学・ものづくり教育普及プロジェクト”ぽっけ”")

    pdfFile.restoreState()
    pdfFile.save()


if __name__ == "__main__":
    main()
