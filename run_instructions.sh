#!/bin/bash

# Define the root directory of your project as the current directory
PROJECT_ROOT="./"

# Define the path to the editor.py script
EDITOR_SCRIPT="$PROJECT_ROOT/editor/editor.py"

# Array of instruction files
declare -a INSTRUCTION_FILES=("update_test_editor_instructions.js"
                              "update_test_file_editor_instructions.js"
                              "update_test_landmark_masterlist_keeper_instructions.js")

# Function to apply instructions from a file and commit changes
function apply_instructions_and_commit() {
    local instruction_file=$1
    local commit_message=$2

    # Apply the instructions using the editor script
    python $EDITOR_SCRIPT $instruction_file

    # Add the changes to the staging area and commit them
    git add -A
    git commit -m "$commit_message"
}

# Iterate over the instruction files and process them
for instruction_file in "${INSTRUCTION_FILES[@]}"; do
    # Construct the commit message based on the instruction file name
    commit_message="Processed instructions from ${instruction_file%.*}"

    # Call the function to apply the instructions and commit changes
    apply_instructions_and_commit "$PROJECT_ROOT/$instruction_file" "$commit_message"
done

echo "All instruction files have been processed and changes committed."
