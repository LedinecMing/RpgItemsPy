from random import randint
import typing

NORMAL_DAMAGE_LENGTH = 2
NORMAL_DAMAGE_TYPE = int

DamageInfo = typing.Sequence[NORMAL_DAMAGE_TYPE]
ArgsChecker = typing.Dict[str, typing.Sequence]


def real_damage(damage: NORMAL_DAMAGE_TYPE, defence: float) -> int:
    return round(damage-(damage*0.01*defence))


class Item:
    arg_types: ArgsChecker = {"name": [str, "raise ValueError(f'Name must be str, got {arg}({type(arg)})')"]}

    @staticmethod
    def check_args(args: typing.Dict[str, typing.Any], arg_types: ArgsChecker) -> bool:
        for (arg, normalType) in arg_types.items():
            if not isinstance(args[arg], normalType[0]):
                exec(normalType[1], {"ValueError": ValueError, "arg": args[arg]})
        return True


class Weapon(Item):
    arg_types: ArgsChecker = {"damage": [typing.Sequence, "raise ValueError(f'Damage is not subclass of typing.Sequence type, got {arg}({type(arg)})')"],
                              "name": [str, "raise ValueError(f'Wrong type for name str or bytes excepted, got {arg}({type(arg)})')"]}

    def __init__(self, damage: DamageInfo, name: str) -> None:
        if self.check_args({"damage": damage, "name": name}, self.arg_types):
            self._damage: DamageInfo = damage
            self._name: str = name

    @property
    def damage(self) -> float:
        return float(randint(self._damage[0], self._damage[1]))

    @property
    def name(self) -> str:
        return self._name

    @staticmethod
    def check_args(args: typing.Dict[str, typing.Any], arg_types: ArgsChecker) -> bool:
        super().check_args(args, arg_types)
        if any(not isinstance(damageConfig, NORMAL_DAMAGE_TYPE) for damageConfig in args["damage"]):
            raise ValueError(f"Wrong types in damage: {type(args['damage'])}")
        elif len(args["damage"]) != 2:
            raise ValueError(f"Damage length must be 2, got {len(args['damage'])}")
        return True


class Armor(Item):
    arg_types: ArgsChecker = {"name": [str, "raise ValueError(f'Wrong type for name str or bytes excepted, got {arg}({type(arg)})')"],
                              "defence": [int, 'raise ValueError(f"Defence must be int, got {arg}({type(arg)})")']}

    def __init__(self, defence: int, name: str) -> None:
        if super().check_args({"defence": defence, "name": name}, self.arg_types):
            self._defence: int = defence
            self._name: str = name


stick: Weapon = Weapon([1, 4], "Stick")
