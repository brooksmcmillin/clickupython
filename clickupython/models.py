from typing import Optional, List, Any

from pydantic import BaseModel, ValidationError, validator, Field

class StatusElement(BaseModel):
    id: Optional[str]
    status: str

    orderindex: int
    color: str

    type: str


class Assignee(BaseModel):
    id: Optional[str] = None
    color: Optional[str] = None
    username: Optional[str] = None
    initials: Optional[str] = None

    profilePicture: Optional[str] = None


class ListFolder(BaseModel):
    id: str
    name: str

    hidden: Optional[bool]

    access: bool

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


class SingleList(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    deleted: Optional[bool] = None

    archived: Optional[bool] = None

    orderindex: Optional[int] = None

    override_statuses: Optional[bool] = None

    priority: Optional[Priority] = None

    assignee: Optional[Assignee] = None
    due_date: Optional[str] = None
    start_date: Optional[str] = None

    folder: Optional[ListFolder] = None

    space: Optional[ListFolder] = None

    statuses: Optional[List[StatusElement]] = None

    inbound_address: Optional[str] = None

    permission_level: Optional[str] = None

    content: Optional[str] = None

    status: Optional[Status] = None

    task_count: Optional[int] = None

    start_date_time: Optional[str] = None

    due_date_time: Optional[bool] = None

    # return a single list

    def build_list(self):
        return SingleList(**self)


class AllLists(BaseModel):
    lists: Optional[List[SingleList]] = None

    # return a list of lists

    def build_lists(self):
        return AllLists(**self)


class ChecklistItem(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    orderindex: Optional[int] = None

    assignee: Optional[Assignee]


class Checklist(BaseModel):
    id: Optional[str]

    task_id: Optional[str] = None
    name: Optional[str] = None

    orderindex: Optional[int] = None

    resolved: Optional[int] = None

    unresolved: Optional[int] = None

    items: Optional[List[ChecklistItem]] = None

    def add_item(self, client_instance, name: str, assignee: Optional[str] = None):
        return client_instance.create_checklist_item(
            self.id, name=name, assignee=assignee
        )


class Checklists(BaseModel):
    checklist: Checklist

    def build_checklist(self):
        final_checklist = Checklists(**self)

        return final_checklist.checklist


class Attachment(BaseModel):
    id: str

    version: int
    date: str
    title: str

    extension: str

    thumbnail_small: str

    thumbnail_large: str
    url: str

    def build_attachment(self):
        return Attachment(**self)


class User(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    initials: Optional[str] = None
    email: Optional[str] = None
    color: Optional[str] = None

    profilePicture: Optional[str] = None

    role: Optional[int] = None

    custom_role: Optional[None] = None

    last_active: Optional[str] = None

    date_joined: Optional[str] = None

    date_invited: Optional[str] = None


class AssignedBy(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    initials: Optional[str] = None
    email: Optional[str] = None
    color: Optional[str] = None
    profile_picture: Optional[str] = None


class CommentComment(BaseModel):
    text: Optional[str] = None


class Comment(BaseModel):
    id: Optional[str] = None

    comment: Optional[List[CommentComment]] = None

    comment_text: Optional[str] = None

    user: Optional[AssignedBy] = None

    resolved: Optional[bool] = None

    assignee: Optional[AssignedBy] = None

    assigned_by: Optional[AssignedBy] = None

    reactions: Optional[List[Any]] = None
    date: Optional[str] = None
    hist_id: Optional[str] = None

    def build_comment(self):
        return Comment(**self)


class Comments(BaseModel):
    comments: Optional[List[Comment]] = None

    def __iter__(self):
        return iter(self.comments)

    def build_comments(self):
        return Comments(**self)


class Creator(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    color: Optional[str] = None
    profile_picture: Optional[str] = None


class Option(BaseModel):
    id: Optional[str]

    name: Optional[str]

    color: Optional[str]

    order_index: Optional[int]


class TypeConfig(BaseModel):
    default: Optional[int]

    placeholder: Optional[str]

    new_drop_down: Optional[bool]

    options: Optional[List[Option]]

    include_guests: Optional[bool]

    include_team_members: Optional[bool]


class CustomItems:
    enabled: Optional[bool] = None


class DueDates(BaseModel):
    enabled: Optional[bool] = None

    start_date: Optional[bool] = None

    remap_due_dates: Optional[bool] = None

    remap_closed_due_date: Optional[bool] = None


class CustomField(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    type: Optional[str] = None

    type_config: Optional[TypeConfig] = None
    date_created: Optional[str] = None

    hide_from_guests: Optional[bool] = None

    value: Optional[Any] = None

    required: Optional[bool] = None


class TimeTracking(BaseModel):
    enabled: bool = False

    harvest: bool = False

    rollup: bool = False


class Sprints(BaseModel):
    enabled: bool = False


class Points(BaseModel):
    enabled: bool = False


class Zoom(BaseModel):
    enabled: bool = False


class Milestones(BaseModel):
    enabled: bool = False


class Emails(BaseModel):
    enabled: bool = False

class MultipleAssignees(BaseModel):
    enabled: bool = False


class TagsStatus(BaseModel):
    enabled: bool = False


class CustomFieldsStatus(BaseModel):
    enabled: bool = False


class DependencyWarning(BaseModel):
    enabled: bool = False


class TimeEstimateStatus(BaseModel):
    enabled: bool = False


class RemapDependenciesStatus(BaseModel):
    enabled: bool = False


class ChecklistsStatus(BaseModel):
    enabled: bool = False


class PortfoliosStatus(BaseModel):
    enabled: bool = False


class Features(BaseModel):
    due_dates: Optional[DueDates] = None

    multiple_assignees: Optional[MultipleAssignees] = None

    sprints: Optional[Sprints] = None

    start_date: bool = False

    remap_due_dates: bool = False

    remap_closed_due_date: bool = False

    time_tracking: Optional[TimeTracking]

    tags: Optional[TagsStatus]

    time_estimates: Optional[TimeEstimateStatus]

    checklists: Optional[ChecklistsStatus]

    custom_fields: Optional[CustomFieldsStatus]

    remap_dependencies: Optional[RemapDependenciesStatus]

    dependency_warning: Optional[DependencyWarning] = None

    portfolios: Optional[PortfoliosStatus]

    points: Optional[Points] = None

    custom_items: Optional[CustomItems] = None

    zoom: Optional[Zoom] = None

    milestones: Optional[Milestones] = None

    emails: Optional[Emails] = None

    class Config:
        validate_assignment = True

    @validator("time_tracking", pre=True, always=True)
    def set_tt(cls, time_tracking):
        return time_tracking or {"enabled": False}

    @validator("custom_fields", pre=True, always=True)
    def set_cf(cls, custom_fields):
        return custom_fields or {"enabled": False}

    @validator("tags", pre=True, always=True)
    def set_tags(cls, tags):
        return tags or {"enabled": False}

    @validator("multiple_assignees", pre=True, always=True)
    def set_ma(cls, multiple_assignees):
        return multiple_assignees or {"enabled": False}

    @validator("checklists", pre=True, always=True)
    def set_checklists(cls, checklists):
        return checklists or {"enabled": False}

    @validator("portfolios", pre=True, always=True)
    def set_portfolios(cls, portfolios):
        return portfolios or {"enabled": False}


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
    def all_features(self):
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


class Space(BaseModel):
    id: Optional[str] = None

    name: Optional[str] = None

    access: Optional[bool] = None

    features: Optional[Features]

    multiple_assignees: Optional[bool] = None

    private: Optional[bool] = False

    statuses: Optional[List[Status]] = None

    archived: Optional[bool] = None

    def build_space(self):
        return Space(**self)


class Spaces(BaseModel):
    spaces: Optional[List[Space]] = None

    def __iter__(self):
        return iter(self.spaces)

    def build_spaces(self):
        return Spaces(**self)


class Folder(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None

    orderindex: Optional[int] = None

    override_statuses: bool = False

    hidden: bool = False

    space: Optional[Space] = None

    task_count: Optional[int] = None

    lists: List[SingleList] = []

    def build_folder(self):
        return Folder(**self)

    def delete(self, client_instance):
        model = "folder/"

        deleted_folder_status = client_instance._delete_request(model, self.id)


class Folders(BaseModel):
    folders: Optional[List[Folder]] = None

    def build_folders(self):
        return Folders(**self)


class ClickupList(BaseModel):
    id: Optional[str] = None


# class Folder(BaseModel):

#     id: Optional[str] = None


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

    creator: Optional[Creator] = None

    assignees: Optional[List[Assignee]] = None

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

    space: Optional[Folder] = None
    url: Optional[str] = ""

    def build_task(self):
        return Task(**self)

    def delete(self, client_instance):
        client_instance.delete_task(self, self.id)

    def upload_attachment(self, client_instance, file_path: str):
        return client_instance.upload_attachment(self.id, file_path)

    def update(
        self,
        client_instance,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Any = None,
        time_estimate: Optional[int] = None,
        archived: Optional[bool] = None,
        add_assignees: Optional[List[str]] = None,
        remove_assignees: Optional[List[int]] = None,
    ):
        return client_instance.update_task(
            self.id,
            name,
            description,
            status,
            priority,
            time_estimate,
            archived,
            add_assignees,
            remove_assignees,
        )

    def add_comment(
        self,
        client_instance,
        comment_text: str,
        assignee: Optional[str] = None,
        notify_all: bool = True,
    ):
        return client_instance.create_task_comment(
            self.id, comment_text, assignee, notify_all
        )

    def get_comments(self, client_instance):
        return client_instance.get_task_comments(self.id)


class Tasks(BaseModel):
    tasks: Optional[List[Task]] = None

    def __iter__(self):
        return iter(self.tasks)

    def build_tasks(self):
        return Tasks(**self)


class InvitedBy(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    color: Optional[str] = None
    email: Optional[str] = None
    initials: Optional[str] = None
    profile_picture: None = None


class Member(BaseModel):
    user: User

    invited_by: Optional[InvitedBy] = None


class Members(BaseModel):
    members: Optional[List[User]] = None

    def __iter__(self):
        return iter(self.members)

    def build_members(self):
        return Members(**self)


class Team(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None

    avatar: Optional[str] = None

    members: Optional[List[Member]] = None


class Teams(BaseModel):
    teams: Optional[List[Team]] = None

    def __iter__(self):
        return iter(self.teams)

    def build_teams(self):
        return Teams(**self)


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

    key_results: Optional[List[Any]] = None
    percent_completed: Optional[int] = None

    history: Optional[List[Any]] = None

    pretty_url: Optional[str] = None

    def build_goal(self):
        return Goal(**self)


class Goals(BaseModel):
    goal: Goal

    def build_goals(self):
        built_goal = Goals(**self)

        return built_goal.goal


class GoalsList(BaseModel):
    goals: Optional[List[Goal]] = None
    folders: Optional[List[Folder]] = None

    def __iter__(self):
        return iter(self.goals)

    def build_goals(self):
        return GoalsList(**self)


class Tag(BaseModel):
    name: Optional[str] = None

    tag_fg: Optional[str] = None

    tag_bg: Optional[str] = None

    def build_tag(self):
        return Tag(**self)


class Tags(BaseModel):
    tags: Optional[List[Tag]] = None

    def __iter__(self):
        return iter(self.tags)

    def build_tags(self):
        return Tags(**self)


class Shared(BaseModel):
    tasks: Optional[List[Tasks]]

    lists: Optional[List[SingleList]]

    folders: Optional[List[Folder]]

    def build_shared(self):
        return Shared(**self)

    def __iter__(self):
        return iter(self.shared)


class SharedHierarchy(BaseModel):
    shared: Shared

    def build_shared(self):
        return SharedHierarchy(**self)

    def __iter__(self):
        return iter(self.shared)


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
    tags: Optional[List[Tag]] = None
    source: str = ""
    at: str = ""

    def build_data(self):
        return TimeTrackingData(**self)


class TimeTrackingDataList(BaseModel):
    data: Optional[List[TimeTrackingData]] = None

    def build_data(self):
        return TimeTrackingDataList(**self)

    def __iter__(self):
        return iter(self.data)


class TimeTrackingDataSingle(BaseModel):
    data: Optional[TimeTrackingData] = None

    def build_data(self):
        return TimeTrackingDataSingle(**self)

    def __iter__(self):
        return iter(self.data)
