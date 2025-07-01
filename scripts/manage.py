import dataclasses
import json
import os
import subprocess

from .lib.paths import PROJECT_ROOT
from .mkworld import generate_world
from .lib.manuals import MANUALS, ManualDefinition


def main():
    while True:
        action = __input_choice(
            "What would you like to do?",
            {
                "Generate .apworld": __handle_generate_world,
                "Preview world data": __handle_preview_world_data,
                "Exit": lambda: exit(),
            },
        )
        if action:
            action()


def __handle_generate_world():
    manual_list = [*MANUALS.values()]

    def generate_all_worlds():
        for manual in manual_list:
            generate_world(manual)

    def generate_world_for(manual: ManualDefinition):
        return lambda: generate_world(manual)

    choices = {manual.name: generate_world_for(manual) for manual in manual_list}
    choices["All"] = generate_all_worlds
    choices["Cancel"] = lambda: None

    action = __input_choice("Choose a world to generate:", choices)
    if action:
        action()


def __handle_preview_world_data():
    manual = __input_choice("Choose a world to preview:", MANUALS)
    if not manual:
        return

    print("Loading manual data...")
    manual_data = manual.load_data()
    preview_file_path = PROJECT_ROOT / ".local/preview.json"

    with open(preview_file_path, mode="w", encoding="utf-8") as preview_file:
        json.dump(
            {
                "item_count": sum(item.get("count", 1) for item in manual_data.items),
                "location_count": len(manual_data.locations),
                **dataclasses.asdict(manual_data),
            },
            fp=preview_file,
            indent="\t",
        )

    editor = os.environ.get("EDITOR")
    if not editor:
        print(f"Saved preview to {preview_file_path.relative_to(PROJECT_ROOT)}")
        print("Set the EDITOR environment editor to open it in your preferred editor.")
    else:
        print(f"Opening with {editor}...")
        subprocess.getoutput(f"{editor} {preview_file_path}")


def __input_choice[Value](heading: str, choices: dict[str, Value]) -> Value | None:
    choice_list = [*choices.items()]

    prompt_text = f"\n{heading}\n"
    for index, (choice_name, _) in enumerate(choice_list):
        prompt_text += f"{index + 1}) {choice_name}\n"

    prompt_text += "\n> "

    response = input(prompt_text).strip()

    if not response.isdigit():
        print("Invalid input\n")
        return

    choice_index = int(response) - 1

    if not 0 <= choice_index < len(choice_list):
        print("Invalid choice number")
        return

    return choice_list[choice_index][1]


main()
