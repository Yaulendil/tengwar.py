"""A module for converting Roman-form Quenya into Tengwar and Tehtar."""

from re import compile
from typing import List, Optional, Tuple

from ._base import Transcriber


class Tehta(object):
    __slots__ = "_base", "_long"

    def __init__(self, base: str, long: str = None):
        self._base: str = base
        self._long: Optional[str] = long

    def short(self, other: str = None) -> str:
        return f"{other or telco}{self._base}"

    def long(self, other: str = None) -> str:
        if other is None:
            return f"{ara}{self._base}"
        elif self._long is not None:
            return f"{other}{self._long}"
        else:
            return f"{other}{mod_long}{self._base}"


class Tema(object):
    __slots__ = "base", "voiced", "fric", "fric_voiced", "nasal", "special"

    def __init__(
        self,
        base: str, voiced: str,
        fric: str, fric_voiced: str,
        nasal: str, special: str,
        *_,
    ):
        self.base: str = base
        self.voiced: str = voiced
        self.fric: str = fric
        # NOTE: In Quenya specifically, the row for voiced fricatives instead
        #   represents nasal stops.
        self.fric_voiced: str = fric_voiced
        self.nasal: str = nasal
        self.special: str = special

    # def __iter__(self):
    #     return (
    #         self.base, self.voiced,
    #         self.fric, self.fric_voiced,
    #         self.nasal, self.special,
    #     )


class Tengwa(object):
    def __init__(self, base: str = None, vowel: Tehta = None):
        self.base: str = base
        self.vowel: Optional[Tehta] = vowel

        self.silme: bool = False
        self.palatal: bool = False
        self.long_cons: bool = False
        self.long_vowel: bool = False

    def __str__(self) -> str:
        out = self.base

        if out == tema_tinco.special and self.vowel:
            out = romen

        if self.long_cons:
            out += mod_double

        if self.palatal:
            out += mod_palatal

        if self.vowel:
            if self.long_vowel:
                out = self.vowel.long(out)
            else:
                out = self.vowel.short(out)

        if self.silme:
            out += mod_silme(self.base)

        return out


def _int(n: int, base: int) -> Tuple[bool, List[int]]:
    if n == 0:
        return False, [0]
    elif n < 0:
        n *= -1
        negative = True
    else:
        negative = False

    digits = []

    while n > 0:
        n, mod = divmod(n, base)
        digits.append(mod)

    return negative, digits


numeral = ""
mod_10 = ""
mod_12 = ""
# mod_10 = ""
# mod_12 = ""


def int_10(n: int) -> str:
    negative, digits = _int(n, 10)

    if negative:
        return "-" + "".join(numeral[d] + mod_10 for d in digits)
    else:
        return "".join(numeral[d] + mod_10 for d in digits)


def int_12(n: int) -> str:
    negative, digits = _int(n, 12)

    if negative:
        return "-" + "".join(numeral[d] + mod_12 for d in digits)
    else:
        return "".join(numeral[d] + mod_12 for d in digits)


telco = ""; "Short vowel carrier."
ara = ""; "Long vowel carrier."

mod_palatal = ""; ""
mod_silme_l = ""; ""
mod_silme_r = ""; ""
mod_double = ""; "Long/double consonant."
mod_nasal = ""; ""
mod_long = ""; "Long vowel after consonant."

yanta = ""; "Carrier Tengwa for '_i' Diphthongs."
ure = ""; "Carrier Tengwa for '_u' Diphthongs."


# Irregular consonant Tengwar.
romen = ""
arda = ""
lambe = ""
alda = ""

silme = ""
silme_nuquerna = ""
esse = ""
esse_nuquerna = ""

hyamen = ""
hwesta = ""
osse = ""


# Regular consonant Témar.
tema_tinco = Tema(*"")
tema_parma = Tema(*"")
tema_calma = Tema(*"")
tema_quesse = Tema(*"")


# Vowel Tehtar.
tehta_a = Tehta("", None)
tehta_e = Tehta("") # , "")
tehta_i = Tehta("", "")
tehta_o = Tehta("", None)
tehta_u = Tehta("", None)

t_short = {
    "a": tehta_a,
    "e": tehta_e,
    "i": tehta_i,
    "o": tehta_o,
    "u": tehta_u,
    "ä": tehta_a,
    "ë": tehta_e,
    "ï": tehta_i,
    "ö": tehta_o,
    "ü": tehta_u,
}
t_long = {
    "á": tehta_a,
    "é": tehta_e,
    "í": tehta_i,
    "ó": tehta_o,
    "ú": tehta_u,
}


# Diphthongs.
diph = {
    "ai": tehta_a.short(yanta),
    "oi": tehta_o.short(yanta),
    "ui": tehta_u.short(yanta),
    "au": tehta_a.short(ure),
    "eu": tehta_e.short(ure),
    "iu": tehta_i.short(ure),
    # "aí": tehta_a.long(yanta),
    # "oí": tehta_o.long(yanta),
    # "uí": tehta_u.long(yanta),
    # "aú": tehta_a.long(ure),
    # "eú": tehta_e.long(ure),
    # "iú": tehta_i.long(ure),
}


