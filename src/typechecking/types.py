from __future__ import annotations
from dataclasses import dataclass
from typing import List
from tree import TypeNode

type Ty = WildcardTy | TyVar | FunTy | DisTy | ErrorTy | None | SimpleType

@dataclass
class WildcardTy:
    
    def __str__(self):
        return "?"

@dataclass
class TyVar:
    index: int
    name: str

    def __str__(self):
        return self.name

@dataclass
class SimpleType:
    name: str

    def __str__(self):
        return self.name

class ErrorTy:
    pass

@dataclass
class FunctionDeclaration:
    generic_arg_count: int
    ty: FunTy

@dataclass
class DisDeclaration:
    generic_arg_count: int
    variants: List[VariantDeclaration]

    def has_variant(self, name):
        return any(variant.name == name for variant in self.variants)

    def get_variant(self, name):
        return next(variant for variant in self.variants if variant.name == name)

    def get_variant_id(self, name):
        return next(i for (i, variant) in enumerate(self.variants) if variant.name == name)

@dataclass
class VariantDeclaration:
    name: str
    args: List[Arg]

    def get_arg_count(self):
        return len(self.args)

    def get_arg_types(self):
        return [arg.ty for arg in self.args]
    
    def has_arg(self, name: str):
        return any(arg.name == name for arg in self.args)

    def get_arg(self, name: str):
        return next(arg for arg in self.args if arg.name == name)

    def arg_index(self, name: str):
        return [arg.name for arg in self.args].index(name)

@dataclass
class Arg:
    name: str
    ty: Ty

@dataclass
class FunTy:
    arg_types: List[Ty]
    result_type: Ty

    def __str__(self) -> str:
        args = [f"({arg})" if isinstance(arg, FunTy) else f"{arg}" for arg in self.arg_types ]
        args = " -> ".join(args)
        res = f"({self.result_type})" if isinstance(self.result_type, FunTy) else self.result_type
        if self.result_type is None:
            res = "Void"
        if len(self.arg_types) == 0:
            args = "()"
        return f"{args} -> {res}"
@dataclass
class TyPattern:
    name: str
    children: List[TyPattern | None] | None

@dataclass
class DisTy:
    name: str
    generic_types: List[Ty]
    pattern: TyPattern | None

    def __str__(self):
        generics = ", ".join(str(ty) for ty in self.generic_types)
        if generics:
            generics = f"[{generics}]"
        pattern = "" if self.pattern is None else f"::{self.pattern.name}"
        return f"{self.name}{generics}{pattern}"


def substitute(ty: Ty, subst: List[Ty]):
    if isinstance(ty, FunTy):
        arg_types = [substitute(arg, subst) for arg in ty.arg_types]
        result_type = substitute(ty.result_type, subst)
        return FunTy(arg_types, result_type)
    elif isinstance(ty, DisTy):
        generic_types = [substitute(t, subst) for t in ty.generic_types]
        return DisTy(ty.name, generic_types, ty.pattern)
    elif isinstance(ty, TyVar):
        return subst[ty.index]
    else:
        return ty
