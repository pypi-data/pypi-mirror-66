# import os
# import json
# import datetime
# import requests
# from loguru import logger as LOG

# from google.cloud import firestore
# from google.cloud import storage

# from typing import Dict, Optional

# from app.shared.dto import FileMetadata
# from app.core.config import INVERSION_SERIVCE, BUCKET_NAME
# from app.inversion.job.dto import InversionJob, InversionParameters, InversionRunner
# from app.project import service as project
# from app.project import model as project_table
# from app.inversion.result import service as inversion_result
# from app.inversion import galei


# def upload_job_file_from_path(
#     user_id: str, project_id: str, inv_job_id: str, inv_file: str, inv_file_id: str
# ) -> FileMetadata:
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(BUCKET_NAME)
#     path = f"users/{user_id}/{project_id}/jobs/{inv_job_id}/{inv_file_id}"
#     blob = bucket.blob(path)
#     blob.upload_from_filename(inv_file)

#     inversion_file = bucket.get_blob(path)

#     assert (
#         inversion_file is not None
#     ), f"There is no file {path} uploaded to the bucket, please upload the data prior to calling this api"

#     blob_metadata = FileMetadata(
#         fileSize=inversion_file.size, fileName=inversion_file.name
#     )

#     return blob_metadata


# def delete_job_data(user_id: str, project_id: str, inv_job_id: str) -> str:
#     storage_client = storage.Client()
#     bucket = storage_client.get_bucket(BUCKET_NAME)
#     path = f"users/{user_id}/{project_id}/jobs/{inv_job_id}"

#     blobs = bucket.list_blobs(prefix=path, delimiter=None)

#     # Delete all blobs under the path
#     for blob in blobs:
#         blob.delete()

#     inversion_file = bucket.get_blob(path)

#     assert (
#         inversion_file is None
#     ), "There are files still contained in the bucket {}".format(path)

#     return path


# def create_job_summary(
#     user_id: str, project_id: str, job_id: str, status: str, *args, **kwargs
# ):
#     algorithm = kwargs.get("algorithm", "galei")
#     selection = kwargs.get("selection", None)
#     size = kwargs.get("size", -1)
#     input_file_uri = kwargs.get("input_file_uri", None)
#     output_file_uri = kwargs.get("output_file_uri", None)
#     sample_count = kwargs.get("sample_count", None)
#     percentage_complete = kwargs.get("percentage_complete", 0)
#     est_time_complete = kwargs.get("est_time_complete", None)
#     start_time = kwargs.get("start_time", None)
#     console_log = kwargs.get("console_log", None)
#     task_id = kwargs.get("task_id", None)
#     queue_task_id = kwargs.get("queue_task_id", None)
#     init_start_time = kwargs.get("init_start_time", None)
#     params = kwargs.get("params", None)
#     columns = kwargs.get("columns", None)

#     if init_start_time:
#         start_time = datetime.datetime.now().isoformat()

#     json = {
#         "jobId": job_id,
#         "status": status,
#         "algorithm": algorithm,
#         "selection": selection,
#         "size": size,
#         "input_file_uri": input_file_uri,
#         "output_file_uri": output_file_uri,
#         "sample_count": sample_count,
#         "percentage_complete": percentage_complete,
#         "est_time_complete": est_time_complete,
#         "start_time": start_time,
#         "console_log": console_log,
#         "task_id": task_id,
#         "queue_task_id": queue_task_id,
#         "params": params,
#         "columns": columns,
#     }

#     fs_client = firestore.Client()
#     doc_ref = (
#         fs_client.collection("users")
#         .document(user_id)
#         .collection("projects")
#         .document(project_id)
#         .collection("jobs")
#         .document(job_id)
#     )
#     doc_ref.set(json)
#     return json


# def update_job_summary(user_id: str, project_id: str, job_id: str, **kwargs):

#     doc_dict = {}

#     status = kwargs.get("status", None)
#     if status is not None:
#         doc_dict["status"] = status

