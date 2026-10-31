#!/usr/bin/env python3
"""GitHubのアバター（_src/avatar.png）から、ハブのfavicon一式を生成する。

    python3 _src/generate-favicons.py      # 要 Pillow（pip install pillow）

入力  _src/avatar.png（https://github.com/yskms のアバター。460x460、四隅が透過のひし形）
出力  リポジトリのルート（手で編集せず、このスクリプトで再生成する）

  favicon.ico          16・32・48pxの3サイズ入り。ブラウザは<link>が無くても/favicon.icoを探すので、
                       ハブの下にあるアプリの紹介ページのうち、自分のfaviconを持たないものにも効く
  icon-192.png         <link rel="icon" sizes="192x192">用。Googleは、48pxの倍数のfaviconを推奨している
  apple-touch-icon.png iOSのホーム画面用（180px）。iOSは透過を黒で埋めるので、不透明にする

faviconは、アバターを透過のまま縮める（ひし形を残す）。apple-touch-icon.pngだけは、ひし形を
ハブの--surface（hub.cssのライト）と同じ色の地に、74%の大きさで置く。黒い地だとひし形の輪郭が消える。

_src/は、Jekyllが公開しない（先頭が_のディレクトリ）。
"""

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "_src" / "avatar.png"
ICO_SIZES = [(16, 16), (32, 32), (48, 48)]
ICON = 192
TOUCH = 180
TOUCH_SCALE = 0.74
TOUCH_BG = (0xF2, 0xF2, 0xF4, 255)  # hub.cssの--surface（ライト）


def main() -> None:
    src = Image.open(SOURCE).convert("RGBA")
    if src.width != src.height:
        raise SystemExit(f"{SOURCE} が正方形ではない: {src.size}")

    src.save(ROOT / "favicon.ico", sizes=ICO_SIZES)
    src.resize((ICON, ICON), Image.LANCZOS).save(ROOT / "icon-192.png", optimize=True)

    tile = Image.new("RGBA", (TOUCH, TOUCH), TOUCH_BG)
    inner = round(TOUCH * TOUCH_SCALE)
    mark = src.resize((inner, inner), Image.LANCZOS)
    tile.alpha_composite(mark, ((TOUCH - inner) // 2, (TOUCH - inner) // 2))
    tile.convert("RGB").save(ROOT / "apple-touch-icon.png", optimize=True)


if __name__ == "__main__":
    main()
