from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List, Optional


@dataclass_json
@dataclass
class InstallConfig:
    run: List[str]
    cwd: Optional[str] = None
