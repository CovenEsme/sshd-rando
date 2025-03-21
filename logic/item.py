from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import World


class Item:
    def __init__(
        self,
        id_: int = -1,
        name_: str = None,
        oarcs_: list[str] = [],
        shop_arc_name_: str = None,
        shop_model_name_: str = None,
        world_: "World" = None,
        major_item_: bool = False,
        game_winning_item_: bool = False,
        chain_locations_: list[str] = [],
    ) -> None:
        self.id: int = id_
        self.name: str = name_
        self.oarcs: list[str] = oarcs_
        self.shop_arc_name: str = shop_arc_name_
        self.shop_model_name: str = shop_model_name_
        self.world: "World" = world_
        self.is_major_item: bool = major_item_
        self.is_game_winning_item: bool = game_winning_item_
        self.chain_locations: list[str] = chain_locations_

        self.is_dungeon_small_key: bool = (
            " Small Key" in name_ and name_ != "Lanayru Caves Small Key"
        )
        self.is_boss_key: bool = " Boss Key" in name_
        self.is_dungeon_map: bool = " Map" in name_

    def __str__(self) -> str:
        return (
            self.name
            if self.world.num_worlds == 1
            else f"{self.name} [W{self.world.id + 1}]"
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other) -> bool:
        if other == None:
            return False
        return self.id == other.id and self.world.id == other.world.id

    def __lt__(self, other) -> bool:
        if other == None:
            return False
        if self.world.id != other.world.id:
            return self.world.id < other.world.id
        return self.id < other.id

    def __hash__(self) -> int:
        return (self.id, self.world.id).__hash__()
