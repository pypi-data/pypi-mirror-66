from typing import Optional


class BlocksActionBuilder(object):
    def __init__(self):
        super().__init__()

        self._data = {"type": "blocks", "blocks": []}

    def build(self):
        return self._data

    def add_block(self, block):
        self._data["blocks"].append(block)
        return self

    def add_text(self, content: str):
        return self.add_block({"type": "text", "content": content})

    def add_youtube_video(self, videoId: str):
        return self.add_block({"type": "youTubeVideo", "videoId": videoId,})

    def add_web_page(self, url: str):
        return self.add_block({"type": "webPage", "url": url,})

    def add_note(self, text: str):
        return self.add_block({"type": "note", "text": text,})

    def add_text_field(self, title: str, required: bool = False, id: Optional[str] = None):
        return self.add_block(
            {"type": "textField", "title": title, "required": required, "id": id,}
        )

    def add_image_field(self, title: str, required: bool = False, id: Optional[str] = None):
        return self.add_block(
            {"type": "imageField", "title": title, "required": required, "id": id,}
        )

    def add_date_time_field(self, title: str, required: bool = False, id: Optional[str] = None):
        return self.add_block(
            {"type": "dateTimeField", "title": title, "required": required, "id": id,}
        )

    def add_scale_field(
        self,
        title: str,
        required: bool = False,
        min: int = 0,
        max: int = 10,
        step: int = 1,
        id: Optional[str] = None,
    ):
        return self.add_block(
            {
                "type": "scaleField",
                "title": title,
                "required": required,
                "id": id,
                "min": min,
                "max": max,
                "step": step,
            }
        )

    def add_multiple_choice_field(
        self, title: str, required: bool = False, choices: list = [], id: Optional[str] = None
    ):
        return self.add_block(
            {
                "type": "multipleChoiceField",
                "title": title,
                "required": required,
                "id": id,
                "choices": choices,
            }
        )

    def add_number_field(
        self,
        title: str,
        required: bool = False,
        min: int = 0,
        max: int = 10,
        step: int = 1,
        id: Optional[str] = None,
    ):
        return self.add_block(
            {
                "type": "numberField",
                "title": title,
                "required": required,
                "id": id,
                "min": min,
                "max": max,
                "step": step,
            }
        )
