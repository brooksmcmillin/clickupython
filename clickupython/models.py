from abc import abstractmethod
from typing import (
    Optional,
    List,
    Any,
    Generator,
    Iterator,
    Sequence,
    TypeVar,
    Generic,
    Type,
)

from pydantic import BaseModel, Field


# Single entry dict that appears a lot
class EnabledBool(BaseModel):
    enabled: bool = False


# Class to hold a list of BaseModels
T = TypeVar("T")  # Define type variable T


class BaseModelList(Generic[T]):
    def __init__(self, **kwargs: dict[str, dict[str, Any]]) -> None:
        self.items: list[T] = []

        for json_item in kwargs[next(iter(kwargs))]:
            self.items.append(self.create_item(json_item))

    @abstractmethod
    def create_item(self, json_obj: dict[str, Any]) -> T: ...

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def __getitem__(self, index: int) -> T:
        return self.items[index]


class Status(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    color: Optional[str] = None

    orderindex: Optional[int] = None

    type: Optional[str] = None


class Priority(BaseModel):
    id: Optional[int] = None

    priority: Any = None
    color: Optional[str] = None

    orderindex: Optional[str] = None


# Reference: https://developer.clickup.com/reference/getspaces
class DueDates(BaseModel):
    # Required Fields
    enabled: bool
    start_date: bool
    remap_due_dates: bool
    remap_closed_due_date: bool


class TimeTracking(BaseModel):
    enabled: bool = False
    harvest: bool = False
    rollup: bool = False


class TagsStatus(BaseModel):
    enabled: bool = False


class TimeEstimateStatus(BaseModel):
    enabled: bool = False


class ChecklistsStatus(BaseModel):
    enabled: bool = False


class CustomFieldsStatus(BaseModel):
    enabled: bool = False


class RemapDependenciesStatus(BaseModel):
    enabled: bool = False


class DependencyWarning(BaseModel):
    enabled: bool = False


class PortfoliosStatus(BaseModel):
    enabled: bool = False


# Reference: https://developer.clickup.com/reference/getspaces
class Features(BaseModel):
    # Required Fields
    due_dates: DueDates
    time_tracking: TimeTracking
    tags: TagsStatus
    time_estimates: TimeEstimateStatus
    checklists: Optional[ChecklistsStatus] = None  # Says required, but not in response?

    # Optional Fields
    custom_fields: Optional[CustomFieldsStatus] = None
    remap_dependencies: Optional[RemapDependenciesStatus] = None
    dependency_warning: Optional[DependencyWarning] = None
    portfolios: Optional[PortfoliosStatus] = None


# Reference: https://developer.clickup.com/reference/getauthorizedteams
class User(BaseModel):
    # Required Fields
    id: int
    username: str
    color: str
    profilePicture: Optional[str]

    # Optional Fields
    initials: Optional[str] = None
    email: Optional[str] = None
    role: Optional[int] = None
    custom_role: Optional[None] = None
    last_active: Optional[str] = None
    date_joined: Optional[str] = None
    date_invited: Optional[str] = None


# Reference: https://developer.clickup.com/reference/getspaces
class Space(BaseModel):
    id: str
    name: Optional[str] = None

    private: Optional[bool] = None
    statuses: Optional[list[Status]] = None
    multiple_assignees: Optional[bool] = None
    features: Optional[Features] = None
    color: Optional[str] = None
    access: Optional[bool] = None
    admin_can_manage: Optional[bool] = None
    archived: Optional[bool] = None
    members: Optional[list[User]] = None


class Spaces(BaseModelList[Space]):
    def create_item(self, json_obj: dict[str, Any]) -> Space:
        return Space(**json_obj)


# Reference: https://developer.clickup.com/reference/getfolder
class Folder(BaseModel):
    id: str
    name: str
    orderindex: Optional[int] = None
    override_statuses: Optional[bool] = None
    hidden: bool
    space: Optional[Space] = None
    task_count: Optional[int] = None
    lists: Optional[list[dict[str, Any]]] = None


# Reference: https://developer.clickup.com/reference/getfolders
class Folders(BaseModelList[Folder]):
    def create_item(self, json_obj: dict[str, Any]) -> Folder:
        return Folder(**json_obj)


class ChecklistItem(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    orderindex: Optional[int] = None

    assignee: Optional[User]


class Checklist(BaseModel):
    id: Optional[str]

    task_id: Optional[str] = None
    name: Optional[str] = None

    orderindex: Optional[int] = None

    resolved: Optional[int] = None

    unresolved: Optional[int] = None

    items: Optional[List[ChecklistItem]] = None


class Checklists(BaseModelList[Checklist]):
    def create_item(self, json_obj: dict[str, Any]) -> Checklist:
        return Checklist(**json_obj)


class Attachment(BaseModel):
    id: str

    version: int
    date: str
    title: str

    extension: str

    thumbnail_small: str

    thumbnail_large: str
    url: str


class CommentComment(BaseModel):
    text: Optional[str] = None


class Comment(BaseModel):
    id: Optional[str] = None

    comment: Optional[list[CommentComment]] = None

    comment_text: Optional[str] = None

    user: Optional[User] = None

    resolved: Optional[bool] = None

    assignee: Optional[User] = None

    assigned_by: Optional[User] = None

    reactions: Optional[list[Any]] = None
    date: Optional[str] = None
    hist_id: Optional[str] = None


class Comments(BaseModelList[Comment]):
    def create_item(self, json_obj: dict[str, Any]) -> Comment:
        return Comment(**json_obj)


class Option(BaseModel):
    id: Optional[str]

    name: Optional[str]

    color: Optional[str]

    order_index: Optional[int]


class TypeConfig(BaseModel):
    default: Optional[int]

    placeholder: Optional[str]

    new_drop_down: Optional[bool]

    options: Optional[list[Option]]

    include_guests: Optional[bool]

    include_team_members: Optional[bool]


class CustomField(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    type: Optional[str] = None

    type_config: Optional[TypeConfig] = None
    date_created: Optional[str] = None

    hide_from_guests: Optional[bool] = None

    value: Optional[Any] = None

    required: Optional[bool] = None


class SpaceFeatures(BaseModel):
    due_dates: bool = False

    multiple_assignees: bool = False

    start_date: bool = False

    remap_due_dates: bool = False

    remap_closed_due_date: bool = False

    time_tracking: bool = False

    tags: bool = False

    time_estimates: bool = False

    checklists: bool = False

    custom_fields: bool = False

    remap_dependencies: bool = False

    dependency_warning: bool = False

    portfolios: bool = False

    points: bool = False

    custom_items: bool = False

    zoom: bool = False

    milestones: bool = False

    emails: bool = False

    @property
    def all_features(self) -> dict[str, Any]:
        return {
            "due_dates": {
                "enabled": self.due_dates,
                "start_date": self.start_date,
                "remap_due_dates": self.remap_due_dates,
                "remap_closed_due_date": self.remap_closed_due_date,
            },
            "time_tracking": {"enabled": self.time_tracking},
            "tags": {"enabled": self.tags},
            "time_estimates": {"enabled": self.time_estimates},
            "checklists": {"enabled": self.checklists},
            "custom_fields": {"enabled": self.custom_fields},
            "remap_dependencies": {"enabled": self.remap_dependencies},
            "dependency_warning": {"enabled": self.dependency_warning},
            "portfolios": {"enabled": self.portfolios},
            "milestones": {"enabled": self.milestones},
        }


class ClickupList(BaseModel):
    id: Optional[str] = None

# Reference: https://developer.clickup.com/reference/gettask
class Task(BaseModel):
    id: Optional[str] = None
    custom_id: Optional[str] = None
    name: Optional[str] = None

    text_content: Optional[str] = None
    description: Optional[str] = None

    status: Optional[Status] = None

    orderindex: Optional[str] = None
    date_created: Optional[str] = None
    date_updated: Optional[str] = None
    date_closed: Optional[str] = None

    creator: Optional[User] = None

    assignees: Optional[list[User]] = None

    task_checklists: Optional[List[Any]] = Field(None, alias="checklists")

    task_tags: Optional[List[Any]] = Field(None, alias="tags")
    parent: Optional[str] = None

    priority: Optional[Any] = None
    due_date: Optional[str] = None
    start_date: Optional[str] = None
    time_estimate: Optional[str] = None

    time_spent: Optional[str] = None

    custom_fields: Optional[List[CustomField]] = None
    list: Optional[ClickupList] = None

    folder: Optional[Folder] = None

    space: Optional[Space] = None
    url: Optional[str] = ""


class Tasks(BaseModelList[Task]):
    def create_item(self, json_obj: dict[str, Any]) -> Task:
        return Task(**json_obj)


class Member(BaseModel):
    user: User
    invited_by: Optional[User] = None


class Members(BaseModelList[User]):
    def create_item(self, json_obj: dict[str, Any]) -> User:
        return User(**json_obj)


# Reference: https://developer.clickup.com/reference/getauthorizedteams
class Team(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None

    avatar: Optional[str] = None

    members: Optional[List[Member]] = None


class Teams(BaseModelList[Team]):
    def create_item(self, json_obj: dict[str, Any]) -> Team:
        return Team(**json_obj)


class Goal(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    team_id: Optional[int] = None
    date_created: Optional[str] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    description: Optional[str] = None

    private: Optional[bool] = None

    archived: Optional[bool] = None
    creator: Optional[int] = None
    color: Optional[str] = None

    pretty_id: Optional[int] = None

    multiple_owners: Optional[bool] = None
    folder_id: Optional[str] = None

    members: Optional[List[User]] = None

    owners: Optional[List[User]] = None

    key_results: Optional[list[Any]] = None
    percent_completed: Optional[int] = None

    history: Optional[list[Any]] = None

    pretty_url: Optional[str] = None


class Goals(BaseModelList[Goal]):
    def create_item(self, json_obj: dict[str, Any]) -> Goal:
        return Goal(**json_obj)


class Tag(BaseModel):
    name: Optional[str] = None

    tag_fg: Optional[str] = None

    tag_bg: Optional[str] = None


class Tags(BaseModelList[Tag]):
    def create_item(self, json_obj: dict[str, Any]) -> Tag:
        return Tag(**json_obj)


class Shared(BaseModel):
    tasks: Optional[list[Task]]
    lists: Optional[list[dict[str, Any]]]
    folders: Optional[list[Folder]]


class SharedHierarchy(BaseModel):
    shared: Shared


class TimeTrackingData(BaseModel):
    id: str = ""
    task: Optional[Task] = None
    wid: str = ""
    user: Optional[User] = None
    billable: bool = False
    start: str = ""
    end: str = ""
    duration: Optional[int] = None
    description: str = ""
    tags: Optional[list[Tag]] = None
    source: str = ""
    at: str = ""


class TimeTrackingDataList(BaseModel):
    items: list[TimeTrackingData] = Field([], alias="data")


class TimeTrackingDataSingle(BaseModel):
    data: Optional[TimeTrackingData] = None
