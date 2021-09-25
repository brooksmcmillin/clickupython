# tests/tests_clickup.py
from unittest import mock
from clickupy.models import (
    AllLists,
    AssignedBy,
    Asssignee,
    Comment,
    Folders,
    Goal,
    SingleList,
    Task,
    Tasks,
)
import pytest

from clickupy import client
from clickupy import models
import os
import sys
from clickupy import exceptions

API_KEY = "pk_6341704_8OV9MRRLXIK2VO3XV3FNKKLY9IMQAXB3"
MOCK_API_URL = "https://private-anon-3a942619a6-clickup20.apiary-mock.com/api/v2/"


class TestHTTPMethods:
    @pytest.mark.http
    def test__get_request(self):
        c = client.ClickUpClient(API_KEY)

        with pytest.raises(exceptions.ClickupClientError):
            c._ClickUpClient__get_request("badmodel")

    @pytest.mark.http
    def test__post_request(self):
        c = client.ClickUpClient(API_KEY)

        with pytest.raises(exceptions.ClickupClientError):
            c._ClickUpClient__post_request("badmodel", "baddata")

    @pytest.mark.http
    def test__put_request(self):
        c = client.ClickUpClient(API_KEY)

        with pytest.raises(exceptions.ClickupClientError):
            c._ClickUpClient__put_request("badmodel", "baddata")

    @pytest.mark.http
    def test__delete_request(self):
        c = client.ClickUpClient(API_KEY)

        c._ClickUpClient__headers_request("badmodel")

    @pytest.mark.http
    def test___headers(self):
        c = client.ClickUpClient("API_KEY")

        headers = c._ClickUpClient__headers(file_upload=False)
        assert headers == {
            "Authorization": "API_KEY",
            "Content-Type": "application/json",
        }


