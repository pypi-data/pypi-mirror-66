import os

import pytest

import yaml
from fa_common import create_app, start_app, utils, force_sync
from fa_common.gitlab import get_gitlab_client
from .conftest import get_env_file

dirname = os.path.dirname(__file__)
test_data_path = os.path.join(dirname, "data")

app = create_app(env_path=get_env_file())
force_sync(start_app)(app)
utils.current_app = app


@pytest.mark.asyncio
async def test_gitlab_create(ensure_no_test_gitlab):

    client = get_gitlab_client()

    project_id = await client.create_project("test_user")

    assert project_id > 0

    branch_name = await client.create_branch(project_id, "test_project")

    assert branch_name == "test_project"

    with open(os.path.join(dirname, test_data_path, "job.yaml"), "r") as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        job_file = yaml.safe_load(file)

    commit_id = await client.update_ci(project_id, branch_name, job_file, "Unit Test")
    assert commit_id
