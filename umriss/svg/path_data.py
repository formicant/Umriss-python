from typing import Literal
import numpy as np

from umriss.types import Point, QuadraticNode, CubicNode


class PathData:
    """
    Generates path data for an SVG `path` element.
    
    Create a `PathData`, add nodes you want, then,
    use it as a value of a `path` `d` attribute.
    
    The node-adding methods take absolute coordinates.
    The rendered path data, however, uses relative ones.
    The values are rounded to the specified number of `decimals`.
    Briefer node types (`h`, `v`, `t`, `s`) are used when possible.
    `a`-nodes are not supported.
    """
    
    def __init__(self, decimals: int):
        self.decimals = decimals
        self.epsilon = 10**(-decimals) / 2
        
        self.nodes: list[str] = []
        
        self.last_point = _zero
        self.last_move_point = _zero
        self.last_quadratic_ctrl = _zero
        self.last_cubic_ctrl = _zero
    
    
    def __str__(self) -> str:
        return ''.join(self.nodes)
    
    
    def add_move_node(self, point: Point) -> None:
        point = point.round(self.decimals)
        vector = point - self.last_point
        
        self._add_node('m', *vector)
        
        self.last_point = point
        self.last_move_point = point
        self.last_quadratic_ctrl = _zero
        self.last_cubic_ctrl = _zero
    
    
    def add_line_node(self, point: Point) -> None:
        point = point.round(self.decimals)
        [dx, dy] = point - self.last_point
        
        if abs(dy) < self.epsilon:
            self._add_node('h', dx)
        elif abs(dx) < self.epsilon:
            self._add_node('v', dy)
        else:
            self._add_node('l', dx, dy)
            
        self.last_point = point
        self.last_quadratic_ctrl = _zero
        self.last_cubic_ctrl = _zero
    
    
    def add_quadratic_node(self, node: QuadraticNode) -> None:
        node = node.round(self.decimals)
        [ctrl, vector] = node - self.last_point
        
        if np.linalg.norm(ctrl - self.last_quadratic_ctrl) < self.epsilon:
            self._add_node('t', *vector)
        else:
            self._add_node('q', *ctrl, *vector)
        
        self.last_point = node[1]
        self.last_quadratic_ctrl = vector - ctrl
        self.last_cubic_ctrl = _zero
    
    
    def add_cubic_node(self, node: CubicNode) -> None:
        node = node.round(self.decimals)
        [ctrl1, ctrl2, vector] = node - self.last_point
        
        if np.linalg.norm(ctrl1 - self.last_cubic_ctrl) < self.epsilon:
            self._add_node('s', *ctrl2, *vector)
        else:
            self._add_node('c', *ctrl1, *ctrl2, *vector)
        
        self.last_point = node[2]
        self.last_quadratic_ctrl = _zero
        self.last_cubic_ctrl = vector - ctrl2
    
    
    def add_close_node(self) -> None:
        self._add_node('z')
        
        self.last_point = self.last_move_point
        self.last_quadratic_ctrl = _zero
        self.last_cubic_ctrl = _zero
    
    
    _NodeType = Literal['m', 'h', 'v', 'l', 't', 'q', 's', 'c', 'z']
    
    def _add_node(self, node_type: _NodeType, *values: float) -> None:
        formated = (self._format_value(v) for v in values)
        self.nodes.append(node_type + ','.join(formated))
    
    
    def _format_value(self, value: float) -> str:
        formatted = '{:.{d}f}'.format(value, d=self.decimals)
        if self.decimals > 0:
            return formatted.rstrip('0').rstrip('.')
        else:
            return formatted


_zero: Point = np.array([0.0, 0.0])
