from dataclasses import dataclass, field
from typing import List


@dataclass
class Author:
    author_href: str
    author_name: str
    author_date: str = field(default_factory=str)
    author_location: str = field(default_factory=str)
    author_description: str = field(default_factory=str)


@dataclass
class Tag:
    href: str
    name: str


@dataclass
class Quote:
    text: str
    author: Author = field(default_factory=Author)
    tags: List[Tag] = field(default_factory=list)
