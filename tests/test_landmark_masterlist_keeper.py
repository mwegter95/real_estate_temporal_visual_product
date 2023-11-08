
import unittest
from editor.landmark_masterlist_keeper import LandmarkMasterlistKeeper
import os
import tempfile
import uuid

class TestLandmarkMasterlistKeeper(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the masterlist file
        self.test_dir = tempfile.TemporaryDirectory()
        self.masterlist_file_path = os.path.join(self.test_dir.name, 'masterlist.log')
        self.masterlist_keeper = LandmarkMasterlistKeeper(self.test_dir.name, self.masterlist_file_path)

    def tearDown(self):
        # Clean up the temporary directory after tests
        self.test_dir.cleanup()

    def test_register_landmark(self):
        landmark = {
            'id': 'test_landmark',
            'uuid': str(uuid.uuid4()),
            'file_path': 'some/file/path',
            'description': 'A test landmark'
        }
        self.masterlist_keeper.register_landmark(landmark)
        self.assertIn(landmark, self.masterlist_keeper.get_masterlist())

    def test_update_landmark(self):
        landmark = {
            'id': 'test_landmark',
            'uuid': str(uuid.uuid4()),
            'file_path': 'some/file/path',
            'description': 'A test landmark'
        }
        self.masterlist_keeper.register_landmark(landmark)

        new_description = 'Updated description'
        landmark['description'] = new_description
        self.masterlist_keeper.update_landmark(landmark['uuid'], landmark)
        updated_landmark = next((lm for lm in self.masterlist_keeper.get_masterlist() if lm['uuid'] == landmark['uuid']), None)
        self.assertEqual(new_description, updated_landmark['description'])

    def test_landmark_id_uniqueness(self):
        landmark = {
            'id': 'test_landmark',
            'uuid': str(uuid.uuid4()),
            'file_path': 'some/file/path',
            'description': 'A test landmark'
        }
        self.masterlist_keeper.register_landmark(landmark)
        with self.assertRaises(ValueError):
            self.masterlist_keeper.register_landmark(landmark)

    def test_landmark_uuid_uniqueness(self):
        landmark = {
            'id': 'test_landmark',
            'uuid': str(uuid.uuid4()),
            'file_path': 'some/file/path',
            'description': 'A test landmark'
        }
        another_landmark = {
            'id': 'another_test_landmark',
            'uuid': landmark['uuid'],  # Duplicate UUID
            'file_path': 'another/file/path',
            'description': 'Another test landmark'
        }
        self.masterlist_keeper.register_landmark(landmark)
        with self.assertRaises(ValueError):
            self.masterlist_keeper.register_landmark(another_landmark)

    def test_get_landmark_history(self):
        landmark_uuid = str(uuid.uuid4())
        history = self.masterlist_keeper.get_landmark_history(landmark_uuid)
        self.assertIsInstance(history, list)

    def test_load_masterlist(self):
        self.assertIsInstance(self.masterlist_keeper.get_masterlist(), list)

if __name__ == '__main__':
    unittest.main()
