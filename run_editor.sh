#!/bin/bash

# Define the path to the editor.py script relative to this script
EDITOR_SCRIPT_PATH="$(dirname "$0")/editor/editor.py"

# Define the path to the JSON file containing the instructions
INSTRUCTION_FILE_PATH="$(dirname "$0")/instructions/test_instructions.json"

# Create the instructions directory if it does not exist
mkdir -p "$(dirname "$INSTRUCTION_FILE_PATH")"

# Generate the JSON content with test instructions
cat > "$INSTRUCTION_FILE_PATH" <<EOL
[
    {
        "instruction": "CreateFile",
        "path": "tests/test_map_integration.py",
        "content": "# LANDMARK-START:001-MAP-INIT\\ndef test_initialize_google_maps_api():\\n    assert False, 'Pending test for Google Maps API initialization'\\n# LANDMARK-END:001-MAP-INIT\\n\\n# LANDMARK-START:002-MAP-UI\\ndef test_place_map_in_ui():\\n    assert False, 'Pending test for placing map in UI with controls'\\n# LANDMARK-END:002-MAP-UI\\n"
    },
    {
        "instruction": "CreateFile",
        "path": "tests/test_sunlight_paths.py",
        "content": "# LANDMARK-START:003-SUNLIGHT-MODEL\\ndef test_sunlight_model():\\n    assert False, 'Pending test for sunlight paths modeling'\\n# LANDMARK-END:003-SUNLIGHT-MODEL\\n\\n# LANDMARK-START:004-SUNLIGHT-SERVICE\\ndef test_sunlight_service():\\n    assert False, 'Pending test for sunlight data fetching service'\\n# LANDMARK-END:004-SUNLIGHT-SERVICE\\n"
    },
    {
        "instruction": "CreateFile",
        "path": "tests/test_ui_elements.py",
        "content": "# LANDMARK-START:005-UI-VIEWPOINT\\ndef test_ui_viewpoint_selector():\\n    assert False, 'Pending test for UI viewpoint selector'\\n# LANDMARK-END:005-UI-VIEWPOINT\\n\\n# LANDMARK-START:006-UI-TIMEPICKER\\ndef test_ui_time_picker():\\n    assert False, 'Pending test for UI time picker'\\n# LANDMARK-END:006-UI-TIMEPICKER\\n"
    }
]
EOL

# Check if the instruction file was created successfully
if [ ! -f "$INSTRUCTION_FILE_PATH" ]; then
    echo "Failed to create instruction file: $INSTRUCTION_FILE_PATH"
    exit 1
fi

# Run the editor script with the instruction file
python "$EDITOR_SCRIPT_PATH" "$INSTRUCTION_FILE_PATH"

# Check the exit status of the editor script
if [ $? -eq 0 ]; then
    echo "Editor script executed successfully."
else
    echo "Editor script failed to execute."
    exit 1
fi
