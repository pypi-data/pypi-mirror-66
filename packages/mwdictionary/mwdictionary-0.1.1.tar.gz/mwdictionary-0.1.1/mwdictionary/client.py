import asyncio
from typing import List

import httpx

from .model import Word


class MWClient:
    def __init__(self, key: str) -> None:
        self.key = key

    def get(self, word: str, product: str="thesaurus", format: str="json") -> Word:
        self._check_product_implemented(product)
        self._check_format_implemented(format)
        r = httpx.get(
            f"https://www.dictionaryapi.com/api/v3/references/{product}/{format}/{word}?key={self.key}"
        )    
        r_json = self._get_response_json(r)
        return Word.from_response(r_json)

    async def aget(self, word: str, product: str="thesaurus", format: str="json") -> Word:
        self._check_product_implemented(product)
        self._check_format_implemented(format)
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://www.dictionaryapi.com/api/v3/references/{product}/{format}/{word}?key={self.key}"
            )
            r_json = self._get_response_json(r)
            return Word.from_response(r_json)

    def _get_response_json(self, response: httpx.Response) -> dict:
        if response.status_code != 200:
            raise AttributeError(
                f"API returned response with status code {response.status_code}."
            )
        r = response.json()
        if not r:
            raise ValueError("API returned empty response!")
        w = r[0] # the word dict is in a single entry list for some reason
        return w

    def _check_product_implemented(self, product: str) -> None:
        implemented = ["thesaurus"]
        self._check_implemented(product, implemented)

    def _check_format_implemented(self, format: str) -> None:
        implemented = ["json"]
        self._check_implemented(format, implemented)
    
    def _check_implemented(self, item: str, implemented: List[str]) -> None:
        if item not in implemented:
            areis = "is" if len(implemented) < 2 else "are"
            imp = ", ".join([f"'{i}'" for i in implemented])
            raise NotImplementedError(f"Only {imp} {areis} currently implemented!")

