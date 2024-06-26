from django import forms
import json

class JSONEditorWidget(forms.Textarea):
    def format_value(self, value):
        if isinstance(value, str):
            return value
        return json.dumps(value, indent=4)
