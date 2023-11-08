# Python code for editor.py
import re
from landmark_masterlist_keeper import LandmarkMasterlistKeeper
import os
import uuid
import argparse
import subprocess
import json

class LandmarkParser:
    # Regex patterns for landmarks
    LANDMARK_START_PATTERN = re.compile(r'# LANDMARK-START:(\w+)')
    LANDMARK_END_PATTERN = re.compile(r'# LANDMARK-END:(\w+)')

    def find_complex_landmarks(self, content):
        """Find landmarks and their start/end positions in the content."""
        landmarks = []
        start_positions = {}

        lines = content.splitlines()

        # Debug: print the number of lines read
        print(f"Number of lines in content: {len(lines)}")

        for idx, line in enumerate(lines):
            print(f"Processing line {idx}: {line}")  # Debug: print each line being processed
            start_match = self.LANDMARK_START_PATTERN.match(line)
            end_match = self.LANDMARK_END_PATTERN.match(line)

            if start_match:
                lm_id = start_match.group(1)
                start_positions[lm_id] = idx
                print(f"Found start landmark: {lm_id}")  # Debug: print when a start landmark is found
            elif end_match:
                lm_id = end_match.group(1)
                start_line = start_positions.pop(lm_id, None)
                if start_line is not None:
                    landmarks.append({
                        'id': lm_id,
                        'start_line': start_line,
                        'end_line': idx
                    })
                    print(f"Found end landmark: {lm_id}")  # Debug: print when an end landmark is found

        # Debug: print all the landmarks found
        print(f"Landmarks found: {landmarks}")

        return landmarks

