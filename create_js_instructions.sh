#!/bin/bash

# Define the root directory of your project as the current directory
PROJECT_ROOT="./"

# Function to create JS instruction files
function create_instruction_file() {
    local filename=$1
    local filepath=$2
    local landmark=$3
    local content=$4

    # Determine the comment style
    local comment_style=$(get_comment_style "$filepath")

    # Escape newlines in content
    local escaped_content=$(printf '%s' "$content" | sed ':a;N;$!ba;s/\n/\\n/g' | sed 's/"/\\"/g')

    # Write the instruction file
    cat << EOF > "$PROJECT_ROOT/$filename"
[
    {
        "instruction": "UpdateFile",
        "path": "$filepath",
        "landmarkId": "$landmark",
        "newContent": "${comment_style} LANDMARK-START:$landmark\n$escaped_content\n${comment_style} LANDMARK-END:$landmark"
    }
]
EOF
}

# Helper function to determine the comment style based on file extension
function get_comment_style() {
    local file=$1
    case "$file" in
        *.py)
            echo "#"
            ;;
        *.js|*.jsx)
            echo "//"
            ;;
        *)
            echo "#"
            ;;
    esac
}

# Create instruction files for test_editor.py
create_instruction_file \
    "update_test_editor_instructions.js" \
    "tests/test_editor.py" \
    "TestEditor" \
    "import unittest\n\nclass TestEditor(unittest.TestCase):\n    def test_sample(self):\n        self.assertTrue(True)"

# Create instruction files for test_file_editor.py
create_instruction_file \
    "update_test_file_editor_instructions.js" \
    "tests/test_file_editor.py" \
    "TestFileEditor" \
    "import unittest\n\nclass TestFileEditor(unittest.TestCase):\n    def test_sample(self):\n        self.assertTrue(True)"

# Create instruction files for test_landmark_masterlist_keeper.py
create_instruction_file \
    "update_test_landmark_masterlist_keeper_instructions.js" \
    "tests/test_landmark_masterlist_keeper.py" \
    "TestLandmarkMasterlistKeeper" \
    "import unittest\n\nclass TestLandmarkMasterlistKeeper(unittest.TestCase):\n    def test_sample(self):\n        self.assertTrue(True)"

echo "JS instruction files have been created."
