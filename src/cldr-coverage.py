#!/usr/bin/env python3
# Copyright 2020 Khaled Hosny
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from icu import Locale, LocaleData


def coverage(font, threshold=10):
    cmap = set(chr(c) for c in font.getBestCmap())

    languages = set()
    scripts = set()
    partial = {}

    for locale in Locale.getAvailableLocales():
        data = LocaleData(locale)
        examplar = set("".join(data.getExemplarSet()))
        if not cmap.isdisjoint(examplar):
            locale = Locale(locale)
            locale.addLikelySubtags()
            diff = examplar - cmap
            if not diff:
                scripts.add(locale.getDisplayScript())
                languages.add(locale.getDisplayLanguage())
            elif len(diff) <= threshold:
                partial[locale.getDisplayLanguage()] = diff

    return scripts, languages, partial


def report(scripts, languages, partial):
    text = []
    if scripts or languages:
        text.append("\n# Full")

    if scripts:
        scripts = ", ".join(sorted(scripts))
        text.append(f"* Scripts: {scripts}")

    if languages:
        languages = ", ".join(sorted(languages))
        text.append(f"* Languages: {languages}")

    if partial:
        import unicodedata as ucd

        text.append("\n# Partial")
        for language, missing in partial.items():
            missing = ", ".join(
                (ucd.combining(c) and f"\u25CC{c}" or c) for c in sorted(missing)
            )
            text.append(f"* {language}: {missing}")

    return "\n".join(text)


if __name__ == "__main__":
    import sys
    from fontTools.ttLib import TTFont

    for fontpath in sys.argv[1:]:
        print("")
        font = TTFont(fontpath)
        print(f"`{fontpath}`:")
        print(report(*coverage(font)))
