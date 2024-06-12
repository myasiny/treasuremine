from enum import Enum

from enums.item_class import ItemClass


class ItemType(Enum):
    def __new__(cls, item_class, low_bound, high_bound):
        item_type = object.__new__(cls)
        item_type._value_ = item_class
        item_type.low_bound = low_bound
        item_type.high_bound = high_bound
        return item_type

    BASIC_PICKAXE = ItemClass.PICKAXE, 10, 30
    BASIC_SWORD = ItemClass.SWORD, 10, 30
