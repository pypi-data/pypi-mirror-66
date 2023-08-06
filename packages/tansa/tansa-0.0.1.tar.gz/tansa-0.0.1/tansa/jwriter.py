import json


class JWriter():
    def json_screen_writer(self, values):
        for j in values:
            j_out = json.dumps(j, indent=4, ensure_ascii=False)
        return print(j_out)