def get_vowel(v: str) -> Optional[Tuple[Tehta, bool, bool]]:
    palatal = False

    if v.startswith("y"):
        palatal = True
        v = v[1:]

    if v in t_short:
        return t_short[v], False, palatal
    elif v in t_long:
        return t_long[v], True, palatal
    else:
        return None


def mod_silme(base: str) -> str:
    if base in "":
        return mod_silme_r
    else:
        return mod_silme_l


con = {
    "t": tema_tinco.base, # tinco
    "nd": tema_tinco.voiced, # ando
    "s": tema_tinco.fric, # thúle/súle
    "þ": tema_tinco.fric, # thúle/súle
    "th": tema_tinco.fric, # thúle/súle
    "nt": tema_tinco.fric_voiced, # anto
    "n": tema_tinco.nasal, # númen
    "r": tema_tinco.special, # óre

    "p": tema_parma.base, # parma
    "mb": tema_parma.voiced, # umbar
    "f": tema_parma.fric, # formen
    "mp": tema_parma.fric_voiced, # ampa
    "m": tema_parma.nasal, # malta
    "v": tema_parma.special, # vala

    "c": tema_calma.base, # calma
    "k": tema_calma.base, # calma
    "ng": tema_calma.voiced, # anga
    # "g": tema_calma.voiced, # anga
    "ch": tema_calma.fric, # harma
    "nc": tema_calma.fric_voiced, # anca
    "ñ": tema_calma.nasal, # noldo
    "y": tema_calma.special, # anna

    "qu": tema_quesse.base, # quesse
    "q": tema_quesse.base, # quesse
    "cw": tema_quesse.base, # quesse
    "ngw": tema_quesse.voiced, # ungwe
    "hw": tema_quesse.fric, # hwesta
    "nqu": tema_quesse.fric_voiced, # unque
    "nw": tema_quesse.nasal, # nwalme
    "w": tema_quesse.special, # vilya

    # "r": romen,
    "rd": arda,
    "l": lambe,
    "ld": alda,
    "h": hyamen,
}


punct = {
    " ": " ",
    "'": "",
    ",": " ",
    ".": "",
    ":": "",
    ";": "",
    "!": "",
    "?": "",
    "(": "",
    ")": "",
}

eof = ""


p_number = compile(r"^-?\d+")


class TranscriberQuenya(Transcriber):
    def transcribe(self, text: str) -> str:
        out: str = ""
        segment = text.replace("x", "cs")
        char = None

        def char_out():
            nonlocal char, out

            if char:
                out += str(char)

            char = None

        while segment:
            nums = p_number.search(segment)

            if nums:
                try:
                    n = nums.group()
                    segment = segment[len(n):]
                    out += int_12(int(n))
                except:
                    pass
                else:
                    continue

            while segment and segment[0] in punct:
                char_out()
                out += punct[segment[0]]
                segment = segment[1:]

            i = 3

            while i > 0:
                sub = segment[:i]

                if char is None:
                    if sub.startswith("y"):
                        i = 1
                        sub = sub[:i]

                    if sub.startswith("s"):
                        char = Tengwa(silme)
                        segment = segment[1:]

                        if segment.startswith("s"):
                            char.long_cons = True
                            segment = segment[1:]

                        if segment and get_vowel(segment[0]):
                            char.base = silme_nuquerna

                        break

                    if sub.startswith("z"):
                        char = Tengwa(esse)
                        segment = segment[1:]

                        if segment.startswith("z"):
                            char.long_cons = True
                            segment = segment[1:]

                        if segment and get_vowel(segment[0]):
                            char.base = esse_nuquerna

                        break

                    if sub in con:
                        char = Tengwa(con[sub])
                        segment = segment[i:]

                        if len(sub) == 1 and segment.startswith(sub):
                            char.long_cons = True
                            segment = segment[i:]

                        break

                    if sub in diph:
                        out += diph[sub]
                        segment = segment[i:]
                        break

                    if v_res := get_vowel(sub):
                        tehta, long, palatal = v_res

                        if long:
                            out += tehta.long()
                        else:
                            out += tehta.short()

                        if palatal:
                            out += mod_palatal

                        segment = segment[i:]
                        break

                    # else:
                    #     segment

                else:
                    if sub == "ss":
                        # if char.vowel:
                            char_out()
                            continue
                        # else:
                        #     char.silme = True
                        #     segment = segment[i:]
                        #     break

                    if sub == "s":
                        if char.vowel:
                            char_out()
                            continue
                        else:
                            char.silme = True
                            segment = segment[i:]
                            break

                    if sub in con:
                        char_out()
                        char = Tengwa(con[sub])
                        segment = segment[i:]

                        if len(sub) == 1 and segment.startswith(sub):
                            char.long_cons = True
                            segment = segment[i:]

                        break

                    if sub in diph:
                        char_out()
                        out += diph[sub]
                        segment = segment[i:]
                        break

                    if v_res := get_vowel(sub):
                        if char.vowel is not None:
                            char_out()
                            continue

                        char.vowel, char.long_vowel, char.palatal = v_res

                        segment = segment[i:]
                        break

                i -= 1
            else:
                char_out()
                if segment:
                    out += segment[0]
                segment = segment[1:]

        char_out()
        return out
