from pathlib import Path
from pydantic import BaseModel


class ReceivedData(BaseModel):

    images: list[str]
    filenames: list[str]
    username: str


class InferenceInstance(BaseModel):
    """Class to keep track of inference instance"""

    id: str  # uniqueID in case of simultaneous requests for dental assessments
    image_path: Path


class Progress(BaseModel):
    """Class used to keep track of progress of receiving data and inference"""

    percentage: int
