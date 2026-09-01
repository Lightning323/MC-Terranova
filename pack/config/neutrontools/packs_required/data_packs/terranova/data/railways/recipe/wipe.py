import os

MIXING_DIR = "./mixing"

# Blank recipe template to overwrite the converted files
BLANK_RECIPE = """
{
    "type": "minecraft:crafting_empty",
    "ingredients": [],
    "result": {}
}
"""

def wipe_mixing_recipes():
    if not os.path.exists(MIXING_DIR):
        print(f"Error: Directory '{MIXING_DIR}' does not exist.")
        return

    wiped_count = 0

    # Iterate directly through the /mixing directory
    for root, _, files in os.walk(MIXING_DIR):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(BLANK_RECIPE)
                
                wiped_count += 1
                print(f"Wiped and overridden: {file_path}")

    print(f"\nDone. Successfully overwritten {wiped_count} recipe file(s) in {MIXING_DIR}.")

if __name__ == "__main__":
    wipe_mixing_recipes()