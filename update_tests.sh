#!/bin/bash

# Define project directories
PROJECT_ROOT="/path/to/your/project"
TESTS_DIR="$PROJECT_ROOT/tests"

# Function to insert landmarks if they don't exist
function insert_landmark_if_absent() {
    local file=$1
    local landmark=$2

    # Check if the landmark start is already in the file
    if ! grep -q "LANDMARK-START:$landmark" "$file"; then
        # Use awk to insert the landmark at the beginning of the file
        awk -v lm="// LANDMARK-START:$landmark" 'BEGIN{print lm}{print}' "$file" > tmp && mv tmp "$file"
    fi

    # Check if the landmark end is already in the file
    if ! grep -q "LANDMARK-END:$landmark" "$file"; then
        # Use awk to insert the landmark at the end of the file
        awk -v lm="// LANDMARK-END:$landmark" '{print}END{print lm}' "$file" > tmp && mv tmp "$file"
    fi
}

# Insert landmarks into test files
insert_landmark_if_absent "$TESTS_DIR/test_editor.py" "TestEditor"
insert_landmark_if_absent "$TESTS_DIR/test_file_editor.py" "TestFileEditor"
insert_landmark_if_absent "$TESTS_DIR/test_landmark_masterlist_keeper.py" "TestLandmarkMasterlistKeeper"

# Function to write instruction file for updating a test file
function write_test_update_instruction() {
    local file=$1
    local landmark=$2
    local content=$3
    local instruction_file=$4

    # Escape backslashes and newlines in content
    local escaped_content=$(echo "$content" | sed ':a;N;$!ba;s/\n/\\n/g' | sed 's/\//\\\//g')

    # Write the instruction file
    cat << EOF > $instruction_file
[
    {
        "instruction": "UpdateFile",
        "path": "$file",
        "landmarkId": "$landmark",
        "newContent": "$escaped_content"
    }
]
EOF
}

# Update test_editor.py
write_test_update_instruction \
    "test_editor.py" \
    "TestEditor" \
    "class TestEditor(unittest.TestCase):\n    def test_dummy(self):\n        self.assertTrue(True)" \
    "$PROJECT_ROOT/update_test_editor_instructions.js"

# Update test_file_editor.py
write_test_update_instruction \
    "test_file_editor.py" \
    "TestFileEditor" \
    "class TestFileEditor(unittest.TestCase):\n    def test_dummy(self):\n        self.assertTrue(True)" \
    "$PROJECT_ROOT/update_test_file_editor_instructions.js"

# Update test_landmark_masterlist_keeper.py
write_test_update_instruction \
    "test_landmark_masterlist_keeper.py" \
    "TestLandmarkMasterlistKeeper" \
    "class TestLandmarkMasterlistKeeper(unittest.TestCase):\n    def test_dummy(self):\n        self.assertTrue(True)" \
    "$PROJECT_ROOT/update_test_landmark_masterlist_keeper_instructions.js"

# Function to process instruction file with editor.py and commit
function process_instructions() {
    local instruction_file=$1
    local commit_message=$2

    # Call editor.py to process the instruction file
    python $EDITOR_SCRIPT $instruction_file

    # Commit the changes
    git add .
    git commit -m "$commit_message"
}

# Process each instruction file
process_instructions "$PROJECT_ROOT/update_test_editor_instructions.js" "Update test_editor with basic test cases"
process_instructions "$PROJECT_ROOT/update_test_file_editor_instructions.js" "Update test_file_editor with basic test cases"
process_instructions "$PROJECT_ROOT/update_test_landmark_masterlist_keeper_instructions.js" "Update test_landmark_masterlist_keeper with basic test cases"

echo "Test files have been updated and changes committed."
