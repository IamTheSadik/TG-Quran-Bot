from .. import Quran
from .getAyahButton import getAyahButton
from .getAyahReply import getAyahReply, getAyahReplyFromPreference


validFormat = """
Give like:

<pre>
surahNo : ayahNo
1:3
</pre>"""


def getValidReply(userID, text, language=None, restrictedLangs: list = None):
    text = text.strip()
    if text.isdecimal() and 1 <= int(text) <= 114:  # if only surah number is given
        surahNo = int(text)
        ayahNo = 1
        surah = Quran.getSurahNameFromNumber(surahNo)
        ayahCount = Quran.getAyahNumberCount(surahNo)

        if language:
            reply = getAyahReply(surahNo, ayahNo, language)
        else:
            print("getAyahReplyFromPreference")
            reply = getAyahReplyFromPreference(
                surahNo, ayahNo, userID, restrictedLangs=restrictedLangs
            )

        buttons = getAyahButton(surahNo, ayahNo, userID, language)

        return {"text": reply, "buttons": buttons}

    sep = text.split(":")
    if len(sep) != 2:
        reply = "<b>Your format is not correct.</b>" + validFormat
        reply = {"text": reply, "buttons": None}
        return reply

    surahNo, ayahNo = sep
    surahNo = surahNo.strip()
    ayahNo = ayahNo.strip()

    if not (surahNo.isdecimal() and ayahNo.isdecimal()):
        reply = "<b>Surah and Ayah number must be integers</b>" + validFormat

        return {"text": reply, "buttons": None, "send": True}

    surahNo = int(surahNo)

    if not 1 <= surahNo <= 114:
        reply = "<b>Surah number needs to be between <i>1</i> to <i>114</i>.</b>"
        return {"text": reply, "buttons": None, "send": True}

    surah = Quran.getSurahNameFromNumber(surahNo)
    ayahCount = Quran.getAyahNumberCount(surahNo)
    ayahNo = int(ayahNo)

    if not 1 <= ayahNo <= ayahCount:
        reply = f"""
<b>Surah {surah} has {ayahCount} ayahs only.</b>

But you gave ayah no. {ayahNo}
"""

        return {"text": reply, "buttons": None, "send": True}

    if language:
        reply = getAyahReply(surahNo, ayahNo, language=language)
    else:
        reply = getAyahReplyFromPreference(surahNo, ayahNo, userID, restrictedLangs)

    buttons = getAyahButton(surahNo, ayahNo, userID, language=language)

    return {"text": reply, "buttons": buttons}
