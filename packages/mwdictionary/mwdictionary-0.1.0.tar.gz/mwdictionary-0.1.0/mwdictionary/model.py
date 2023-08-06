from dataclasses import dataclass, field
from typing import List


@dataclass
class Word:
    word: str
    wordtype: str
    shortdef: str
    synonyms: List[str] = field(default_factory=list)
    antonyms: List[str] = field(default_factory=list)
    stems: List[str] = field(default_factory=list)

    @classmethod
    def from_response(cls, r: dict) -> object:
        def set_list_attr(attr: str, _list: list) -> None:
            try:
                l = _list[0]
            except IndexError:
                l = []
            finally:
                setattr(cls, attr, l)
        obj = cls.__new__(cls)
        obj.word = r["meta"]["id"]
        obj.wordtype = r["fl"]
        set_list_attr("shortdef", r["shortdef"])
        set_list_attr("synonyms", r["meta"]["syns"])
        set_list_attr("antonyms", r["meta"]["ants"])
        set_list_attr("stems", r["meta"]["stems"])
        return obj