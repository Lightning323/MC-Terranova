import json
import os
from pathlib import Path

# Base directories
MIXING_DIR = Path("./mixing")
COLORING_DIR = Path("./coloring")

# Standard 16 Vanilla Minecraft Colors
VANILLA_COLORS = {
    "white", "orange", "magenta", "light_blue", "yellow", "lime", 
    "pink", "gray", "light_gray", "cyan", "purple", "blue", 
    "brown", "green", "red", "black"
}

# Custom color aliases mapped directly to Dye Depot IDs
COLOR_TRANSLATIONS = {
    # Direct Dye Depot matches
    "amber": "dye_depot:amber",
    "aqua": "dye_depot:aqua",
    "beige": "dye_depot:beige",
    "coral": "dye_depot:coral",
    "forest": "dye_depot:forest",
    "ginger": "dye_depot:ginger",
    "indigo": "dye_depot:indigo",
    "maroon": "dye_depot:maroon",
    "mint": "dye_depot:mint",
    "navy": "dye_depot:navy",
    "olive": "dye_depot:olive",
    "rose": "dye_depot:rose",
    "slate": "dye_depot:slate",
    "tan": "dye_depot:tan",
    "teal": "dye_depot:teal",
    "verdant": "dye_depot:verdant",
    
    # Custom similarity/synonym mappings
    "chartreuse": "dye_depot:olive",     # Chartreuse is yellow-green -> Olive or Verdant
    "turquoise": "dye_depot:teal",      # Turquoise is blue-green -> Teal (not verdant)
    "royal_blue": "dye_depot:navy",     # Deep blue -> Navy
    "sky_blue": "dye_depot:aqua",       # Light blue -> Aqua
    "pine_green": "dye_depot:forest",   # Dark green -> Forest
    "vermilion": "dye_depot:ginger",    # Red-Orange -> Ginger or Coral
    "olive_green": "dye_depot:olive",
    "granite": "dye_depot:tan",
    "tuff": "dye_depot:slate",          # Dark blue-gray stone -> Slate
    "dripstone": "dye_depot:tan",       # Brownish-orange stone -> Tan
    "ochrum": "dye_depot:beige",        # Light yellowish stone -> Beige or Amber
    "sea_green": "dye_depot:verdant",     
    # "limestone":"dye_depot:beige"
}


def translate_color(raw_color: str) -> str:
    """
    Checks if a raw color string is vanilla, or maps it to Dye Depot.
    """
    if not raw_color:
        return "minecraft:black"

    # Clean up prefixes or tags if present (e.g., "minecraft:black" or "#c:dyes/dye_depot_amber")
   
    color = raw_color.lower().split(":")[-1].split("/")[-1].replace("dye_depot_", "")
    print("Color = ", color)

    # 1. Vanilla Minecraft Color
    if color in VANILLA_COLORS:
        return f"minecraft:{color}"

    # 2. Dye Depot translation lookup
    if color in COLOR_TRANSLATIONS:
        return COLOR_TRANSLATIONS[color]

    # 3. Fallback: If it's an unmapped non-vanilla color, format under dye_depot namespace
    return f"dye_depot:{color}"


def convert_mixing_to_coloring(mixing_data: dict) -> dict:
    """Converts a Create mixing recipe dictionary to a Create Dragons Plus coloring recipe."""
    extracted_color = None
    ingredients = mixing_data.get("ingredients", [])
    filtered_ingredients = []

    for ing in ingredients:
        # Check for fluid or custom data containing the color info
        if ing.get("fluids") == "railways:paint" or "components" in ing:
            custom_data = (
                ing.get("components", {})
                .get("minecraft:custom_data", {})
            )
            extracted_color = custom_data.get("Color")
        else:
            filtered_ingredients.append(ing)

    # Translate the extracted color
    final_color = translate_color(extracted_color)

    return {
        "type": "create_dragons_plus:coloring",
        "color": final_color,
        "ingredients": filtered_ingredients,
        "results": mixing_data.get("results", []),
    }


def process_recipes():
    if not MIXING_DIR.exists():
        print(f"Error: Base directory '{MIXING_DIR}' does not exist.")
        return

    processed_count = 0

    for root, _, files in os.walk(MIXING_DIR):
        for file in files:
            if file.endswith(".json"):
                source_path = Path(root) / file
                relative_path = source_path.relative_to(MIXING_DIR)
                dest_path = COLORING_DIR / relative_path

                try:
                    with open(source_path, "r", encoding="utf-8") as f:
                        mixing_json = json.load(f)

                    coloring_json = convert_mixing_to_coloring(mixing_json)

                    dest_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(dest_path, "w", encoding="utf-8") as f:
                        json.dump(coloring_json, f, indent=2)

                    processed_count += 1
                    print(f"Converted: {relative_path} -> color: {coloring_json['color']}")

                except Exception as e:
                    print(f"Failed to process {source_path}: {e}")

    print(f"\nSuccessfully converted {processed_count} recipe files!")


if __name__ == "__main__":
    process_recipes()