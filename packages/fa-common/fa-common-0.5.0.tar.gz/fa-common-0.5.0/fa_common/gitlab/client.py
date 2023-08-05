
import time

from gitlab import Gitlab
from gitlab.v4.objects import Project

import yaml
from fa_common import force_async, get_current_app, get_settings
from fa_common import logger as LOG

# gl = gitlab.Gitlab("https://gitlab.com/", private_token="xsPGqL9yJFKVKFKz7b4A")

# project = gl.projects.create({"name": "test_user", "namespace_id": 7684130})

# print(project)


class GitlabClient:
    """
    Singleton client for interacting with gitlab.
    Is a wrapper over the existing gitlab python client to provide specialist functions for the Job/Module
    workflow.

    Please don't use it directly, use `fa_common.gitlab.utils.get_gitlab_client`.
    """

    __instance = None
    gitlab: Gitlab = None

    def __new__(cls) -> "GitlabClient":
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            app = get_current_app()
            cls.__instance.gitlab = app.gitlab  # type: ignore
        return cls.__instance

    async def _get_project(self, project_id: int) -> Project:
        return await force_async(self.gitlab.projects.get)(project_id)

    async def create_project(self, project_name: str) -> int:
        settings = get_settings()
        project = await force_async(self.gitlab.projects.create)(
            {"name": project_name, "namespace_id": settings.GITLAB_GROUP_ID}
        )
        LOG.info(f"Created project: {project}")

        data = {
            "branch": "master",
            "commit_message": "First Commit",
            "actions": [
                {"action": "create", "file_path": ".gitlab-ci.yml", "content": ""}
            ],
        }
        commit = await force_async(project.commits.create)(data)
        LOG.info(f"Created commit: {commit}")

        return project.id

    async def create_branch(self, project_id: int, branch_name: str):
        project = await self._get_project(project_id)
        branch = await force_async(project.branches.create)(
            {"branch": branch_name, "ref": "master"}
        )
        LOG.info(f"Created branch: {branch}")
        return branch_name

    async def update_ci(
        self,
        project_id: int,
        branch_name: str,
        ci_file: dict,
        update_message: str = "No message",
    ):
        project = await self._get_project(project_id)
        data = {
            "branch": branch_name,
            "commit_message": update_message,
            "actions": [
                {
                    "action": "update",
                    "file_path": ".gitlab-ci.yml",
                    "content": yaml.dump(ci_file),
                }
            ],
        }
        commit = await force_async(project.commits.create)(data)
        LOG.info(f"Created CI Commit: {commit}")
        return commit.id

    async def delete_project(self, project_id: int):
        await force_async(self.gitlab.projects.delete)(project_id)

    async def delete_project_by_name(self, project_name: str, wait: bool = True):
        settings = get_settings()
        projects = await force_async(self.gitlab.projects.list)(
            search=project_name, owned=True
        )
        LOG.info(f"Found projects: {projects}")
        for proj in projects:
            group_id = proj.namespace["id"]
            LOG.info(f"Checking project: {proj.id}, {proj.name}, {group_id}")
            if (
                proj.name == project_name and group_id == settings.GITLAB_GROUP_ID
            ):
                LOG.info(f"Deleting project: {proj.id}")
                project_id = proj.id
                await force_async(proj.delete)()
                if wait:
                    while proj is not None:
                        LOG.info(f"Waiting for project to delete")
                        time.sleep(2)
                        proj = await self._get_project(project_id)

                return
        raise ValueError(f"No project found with the name {project_name}")
