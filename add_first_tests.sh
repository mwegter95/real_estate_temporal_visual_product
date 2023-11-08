#!/bin/bash

# Define the root directory of your project
PROJECT_ROOT="./"

# Define the path to the editor.py script
EDITOR_SCRIPT="$PROJECT_ROOT/editor/editor.py"

# Instructions JSON file path
INSTRUCTIONS_FILE="$PROJECT_ROOT/instructions.json"

# Define the initial set of landmarks and instructions in a JSON format
cat << EOF > $INSTRUCTIONS_FILE
[
  {
    "instruction": "CreateFile",
    "path": "src/tests/map_integration.test.js",
    "content": "// LANDMARK-START:MAP-INTEGRATION\n// Test cases for Google Maps API loading\n// LANDMARK-END:MAP-INTEGRATION"
  },
  {
    "instruction": "CreateFile",
    "path": "src/tests/sunlight_model.test.js",
    "content": "// LANDMARK-START:SUNLIGHT-MODEL\n// Test cases for sunlight path modeling\n// LANDMARK-END:SUNLIGHT-MODEL"
  },
  {
    "instruction": "CreateFile",
    "path": "src/tests/ui_viewpoint.test.js",
    "content": "// LANDMARK-START:UI-VIEWPOINT\n// Test cases for UI viewpoint selection\n// LANDMARK-END:UI-VIEWPOINT"
  }
]
EOF

# Function to run the editor script and commit changes
function apply_instructions_and_commit() {
  local message=$1

  # Apply the instructions using the editor script
  python $EDITOR_SCRIPT $INSTRUCTIONS_FILE

  # Commit the changes to the git repository
  git add .
  git commit -m "$message"
}

# Apply the initial instructions and commit
apply_instructions_and_commit "Initialize project with foundational test cases"

# Check if more changes need to be applied recursively
# This loop will run until the editor script reports no more changes
while true; do
  # Apply the instructions
  python $EDITOR_SCRIPT $INSTRUCTIONS_FILE

  # Check the status of the repository to see if there are changes
  if ! git diff-index --quiet HEAD --; then
    # Commit the new changes
    apply_instructions_and_commit "Apply new changes from instructions"
  else
    # No more changes detected, break the loop
    break
  fi
done

echo "All instructions have been applied and changes committed."