#     init_start_time = kwargs.get("init_start_time", None)

#     algorithm = kwargs.get("algorithm", None)
#     if algorithm is not None:
#         doc_dict["algorithm"] = algorithm

#     selection = kwargs.get("selection", None)
#     if selection is not None:
#         doc_dict["selection"] = selection

#     size = kwargs.get("size", None)
#     if size is not None:
#         doc_dict["size"] = size

#     input_file_uri = kwargs.get("input_file_uri", None)
#     if input_file_uri is not None:
#         doc_dict["input_file_uri"] = input_file_uri

#     output_file_uri = kwargs.get("output_file_uri", None)
#     if output_file_uri is not None:
#         doc_dict["output_file_uri"] = output_file_uri

#     sample_count = kwargs.get("sample_count", None)
#     if sample_count is not None:
#         doc_dict["sample_count"] = sample_count

#     percentage_complete = kwargs.get("percentage_complete", None)
#     if percentage_complete is not None:
#         doc_dict["percentage_complete"] = percentage_complete

#     est_time_complete = kwargs.get("est_time_complete", None)
#     if est_time_complete is not None:
#         doc_dict["est_time_complete"] = est_time_complete

#     start_time = kwargs.get("start_time", None)
#     if start_time is not None:
#         doc_dict["start_time"] = start_time

#     console_log = kwargs.get("console_log", None)
#     if console_log is not None:
#         doc_dict["console_log"] = console_log

#     task_id = kwargs.get("task_id", None)
#     if task_id is not None:
#         doc_dict["task_id"] = task_id

#     queue_task_id = kwargs.get("queue_task_id", None)
#     if queue_task_id is not None:
#         doc_dict["queue_task_id"] = queue_task_id

#     params = kwargs.get("params", None)
#     if params is not None:
#         doc_dict["params"] = params

#     columns = kwargs.get("columns", None)
#     if columns is not None:
#         doc_dict["columns"] = columns

#     init_start_time = kwargs.get("init_start_time", None)

#     if init_start_time == True:
#         doc_dict["submit_time"] = datetime.datetime.now().isoformat()

#     doc_ref = read_job_summary(user_id, project_id, job_id)

#     doc_ref.update(doc_dict)
#     return job_id


# def read_job_summary(user_id: str, project_id: str, job_id: str):

#     fs_client = firestore.Client()
#     doc_ref = (
#         fs_client.collection("users")
#         .document(user_id)
#         .collection("projects")
#         .document(project_id)
#         .collection("jobs")
#         .document(job_id)
#     )
#     doc_ref

#     return doc_ref


# async def delete_job(user_id: str, project_id: str, job_id: str):

#     job_ref = read_job_summary(user_id, project_id, job_id)
#     job_data = job_ref.get().to_dict()
#     job_ref.delete()

#     try:
#         inversion_result.delete_inversion(job_id)
#     except Exception as exc:
#         # Service might be down, still need to delete the job data.
#         LOG.warning(
#             "Error deleting job from the inversion service, continuing with job data delete"
#         )

#     delete_job_data(user_id, project_id, job_id)

#     return True


# def map_columns(columns: list, data_definition: dict) -> Dict[str, int]:
#     column_offsets: Dict[str, int] = {}

#     # get the width on any multi-column data
#     for column in data_definition:
#         value = data_definition.get(column)
#         if isinstance(value, list):
#             column_offsets[column] = len(value)

#     column_mapping: Dict[str, int] = {}
#     column_value: int = 1

#     # generate column mapping accounting for any multi-column data and including exported error columns
#     for column_name in columns:
#         if column_name in column_offsets:
#             column_mapping[column_name] = column_value
#             column_offset: Optional[int] = column_offsets.get(column_name)
#             assert column_offset is not None
#             column_offset_int: int = column_offset
#             column_value += column_offset_int
#             column_mapping[f"{column_name}_Error"] = column_value
#             column_value += column_offset_int
#         else:
#             column_mapping[column_name] = column_value
#             column_value += 1

