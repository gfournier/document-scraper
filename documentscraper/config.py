import json
from typing import List, Optional, Any, Dict

from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Field:
    name: str
    value: Any


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class XPathExpression:
    xpath: str
    regex: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Form:
    method: str
    fields: List[Field]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Output:
    metadata: Dict[str, XPathExpression]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Item:
    output: Output


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Config:
    root_url: str
    base_url: str
    next_page: XPathExpression
    item: Item
    form: Optional[Form] = None


def load_config(filename):
    with open(filename, 'rt') as fp:
        config = Config.from_dict(json.load(fp))
    return config