class FileEditor:
    def __init__(self, project_root, parser: LandmarkParser, masterlist_keeper: LandmarkMasterlistKeeper):
        self.project_root = project_root
        self.parser = parser
        self.masterlist_keeper = masterlist_keeper

    def apply_changes(self, content, change):
        landmarks = self.parser.find_complex_landmarks(content)
        lines = content.split('\n')
        updated = False  # Flag to check if updates have been made

        # Directly access the keys from the change dictionary
        lm_id = change['landmarkId']
        action = change['instruction']
        new_content = change['newContent']

        lm = next((lm for lm in landmarks if lm['id'] == lm_id), None)
        if not lm:
            print(f"Landmark {lm_id} not found.")  # Debugging
            return content

        if action == 'UpdateFile':
            print(f"Replacing content for landmark {lm_id}.")  # Debugging
            before = lines[:lm['start_line']]
            after = lines[lm['end_line'] + 1:]
            lines = before + [new_content.strip()] + after
            updated = True

        if updated:
            updated_content = '\n'.join(lines)
            print(f"Updated content:\n{updated_content}")  # Debugging
            return updated_content
        else:
            print("No updates applied.")  # Debugging
            return content


    def create_file(self, file_path, content):
        full_path = os.path.join(self.project_root, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Debug print
        print(f"Creating file at: {full_path}")
        print(f"With content: {content}")

        with open(full_path, 'w') as file:
            file.write(content)
    
    def apply_instruction_file(self, instruction_file_path):
        with open(instruction_file_path, 'r') as file:
            instructions_content = file.read()
        self.apply_instructions(instructions_content)

    def apply_instructions(self, instructions):
        for instruction in instructions:
            if instruction['instruction'] == 'UpdateFile':
                file_path = instruction['path']
                full_file_path = os.path.join(self.project_root, file_path)
                with open(full_file_path, 'r') as file:
                    content = file.read()
                updated_content = self.apply_changes(content, instruction)  # Pass the single instruction dictionary
                with open(full_file_path, 'w') as file:
                    file.write(updated_content)
            elif instruction['instruction'] == 'CreateFile':
                file_path = instruction['path']
                content = instruction.get('content', '')  # Default to empty string if 'content' key is not present
                self.create_file(file_path, content)

    def _extract_path(self, block):
        # Extract the file path from the instruction block
        path_match = re.search(r'PATH: ([^\n]+)', block)
        if path_match:
            return path_match.group(1).strip()
        else:
            raise ValueError("No PATH found in the instruction block")

    def _extract_landmark_id(self, block):
        # Extract the landmark ID from the instruction block
        landmark_id_match = re.search(r'LANDMARK: (\w+)', block)
        if landmark_id_match:
            return landmark_id_match.group(1).strip()
        else:
            raise ValueError("No LANDMARK ID found in the instruction block")

    def _handle_create_file_instruction(self, block):
        # Debug print the block being processed
        print("Processing block:", block)

        # Extract file path
        path_match = re.search(r'PATH: ([^\*]+)\*/', block)
        if path_match:
            file_path = path_match.group(1).strip()
        else:
            raise ValueError("No file path found in the instruction block")

        # Extract landmark ID
        landmark_id_match = re.search(r'// LANDMARK-START:(\w+)', block)
        if landmark_id_match:
            landmark_id = landmark_id_match.group(1)
        else:
            raise ValueError("No landmark id found in the instruction block")

        # Extract content
        content_match = re.search(r'\*/(.*?)/* INSTRUCTION:', block, re.DOTALL)
        if content_match:
            content = content_match.group(1).strip()
        else:
            content = block.split('*/', 1)[1].strip()

        # Debug print extracted information
        print("File path:", file_path)
        print("Landmark ID:", landmark_id)
        print("Content:", content)

        # Create file and register landmark
        self.create_file(file_path, content)
        landmark_uuid = str(uuid.uuid4())
        self.masterlist_keeper.register_landmark({
            'uuid': landmark_uuid,
            'id': landmark_id,
            'file_path': file_path,
            'description': f'Created file at {file_path}'
        })

    def _handle_insert_content_instruction(self, block):
        # Similar to _handle_create_file_instruction, but for inserting content
        pass

    # ... additional methods for parsing and handling other types of instructions ...

    def _generate_uuid(self):
        # Return a new unique identifier
        return str(uuid.uuid4())
    
    def execute_js_instructions(self, js_file_path):
        with open(js_file_path, 'r') as js_file:
            instructions_content = js_file.read()
        self.apply_instructions(instructions_content)

    def process_create_file_instruction(self, file_path, content, landmark_id):
        # Create the file with the given content
        self.create_file(file_path, content)
        # Generate a unique UUID for the landmark
        uuid = str(uuid.uuid4())
        # Register the new landmark with its UUID and identifier
        self.masterlist_keeper.register_landmark({
            'uuid': uuid,
            'id': landmark_id,
            'file_path': file_path,
            'description': f'File created for {landmark_id}'
        })

    def _find_code_after_landmark(self, content, landmark_id, code_snippet_regex):
        """
        Find the position in 'content' of a code snippet that matches 'code_snippet_regex'
        occurring after the landmark identified by 'landmark_id'.
        """
        # Find all landmarks first
        landmarks = self.parser.find_complex_landmarks(content)
        landmark = next((lm for lm in landmarks if lm['id'] == landmark_id), None)
        print("landmarks: ", landmarks)
        print("landmark: ", landmark)

        if not landmark:
            raise ValueError(f"Landmark '{landmark_id}' not found.")

        # Find the position of the end of the landmark
        end_of_landmark_pos = self._get_position(content, landmark['end_line'])

        # Perform a regex search for the code snippet starting from the end of the landmark
        code_snippet_match = re.search(code_snippet_regex, content[end_of_landmark_pos:], re.DOTALL)

        if not code_snippet_match:
            raise ValueError(f"Code snippet regex '{code_snippet_regex}' not found after landmark '{landmark_id}'.")

        # Calculate the position relative to the start of the content
        snippet_pos = end_of_landmark_pos + code_snippet_match.start()

        return snippet_pos

    def _get_position(self, content, line_num):
        """
        Get the character position in 'content' corresponding to the start of 'line_num'.
        """
        lines = content.splitlines(keepends=True)
        return sum(len(lines[i]) for i in range(line_num))
    
    def _handle_update_file_instruction(self, block, content):
        # Extract file path and code snippet regex from the block
        file_path = self._extract_path(block)
        code_snippet_regex = self._extract_code_snippet_regex(block)

        # Check if a landmark ID is provided and find the content to update after the landmark
        if 'AFTER LANDMARK:' in block:
            landmark_id = self._extract_landmark_id(block)
            position_to_update = self._find_code_after_landmark(content, landmark_id, code_snippet_regex)
        else:
            # If no landmark ID is provided, find the position using just the regex
            snippet_match = re.search(code_snippet_regex, content, re.DOTALL)
            if snippet_match:
                position_to_update = snippet_match.start()
            else:
                raise ValueError(f"Code snippet regex '{code_snippet_regex}' not found.")

        # Extract the actual new content to insert from the block
        new_content = self._extract_new_content(block)

        # Replace the content at the found position with the new content
        updated_content = self._replace_content_at_position(content, position_to_update, new_content, code_snippet_regex)

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(updated_content)

        # If a landmark ID was provided, use it in the commit message
        if 'AFTER LANDMARK:' in block:
            self.commit_change(file_path, f"Updated code after landmark {landmark_id}")
        else:
            self.commit_change(file_path, f"Updated code matching pattern: {code_snippet_regex}")

    def _extract_code_snippet_regex(self, block):
        # Extract the regex pattern for the code snippet
        regex_pattern_match = re.search(r'CODE SNIPPET REGEX: (.*)', block)
        if regex_pattern_match:
            return regex_pattern_match.group(1).strip()
        else:
            raise ValueError("No CODE SNIPPET REGEX found in the instruction block")
    
    def _extract_new_content(self, block):
        # Extract the new content from the instruction block
        # Assuming new content is enclosed within specific markers, e.g., /* START-CONTENT */ and /* END-CONTENT */
        new_content_match = re.search(r'/\* START-CONTENT \*/(.*?)/\* END-CONTENT \*/', block, re.DOTALL)
        if new_content_match:
            return new_content_match.group(1).strip()
        else:
            raise ValueError("No new content found within content markers")

    def _replace_content_at_position(self, content, position_to_update, new_content, code_snippet_regex):
        # Find the old content using the code snippet regex
        old_content_match = re.search(code_snippet_regex, content[position_to_update:], re.DOTALL)
        if old_content_match:
            # Replace the old content with the new content
            return content[:position_to_update] + re.sub(code_snippet_regex, new_content, content[position_to_update:], count=1)
        else:
            raise ValueError("The code snippet regex did not match any content after the specified landmark")

    
    

def commit_change(file_path, change_description):
    """Commit a file change to the git repository."""
    try:
        # Check if the file is tracked in git
        git_ls_files = subprocess.run(['git', 'ls-files', file_path], check=True, text=True, capture_output=True)
        if not git_ls_files.stdout.strip():
            # If the file is not tracked, add it
            subprocess.run(['git', 'add', file_path], check=True)
        # Commit the change
        commit_message = f"Update {file_path}: {change_description}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"Successfully committed changes for {file_path}: {change_description}")  # Debug: print successful commit
    except subprocess.CalledProcessError as e:
        print(f"Failed to commit changes: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process DSL instructions for file editing.')
    parser.add_argument('instruction_file', help='The path to the .js instruction file')
    
    # Add optional arguments for specifying the project root
    parser.add_argument('--root', action='store_true', help='Use the project root for file changes.')
    parser.add_argument('--react', action='store_true', help='Use the React app root for file changes.')

    args = parser.parse_args()

    # Set the project_root based on the provided arguments
    if args.root:
        # If --root is specified, use the current directory as the project root
        project_root = os.getcwd()
        print(f"Using the current directory as the project root: {project_root}")
    elif args.react:
        # If --react is specified, use the real_estate_temporal_visual_react/src directory as the project root
        project_root = os.path.join(os.getcwd(), 'real_estate_temporal_visual_react', 'src')
        print(f"Using the React app root for file changes: {project_root}")
    else:
        # Default to using the current directory as the project root if no flags are provided
        project_root = os.getcwd()
        print(f"No specific root flag provided, using the current directory as the project root: {project_root}")

    # Instantiate FileEditor with the appropriate project_root
    parser_instance = LandmarkParser()
    masterlist_keeper = LandmarkMasterlistKeeper(project_root)
    file_editor = FileEditor(project_root, parser_instance, masterlist_keeper)

    # Load the instructions from the .js file
    with open(args.instruction_file, 'r') as file:
        instructions = json.load(file)
    print(f"Loaded instructions: {instructions}")  # Debugging: print loaded instructions

    # Process the instructions
    file_editor.apply_instructions(instructions)