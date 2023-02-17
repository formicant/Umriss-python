from typing import Any

from .path import Path


class Group:
    """
    Generates an SVG group with some paths inside.
    
    Create a `Group`, add paths, then, `render` it.
    Optionally, group attributes (`fill`, `stroke`, etc.) can be specified.
    """
    
    def __init__(self, attributes: dict[str, Any], decimals: int):
        self.decimals = decimals
        self.attributes = attributes
        
        self.paths: list[Path] = []
    
    
    def render(self) -> str:
        paths = (path.render() for path in self.paths)
        attributes = (f' {k.replace("_", "-")}="{v}"' for k, v in self.attributes.items())
        return _group_template.format(
            attributes = ''.join(attributes),
            paths='\n  '.join(paths)
        )
    
    
    def add_path(self, path: Path) -> None:
        self.paths.append(path)


_group_template = '<g{attributes}>\n  {paths}\n </g>'
