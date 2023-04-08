from pathlib import Path
import requests

OUTPUT_DIR = Path(__file__).parent / "output"

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

        logo_img = requests.get(src)
        with open(OUTPUT_DIR / f"{id}.png", "wb") as f:
            f.write(logo_img.content)


if __name__ == "__main__":
    main()
