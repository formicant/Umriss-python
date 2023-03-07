from __future__ import annotations
from typing import Any


class Element:
    
    def __init__(self, name: str, **attributes: Any):
        self.name = name
        self.attributes = attributes
        self.children: list[Element] = []
    
    
    def add_child(self, child: Element) -> None:
        self.children.append(child)
    
    
    def render(self, indent: str='') -> str:
        attributes = ''.join(f' {_attr_name(k)}="{v}"' for k, v in self.attributes.items())
        if len(self.children) > 0:
            children = ''.join(child.render(indent + ' ') for child in self.children)
            return f'{indent}<{self.name}{attributes}>\n{children}{indent}</{self.name}>\n'
        else:
            return f'{indent}<{self.name}{attributes} />\n'


def _attr_name(attr: str) -> str:
    return attr.replace("__", ":").replace("_", "-")
