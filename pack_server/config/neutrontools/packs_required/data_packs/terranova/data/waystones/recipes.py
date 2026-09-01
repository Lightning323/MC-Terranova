import json
import os

# Define output directory
OUTPUT_DIR = "./recipe"

# Vanilla Minecraft Dyes (namespace: "minecraft")
VANILLA_DYES = [
    "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
    "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"
]

# Dye Depot Dyes (namespace: "dye_depot")
DYE_DEPOT_DYES = [
    "amber", "aqua", "beige", "burgundy", "coral", "forest", "ginger", "indigo",
    "maroon", "mint", "navy", "olive", "peach", "rose", "teal", "vermilion"
]


def get_portstone_recipe(color, dye_item_id):
    """Generates the Mechanical Crafting JSON structure for Portstone."""
    return {
        "type": "create:mechanical_crafting",
        "accept_mirrored": False,
        "category": "misc",
        "key": {
            "A": {"item": "minecraft:lodestone"},
            "B": {"item": dye_item_id},
            "P": {"tag": "minecraft:stone_bricks"},
            "S": {"item": "terranova:void_pearl"}
        },
        "pattern": [
            "  S  ",
            " BAB ",
            "PPAPP"
        ],
        "result": {
            "count": 1,
            "id": f"waystones:{color}_portstone"
        },
        "show_notification": False
    }


def get_sharestone_recipe(color, dye_item_id):
    """Generates the Mechanical Crafting JSON structure for Sharestone."""
    return {
        "type": "create:mechanical_crafting",
        "accept_mirrored": False,
        "category": "misc",
        "key": {
            "A": {"item": "minecraft:lodestone"},
            "B": {"item": dye_item_id},
            "P": {"tag": "minecraft:stone_bricks"},
            "S": {"item": "terranova:void_pearl"}
        },
        "pattern": [
            "PPAPP",
            " ABA ",
            "  S  ",
            " ABA ",
            "PPPPP"
        ],
        "result": {
            "count": 1,
            "id": f"waystones:{color}_sharestone"
        },
        "show_notification": False
    }


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_count = 0

    # Build color-to-dye mapping
    color_dye_map = {}
    
    for color in VANILLA_DYES:
        color_dye_map[color] = f"minecraft:{color}_dye"

    for color in DYE_DEPOT_DYES:
        color_dye_map[color] = f"dye_depot:{color}_dye"

    # Generate recipes
    for color, dye_item_id in color_dye_map.items():
        # Portstone
        portstone_file = os.path.join(OUTPUT_DIR, f"{color}_portstone.json")
        with open(portstone_file, "w", encoding="utf-8") as f:
            json.dump(get_portstone_recipe(color, dye_item_id), f, indent=2)
        generated_count += 1

        # Sharestone
        sharestone_file = os.path.join(OUTPUT_DIR, f"{color}_sharestone.json")
        with open(sharestone_file, "w", encoding="utf-8") as f:
            json.dump(get_sharestone_recipe(color, dye_item_id), f, indent=2)
        generated_count += 1

    print(f"Successfully generated {generated_count} recipe files in '{OUTPUT_DIR}'.")


if __name__ == "__main__":
    main()