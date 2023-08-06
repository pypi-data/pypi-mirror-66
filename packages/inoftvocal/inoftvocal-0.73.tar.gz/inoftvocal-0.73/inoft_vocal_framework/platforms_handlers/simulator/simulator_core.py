import os
from json import load as json_load
from json import loads as json_loads


class Simulator:
    def __init__(self, event_type: str):
        self.current_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.request_samples_folderpath = os.path.join(self.current_dir_path, "request_samples")
        self.event_file_filepath = os.path.join(self.request_samples_folderpath, f"{event_type}.json")
        if not os.path.isfile(self.event_file_filepath):
            raise Exception(f"No event file was found at {self.event_file_filepath}. Please use a valid event_type name.")

    def get_event_and_context(self) -> (str, str):
        # For the simulator, we want the event and the context to be in the form of
        # strings, not in dicts. So we do not load them by using the json module.
        event = None
        with open(self.event_file_filepath, "r") as request_file:
            try:
                event = json_load(request_file)
            except Exception as e:
                try:
                    event = request_file.read()
                except Exception as e2:
                    print(e2)
            # todo: improve the json processing, since this way of replacing could replace some important informations in the actual request/response

        context = None

        return event, context
