# from loguru import logger as LOG

# from fastapi import APIRouter, Depends

# from app.preprocessing import model as preprocessing_model
# from app.shared.dto.message import Message
# from app.shared.utils import api_utils
# from app.inversion.job.dto import InversionJob
# from app.inversion.job import service
# from app.core.config import OAUTH2_SCHEME

# router = APIRouter()


# @router.post("/create/{project_id}", response_model=Message)
# async def create_inversion_job(
#     project_id: str, data: InversionJob, user_token: str = Depends(OAUTH2_SCHEME)
# ) -> Message:
#     """Create an inversion job"""
#     project_id = api_utils.cleanse_id(project_id)
#     job_id = api_utils.cleanse_id(data.jobId)

#     data.lines = (
#         data.lines
#         if data.lines is not None
#         else preprocessing_model.get_line_numbers(user_token, project_id).tolist()
#     )

#     params = data.params
#     columns = data.columns

#     # TODO Use DTO
#     service.create_job_summary(
#         user_token,
#         project_id,
#         job_id,
#         "RECEIVED",
#         algorithm=data.algorithm,
#         selection=data.lines,
#         init_start_time=True,
#         params=params,
#         columns=columns,
#     )
#     LOG.debug(f"Initialiing Inversion for {user_token} {project_id} {job_id}")
#     service.init_inversion_job(user_token, project_id, job_id, data)
#     # queue_task_id = gcp.send_queue_task(
#     #     PEND_JOB_QUEUE_NAME,
#     #     f"/inversion/job/task/init/{user_token}/{project_id}/{job_id}",
#     #     payload=payload,
#     # )

#     # service.update_job_summary(
#     #     user_token, project_id, job_id, queue_task_id=queue_task_id
#     # )

#     return Message(
#         message=f"""Job {job_id} has been successfully received """, returnValue=job_id
#     )


# @router.get("/delete/{project_id}/{job_id}", response_model=Message)
# async def delete_inversion_job(
#     project_id: str, job_id: str, user_token: str = Depends(OAUTH2_SCHEME)
# ) -> Message:
#     """Delete an inversion job"""
#     project_id = api_utils.cleanse_id(project_id)
#     job_id = api_utils.cleanse_id(job_id)

#     service.delete_job(user_token, project_id, job_id)

#     return Message(message=f"Job {job_id} has been scheduled for removal")