#     return column_mapping


# # @router.post("/task/init/{user_token}/{project_id}/{job_id}", response_model=Message)
# async def init_inversion_job(
#     user_token: str, project_id: str, job_id: str, data: InversionJob
# ) -> None:
#     """Private api call that initialises a job"""

#     params: InversionParameters = data.params

#     project_session = project.get_project_session(user_token, project_id)

#     job_data = read_job_summary(user_token, project_id, job_id).get().to_dict()

#     current_status = job_data["status"]

#     if current_status != "RECEIVED":
#         LOG.info(
#             f"Job {job_id} is in status {current_status} and does not need to be pended"
#         )

#     # if no columns are provided in the request, grab the defaults from the session
#     columns = data.columns
#     if columns is None:
#         columns = project_session["export_for_inversion"]

#     data_definition = project_session["data_definition"]

#     column_mapping = map_columns(columns, data_definition)

#     export_path = project_table.export_data(
#         user_token, project_id, columns, export_file="job_export.csv", lines=data.lines
#     )

#     job_file_bundle = galei.create_job_bundle(
#         job_id, export_path, params, column_mapping
#     )

#     storage_summary = upload_job_file_from_path(
#         user_token,
#         project_id,
#         job_id,
#         job_file_bundle["bundle_path"],
#         job_file_bundle["bundle_name"],
#     )

#     # cleanup the zip file
#     os.remove(job_file_bundle["bundle_path"])

#     update_job_summary(
#         user_token,
#         project_id,
#         job_id,
#         status="PENDING",
#         size=storage_summary["size"],
#         input_file_uri=storage_summary["uri"],
#         sample_count=job_file_bundle["sample_count"],
#     )

#     payload = {"userId": user_token, "projectId": project_id, "jobId": job_id}
#     if data.runner == InversionRunner.PEARCEY:
#         try:
#             payload["nexusUser"] = data.runnerUser
#             payload["nexusPassword"] = data.runnerPassword
#             payload["cpus"] = data.runnerCPUs
#             payload["timeMinutes"] = data.runnerAllocationMins
#         except Exception as exc:
#             LOG.error(
#                 "There was an error in job: {} setting the variables for a pearcey inversion. Error: {}".format(
#                     job_id, exc
#                 )
#             )
#             return
#         payload["runner"] = "pearcey"

#     # queue_task_id = gcp.send_queue_task(
#     #     SEND_JOB_QUEUE_NAME,
#     #     "/inversion/job/task/send/{}/{}/{}".format(user_token, project_id, job_id),
#     #     payload=payload,
#     # )
#     send_inversion(user_token, project_id, job_id, payload)

#     # update_job_summary(
#     #     user_token, project_id, job_id, queue_task_id=queue_task_id
#     # )
#     LOG.info(f"Job {user_token} has been successfully pended.")


# # @api.route("/task/send/{user_token}/{project_id}/{job_id}", response_model=Message)
# async def send_inversion(user_token: str, project_id: str, job_id: str, payload: dict):
#     """Private api call sends an inversion start request to the inversion runner"""

#     latest_job = read_job_summary(user_token, project_id, job_id)
#     current_status = latest_job.get().to_dict()["status"]
#     if current_status != "PENDING":
#         LOG.info(
#             f"Job {job_id} is in status {current_status} and does not need to be sent"
#         )

#     try:
#         url = INVERSION_SERIVCE + "/inversion"

#         if "runner" in payload and payload["runner"].lower() == "pearcey":
#             url = INVERSION_SERIVCE + "/inversion/pearcey"

#         r = requests.post(url, json=json.dumps(payload))
#         assert r.status_code == 200, "Failed to send inversion job: {}".format(r.text)
#     except Exception as exc:
#         LOG.error("Call to Inversion Runner failed: {}".format(exc))
#         return
#     LOG.info(f"Job {job_id} sent to inversion runner")