class TestClientLists:
    @pytest.mark.lists
    def test_get_list(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_list("132237389")
        assert type(result) == SingleList
        assert result.id == "132237389"

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    def test_get_lists(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_lists("456")

        assert isinstance(result, models.AllLists)

    # Work on this test
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    def test_create_list(self):

        c = client.ClickUpClient(API_KEY)
        result = c.create_list(
            "456", "New List Name", "New List Content", "1567780450202", 2361428, "red"
        )

        assert result.id == "124"
        assert result.assignee.id == "183"
        assert result.folder.id == "456"
        assert result.space.id == "789"
        assert len(result.statuses) > 0
        assert result.statuses[0].status == "to do"

        assert isinstance(result, models.SingleList)


class TestClientFolders:
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.folders
    def test_get_folder(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_folder("457")
        assert result.id == "457"
        assert result.name == "Updated Folder Name"
        assert result.task_count == 0
        assert isinstance(result, models.Folder)

    @pytest.mark.folders
    def test_get_folders(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_folders("30094063")

        assert result.folders[0].id == "78070294"
        assert isinstance(result, models.Folders)

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.folders
    def test_create_folder(self):

        c = client.ClickUpClient(API_KEY)
        result = c.create_folder("789", "New Folder Name")

        assert result.id == "457"
        assert result.name == "New Folder Name"
        assert result.hidden == False
        assert result.space.id == 789
        assert result.task_count == 0
        assert isinstance(result, models.Folder)

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.folders
    def test_update_folder(self):

        c = client.ClickUpClient(API_KEY)
        result = c.update_folder("457", "Updated Folder Name")

        assert result.id == "457"
        assert result.name == "Updated Folder Name"
        assert result.hidden == False
        assert result.space.id == 789
        assert result.task_count == 0
        assert isinstance(result, models.Folder)

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.folders
    def test_delete_folder(self):

        c = client.ClickUpClient(API_KEY)
        result = c.delete_folder("457")

        assert result


class TestClientTasks:
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.tasks
    def test_upload_attachment(self):

        c = client.ClickUpClient(API_KEY)
        result = c.upload_attachment("9hv", r"tests/assets/test-image.png")

        assert result.id == "ac434d4e-8b1c-4571-951b-866b6d9f2ee6.png"
        assert result.version == 0
        assert result.date == "1569988578766"
        assert type(result) == models.Attachment
        assert result.title == "image.png"
        assert result.extension == "png"
        assert (
            result.thumbnail_small
            == "https://attachments-public.clickup.com/ac434d4e-8b1c-4571-951b-866b6d9f2ee6/logo_small.png"
        )
        assert (
            result.thumbnail_large
            == "https://attachments-public.clickup.com/ac434d4e-8b1c-4571-951b-866b6d9f2ee6/logo_small.png"
        )
        assert (
            result.url
            == "https://attachments-public.clickup.com/ac434d4e-8b1c-4571-951b-866b6d9f2ee6/logo_small.png"
        )

    @pytest.mark.tasks
    def test_create_task(self):

        c = client.ClickUpClient(API_KEY)
        result = c.create_task("138166377", "New Task Name", "New Task Description")

        assert isinstance(result, models.Task)

        with pytest.raises(exceptions.ClickupClientError):
            t = c.create_task("Not a real task id", "New Task Name")

        with pytest.raises(exceptions.ClickupClientError):
            t = c.create_task("138166377", "New Task Name", priority=6)

    @pytest.mark.tasks
    def test_get_tasks(self):

        c = client.ClickUpClient(API_KEY)
        result = c.get_tasks("138166377")
        assert isinstance(result, models.Tasks)

    @pytest.mark.tasks
    def test_update_task(self):

        description = "Updated Task description"

        c = client.ClickUpClient(API_KEY)
        result = c.update_task("1hpx6uk", description=description)
        assert type(result) == models.Task
        assert result.description == description


class TestClientComments:
    @pytest.mark.comments
    def test_get_task_comments(self):
        c = client.ClickUpClient(API_KEY)
        result = c.get_task_comments("1hpx6uk")

        for c in result:
            assert c.user.id == "6341704"


class TestClientChecklists:
    @pytest.mark.checklists
    def test_update_checklist(self):
        c = client.ClickUpClient(API_KEY)
        result = c.create_checklist("1gu4f5g", "Test Checklist")
        assert isinstance(result, models.Checklist)
        result2 = c.update_checklist(result.id, name="Updated Checklist Title")
        assert result2.name == "Updated Checklist Title"

    @pytest.mark.checklists
    def test_delete_checklist(self):
        c = client.ClickUpClient(API_KEY)
        result = c.create_checklist("1gu4f5g", "Test Checklist")
        assert isinstance(result, models.Checklist)
        assert c.delete_checklist(result.id)

    @pytest.mark.checklists
    def test_delete_checklist_item(self):
        c = client.ClickUpClient(API_KEY)
        result = c.create_checklist("1gu4f5g", "Test Checklist")
        checklist_with_item = c.create_checklist_item(result.id, "Test Checklist item")

        assert isinstance(checklist_with_item, models.Checklist)

        assert c.delete_checklist_item(
            checklist_with_item.id, checklist_with_item.items[0].id
        )

    @pytest.mark.checklists
    def test_update_checklist_item(self):
        c = client.ClickUpClient(API_KEY)
        result = c.create_checklist("1gu4f5g", "Test Checklist")
        checklist_with_item = c.create_checklist_item(result.id, "Test Checklist item")

        assert isinstance(checklist_with_item, models.Checklist)

        result2 = c.update_checklist_item(
            checklist_with_item.id, checklist_with_item.items[0].id, name="it worked"
        )

        assert result2.items[0].name == "it worked"


class TestClientMembers:
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.members
    def test_get_task_members(self):
        c = client.ClickUpClient("apikey")
        result = c.get_task_members("12345")

        assert isinstance(result, models.Members)
        assert result.members[0].id == "812"
        assert result.members[0].username == "John Doe"

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.members
    def test_get_list_members(self):
        c = client.ClickUpClient("apikey")
        result = c.get_list_members("12345")

        assert isinstance(result, models.Members)
        assert result.members[0].id == "812"
        assert result.members[0].username == "John Doe"


class TestClientGoals:
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.goals
    def test_create_goal(self):
        c = client.ClickUpClient("apikey")
        result = c.create_goal("12345", "name")

        assert isinstance(result, models.Goal)
        assert result.id == "e53a033c-900e-462d-a849-4a216b06d930"
        assert result.owners[0].id == "183"
        assert result.pretty_url == "https://app.clickup.com/512/goals/6"

    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.goals
    def test_update_goal(self):
        c = client.ClickUpClient("apikey")
        result = c.update_goal("12345")

        assert isinstance(result, models.Goal)
        assert result.id == "e53a033c-900e-462d-a849-4a216b06d930"
        assert result.owners[0].id == "182"
        assert result.pretty_url == "https://app.clickup.com/512/goals/6"


class TestSharedHierarchy:
    @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    @pytest.mark.shared
    def test_get_shared_hierarchy(self):
        c = client.ClickUpClient("apikey")
        result = c.get_shared_hierarchy("333")
        assert isinstance(result, models.SharedHierarchy)
        assert result.shared.lists[0].id == "1421"
        assert result.shared.folders[0].id == "1058"

    # class TestTimeTracking:
    #     @mock.patch("clickupy.client.API_URL", MOCK_API_URL)
    #     @pytest.mark.timetracking
    #     def test_get_time_entries_in_range(self):
    #         c = client.ClickUpClient("apikey")
    #         result = c.get_time_entries_in_range("333")
    #         assert isinstance(result, models.TimeTrackingDataList)
    #         assert result.data[0].id == "1963465985517105840"
    #         assert result.data[0].task.id == "1vwwavv"
    #         assert result.data[0].wid == "300702"
    #         assert result.data[0].user.username == "first_name last_name" @ mock.patch(
    #             "clickupy.client.API_URL", MOCK_API_URL
    #         )

    @pytest.mark.timetracking
    def test_get_single_time_entry(self):
        c = client.ClickUpClient("pk_6341704_8OV9MRRLXIK2VO3XV3FNKKLY9IMQAXB3")
        result = c.get_single_time_entry("18027888", "2626816009272585830")
        assert isinstance(result, models.TimeTrackingDataSingle)
        assert result.data.id == "2626816009272585830"
