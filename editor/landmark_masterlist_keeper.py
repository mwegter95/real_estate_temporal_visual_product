# Python code for landmark_masterlist_keeper.py
# life_assistant_app/editor/landmark_masterlist_keeper.py

import json
import os

class LandmarkMasterlistKeeper:
    def __init__(self, project_root, masterlist_file='masterlist.log'):
        # Ensure the masterlist file path is constructed properly
        self.masterlist_file = os.path.join(project_root, masterlist_file)
        self.masterlist = self._load_masterlist()

    def _load_masterlist(self):
        # Load the existing master list from the file, if it exists
        if os.path.exists(self.masterlist_file):
            with open(self.masterlist_file, 'r') as file:
                return json.load(file)
        return []

    def register_landmark(self, landmark):
        # Ensure the landmark id and uuid are unique
        if any(lm['id'] == landmark['id'] for lm in self.masterlist):
            raise ValueError(f"Landmark ID '{landmark['id']}' is already in use.")
        if any(lm['uuid'] == landmark['uuid'] for lm in self.masterlist):
            raise ValueError(f"Landmark UUID '{landmark['uuid']}' is already in use.")

        self.masterlist.append(landmark)
        self._write_masterlist_to_file()

    def update_landmark(self, uuid, new_landmark):
        # Find the landmark with the given uuid and update it
        for index, lm in enumerate(self.masterlist):
            if lm['uuid'] == uuid:
                # Ensure the new id is also unique if it has changed
                if 'id' in new_landmark and new_landmark['id'] != lm['id'] and \
                        any(lm['id'] == new_landmark['id'] for lm in self.masterlist):
                    raise ValueError(f"New landmark ID '{new_landmark['id']}' is already in use.")
                self.masterlist[index] = new_landmark
                break
        self._write_masterlist_to_file()

    def _write_masterlist_to_file(self):
        # Write the masterlist to a file in a JSON format
        with open(self.masterlist_file, 'w') as file:
            json.dump(self.masterlist, file, indent=4)

    def get_landmark_history(self, uuid):
        return [h for h in self.history if h['landmark']['uuid'] == uuid or h.get('old_landmark', {}).get('uuid', '') == uuid]

    def get_masterlist(self):
        return self.masterlist

