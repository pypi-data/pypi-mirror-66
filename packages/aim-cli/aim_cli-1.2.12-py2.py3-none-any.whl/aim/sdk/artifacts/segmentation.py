from typing import Any, Optional

from aim.sdk.artifacts.artifact import Artifact
from aim.sdk.artifacts.record import Record
from aim.sdk.artifacts.media import Media


class Segmentation(Artifact):
    cat = ('segmentation',)

    def __init__(self, name: str, obj: Media, mask: Any,
                 class_labels: Optional[dict] = None):
        self.name = name
        self.obj = obj
        self.mask = mask
        self.class_labels = class_labels

        super(Segmentation, self).__init__(self.cat)

    def serialize(self):
        content = {
            'cat': self.obj.cat[-1],
            'path': self.obj.path,
            'mask': self.mask,
        }

        return Record(
            name=self.name,
            cat=self.cat,
            content=content,
            data={
                'class_labels': self.class_labels,
            }
        )

    def save_blobs(self, name: str, abs_path: str = None):
        pass
