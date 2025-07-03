import os
import pickle
from epigame.utils import Record, Struct  # Import every class that might be in the pickle

class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Redirect misnamed classes from __main__ to actual module
        if module == "__main__":
            if name == "Record":
                return Record
            if name == "Struct":
                return Struct
        return super().find_class(module, name)

def load_safely(filepath):
    with open(filepath, "rb") as f:
        return SafeUnpickler(f).load()

def migrate_pickle_file(filepath):
    try:
        data = load_safely(filepath)
        with open(filepath, "wb") as f:
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"Migrated: {filepath}")
    except Exception as e:
        print(f"Failed to migrate {filepath}: {e}")

def migrate_directory(folder, extensions=(".prep", ".res")):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(extensions):
                migrate_pickle_file(os.path.join(root, file))


if __name__ == "__main__":
    folder_to_fix = "data/output/connectivity"
    migrate_directory(folder_to_fix)
