from dataclasses import dataclass, field
from typing import List

@dataclass
class InnerModel:
    type: str = "minecraft:model"
    model: str = ""

@dataclass
class CaseItem:
    when: str
    model: InnerModel

@dataclass
class SelectModel:
    type: str = "minecraft:select"
    property: str = "minecraft:component"
    component: str = "minecraft:custom_name"
    cases: List[CaseItem] = field(default_factory=list)
    fallback: InnerModel = field(default_factory=lambda: InnerModel(model="minecraft:item/diamond_sword"))

@dataclass
class MinecraftRootModel:
    model: SelectModel