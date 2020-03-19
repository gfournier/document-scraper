import json
from typing import List, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Field:
    name: str
    value: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class XPathExpression:
    xpath: str
    regex: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Form:
    fields: List[Field]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Config:
    root_url: str
    base_url: str
    next_page: XPathExpression
    form: Form


def load_config(filename):
    with open(filename, 'rt') as fp:
        config = Config.from_dict(json.load(fp))
    return config