import re
from collections import OrderedDict
from dataclasses import dataclass
from functools import lru_cache
from typing import Self

LANG = OrderedDict[str, str]
MASTER = "LANG_DE.h"


@dataclass
class BSBLang:
    dict: OrderedDict[str, str]

    @classmethod
    def decode(cls, lang_str: str) -> Self:
        lang_dict = OrderedDict()
        for line in lang_str.split("\n"):
            match = re.match(r"\W*#define\W+(\w+)\W+\"(.*)\"", line)
            if match:
                lang_dict[match.group(1)] = match.group(2)
        return cls(lang_dict)

    @classmethod
    def load(cls, filepath: str) -> Self:
        with open(filepath) as f:
            return cls.decode(f.read())

    @classmethod
    @lru_cache(maxsize=1)
    def master(cls) -> Self:
        return cls.load(MASTER)

    def encode(self) -> str:
        return "\n".join([f"#define {k} \"{v}\"" for k, v in self.dict.items()])

    def untranslated(self) -> Self:
        untranslated_dict = OrderedDict()
        master = self.master()
        for key in master.dict:
            if not key.startswith("UNIT_") and key not in self.dict:
                untranslated_dict[key] = master.dict[key]
        return type(self)(untranslated_dict)


lang_en = BSBLang.load("LANG_EN2.h")
print(lang_en.untranslated().encode())
print(len(BSBLang.master().dict))
