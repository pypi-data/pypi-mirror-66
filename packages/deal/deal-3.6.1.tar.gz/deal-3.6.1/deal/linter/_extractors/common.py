import ast
from types import SimpleNamespace
from typing import Optional

import astroid


TOKENS = SimpleNamespace(
    ATTR=(ast.Attribute, astroid.Attribute),
    ASSERT=(ast.Assert, astroid.Assert),
    BIN_OP=(ast.BinOp, astroid.BinOp),
    CALL=(ast.Call, astroid.Call),
    EXPR=(ast.Expr, astroid.Expr),
    FOR=(ast.For, astroid.For),
    IF=(ast.If, astroid.If),
    NAME=(ast.Name, astroid.Name),
    RAISE=(ast.Raise, astroid.Raise),
    RETURN=(ast.Return, astroid.Return),
    TRY=(ast.Try, astroid.TryExcept, astroid.TryFinally),
    UNARY_OP=(ast.UnaryOp, astroid.UnaryOp),
    WITH=(ast.With, astroid.With),
    FUNC=(ast.FunctionDef, astroid.FunctionDef),
)


class Token:
    def __init__(self, value, line: int, col: int):
        self.value = value
        self.line = line
        self.col = col


def traverse(body):
    for expr in body:
        if isinstance(expr, TOKENS.EXPR):
            yield expr.value
            continue
        if isinstance(expr, TOKENS.IF + TOKENS.FOR):
            yield from traverse(body=expr.body)
            yield from traverse(body=expr.orelse)
            continue
        if isinstance(expr, TOKENS.TRY):
            if hasattr(expr, 'orelse'):
                yield from traverse(body=expr.orelse)
            if hasattr(expr, 'finalbody'):
                yield from traverse(body=expr.finalbody)
            continue
        if isinstance(expr, TOKENS.WITH):
            yield from traverse(body=expr.body)
        yield expr


def get_name(expr) -> Optional[str]:
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, astroid.Name):
        return expr.name

    if isinstance(expr, astroid.Attribute):
        return get_name(expr.expr) + '.' + expr.attrname
    if isinstance(expr, ast.Attribute):
        return get_name(expr.value) + '.' + expr.attr

    return None
