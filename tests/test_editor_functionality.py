import unittest
import subprocess
import os
import time
import sys

class TestEditorFunctionality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestEditorFunctionality, cls).setUpClass()
        cls.editor_script = os.path.join(os.path.dirname(__file__), '..', 'editor', 'editor.py')
        cls.project_root = os.path.join(os.path.dirname(__file__), '..')

    def test_update_file_instruction(self):
        instruction_file = os.path.join(self.project_root, 'update_instruction.json')
        dummy_file_path = os.path.join(self.project_root, 'tests', 'dummy_file.py')


        # Instruction content to update a dummy file
        instruction_content = '''[
            {
                "instruction": "UpdateFile",
                "path": "tests/dummy_file.py",
                "landmarkId": "DummyContent",
                "newContent": "# LANDMARK-START:DummyContent\\n# New content\\n# LANDMARK-END:DummyContent"
            }
        ]'''

        # Write the instruction to the instruction file
        with open(instruction_file, 'w') as file:
            file.write(instruction_content)

        # Path to the dummy file that will be updated
        dummy_file_path = os.path.join(self.project_root, 'tests', 'dummy_file.py')

        # Initial content for the dummy file
        initial_dummy_content = '''# LANDMARK-START:DummyContent
# Original content
# LANDMARK-END:DummyContent'''

        # Write the initial content to the dummy file
        with open(dummy_file_path, 'w') as file:
            file.write(initial_dummy_content)

        # Start the editor.py script in the background
        process = subprocess.Popen(
            ['python', self.editor_script, instruction_file, '--root'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        # Implementing a timeout mechanism
        timeout = time.time() + 1*1  # 1 seconds from now
        while True:
            if process.poll() is not None:  # Checks if process has ended
                break
            if time.time() > timeout:  # Checks if current time is past the timeout
                process.kill()  # Kills the process
                self.fail("The editor.py script timed out")
                break
            time.sleep(0.1)  # Sleep for a short time to avoid busy waiting

        # Read the output
        stdout, _ = process.communicate()
        print(stdout.decode())

        # Verify that the content was updated
        with open(dummy_file_path, 'r') as file:
            updated_content = file.read()

        # Check if new content is in the updated file content
        self.assertIn('# New content', updated_content)

if __name__ == '__main__':
    unittest.main()
