"""Workflow Engine API endpoints."""
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user, get_db
from app.core.logging import get_logger
from app.models.workflow import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
    AutomationAnalysisResponse,
    CareerCaseResponse,
    CompanyProfileCreate,
    CompanyProfileResponse,
    DashboardMetrics,
    DashboardResponse,
    KanbanBoardResponse,
    MorningBriefResponse,
    NoteCreate,
    NoteResponse,
    NotificationResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TimelineEventCreate,
    TimelineEventResponse,
    UserActivityData,
    WorkflowTriggerRequest,
    WorkflowTriggerResponse,
)
from app.repositories.workflow import WorkflowRepository
from app.services.smart_automation import smart_automation_service
from app.services.workflow_engine import workflow_engine
from app.db.models.user import User

logger = get_logger(__name__)

router = APIRouter(prefix="/workflow", tags=["workflow"])


async def validate_uuid(uuid_str: str, field_name: str) -> UUID:
    """Validate and convert string to UUID."""
    try:
        return UUID(uuid_str)
    except (ValueError, AttributeError) as e:
        logger.error(f"Invalid {field_name} format: {uuid_str}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid {field_name} format. Must be a valid UUID.",
        ) from e


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApplicationResponse:
    """Create a new application."""
    try:
        repo = WorkflowRepository(db)

        # Validate UUIDs
        await validate_uuid(str(application_data.resume_id), "resume_id")
        if application_data.job_id:
            await validate_uuid(str(application_data.job_id), "job_id")
        if application_data.company_id:
            await validate_uuid(str(application_data.company_id), "company_id")

        # Create company profile if needed
        company_id = application_data.company_id
        if not company_id:
            pass

        application = await repo.create_application(
            user_id=str(current_user.id),
            resume_id=str(application_data.resume_id),
            job_id=str(application_data.job_id) if application_data.job_id else None,
            company_id=str(company_id) if company_id else None,
            status=application_data.status,
            priority=application_data.priority,
            probability=application_data.probability,
            notes=application_data.notes,
            metadata=application_data.metadata,
        )

        # Trigger workflow (non-critical, don't fail if this errors)
        try:
            await workflow_engine.trigger_workflow(
                "application_created",
                {
                    "application_id": str(application.id),
                    "user_id": str(current_user.id),
                    "resume_id": str(application_data.resume_id),
                    "job_id": str(application_data.job_id),
                },
            )
        except Exception as e:
            logger.warning(f"Workflow trigger failed for application {application.id}: {e}")

        # Log activity (non-critical, don't fail if this errors)
        try:
            await repo.log_activity(
                user_id=str(current_user.id),
                action="create_application",
                entity_type="application",
                entity_id=str(application.id),
                application_id=str(application.id),
            )
        except Exception as e:
            logger.warning(f"Activity logging failed for application {application.id}: {e}")

        # Store to Lemma structured datastore (optional, non-blocking)
        try:
            from app.ai.lemma_client import lemma_client
            if lemma_client.is_enabled():
                await lemma_client.store_job_application({
                    "user_id":      str(current_user.id),
                    "status":       application_data.status,
                    "notes":        application_data.notes or "",
                    "applied_date": application.created_at.isoformat() if application.created_at else "",
                })
        except Exception:
            pass  # Lemma is optional

        return ApplicationResponse.model_validate(application)
    except SQLAlchemyError as e:
        logger.error(f"Database error creating application: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create application due to database error.",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error creating application: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the application.",
        ) from e


@router.patch("/applications/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: UUID,
    application_data: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApplicationResponse:
    """Update an application."""
    try:
        repo = WorkflowRepository(db)

        application = await repo.get_application(str(application_id))
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        if application.user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this application",
            )

        # Update status if provided
        if application_data.status and application_data.status != application.status:
            application = await repo.update_application_status(
                str(application_id),
                application_data.status,
                reason="User update",
                changed_by="user",
            )

        # Update other fields
        if application_data.priority:
            application.priority = application_data.priority
        if application_data.probability:
            application.probability = application_data.probability
        if application_data.notes is not None:
            application.notes = application_data.notes
        if application_data.metadata is not None:
            application.metadata = application_data.metadata

        await db.commit()
        await db.refresh(application)

        # Log activity (non-critical)
        try:
            await repo.log_activity(
                user_id=str(current_user.id),
                action="update_application",
                entity_type="application",
                entity_id=str(application_id),
                application_id=str(application_id),
            )
        except Exception as e:
            logger.warning(f"Activity logging failed for application {application_id}: {e}")

        return ApplicationResponse.model_validate(application)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error updating application {application_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update application due to database error.",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error updating application {application_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the application.",
        ) from e


@router.get("/applications", response_model=list[ApplicationResponse])
async def get_applications(
    status_filter: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[ApplicationResponse]:
    """Get all applications for the current user."""
    try:
        repo = WorkflowRepository(db)
        applications = await repo.get_applications(
            user_id=str(current_user.id),
            status=status_filter,
        )
        return [ApplicationResponse.model_validate(app) for app in applications]
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching applications: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch applications due to database error.",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error fetching applications: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching applications.",
        ) from e


@router.get("/applications/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApplicationResponse:
    """Get a specific application."""
    try:
        repo = WorkflowRepository(db)
        application = await repo.get_application(str(application_id))

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        if application.user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this application",
            )

        return ApplicationResponse.model_validate(application)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching application {application_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch application due to database error.",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error fetching application {application_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the application.",
        ) from e


@router.post("/applications/{application_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    application_id: UUID,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TaskResponse:
    """Create a task for an application."""
    try:
        repo = WorkflowRepository(db)

        application = await repo.get_application(str(application_id))
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        if application.user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create tasks for this application",
            )

        task = await repo.create_application_task(
            application_id=str(application_id),
            user_id=str(current_user.id),
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.due_date,
            priority=task_data.priority,
            task_type=task_data.task_type,
        )

        return TaskResponse.model_validate(task)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error creating task: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task due to database error.",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error creating task: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the task.",
        ) from e


@router.get("/tasks", response_model=list[TaskResponse])
async def get_tasks(
    application_id: UUID | None = None,
    status_filter: str | None = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[TaskResponse]:
    """Get tasks for the current user."""
    repo = WorkflowRepository(db)
    tasks = await repo.get_tasks(
        user_id=str(current_user.id),
        application_id=str(application_id) if application_id else None,
        status=status_filter,
    )
    return [TaskResponse.model_validate(task) for task in tasks]


@router.post("/applications/{application_id}/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    application_id: UUID,
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NoteResponse:
    """Create a note for an application."""
    repo = WorkflowRepository(db)

    application = await repo.get_application(str(application_id))
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create notes for this application",
        )

    note = await repo.create_application_note(
        application_id=str(application_id),
        user_id=str(current_user.id),
        content=note_data.content,
        note_type=note_data.note_type,
    )

    return NoteResponse.model_validate(note)


@router.post("/applications/{application_id}/timeline", response_model=TimelineEventResponse, status_code=status.HTTP_201_CREATED)
async def create_timeline_event(
    application_id: UUID,
    event_data: TimelineEventCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TimelineEventResponse:
    """Create a timeline event for an application."""
    repo = WorkflowRepository(db)

    application = await repo.get_application(str(application_id))
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create timeline events for this application",
        )

    event = await repo.create_timeline_event(
        application_id=str(application_id),
        event_type=event_data.event_type,
        title=event_data.title,
        description=event_data.description,
        event_date=event_data.event_date,
        metadata=event_data.extra_metadata,
    )

    return TimelineEventResponse.model_validate(event)


@router.get("/applications/{application_id}/timeline", response_model=list[TimelineEventResponse])
async def get_timeline_events(
    application_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[TimelineEventResponse]:
    """Get timeline events for an application."""
    repo = WorkflowRepository(db)

    application = await repo.get_application(str(application_id))
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    if application.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this application",
        )

    events = await repo.get_timeline_events(str(application_id))
    return [TimelineEventResponse.model_validate(event) for event in events]


@router.get("/notifications", response_model=list[NotificationResponse])
async def get_notifications(
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[NotificationResponse]:
    """Get notifications for the current user."""
    repo = WorkflowRepository(db)
    notifications = await repo.get_notifications(
        user_id=str(current_user.id),
        unread_only=unread_only,
    )
    return [NotificationResponse.model_validate(notif) for notif in notifications]


@router.patch("/notifications/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> NotificationResponse:
    """Mark a notification as read."""
    repo = WorkflowRepository(db)
    notification = await repo.mark_notification_read(str(notification_id))

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    if notification.user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this notification",
        )

    return NotificationResponse.model_validate(notification)


@router.post("/companies", response_model=CompanyProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_company_profile(
    company_data: CompanyProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CompanyProfileResponse:
    """Create a company profile."""
    repo = WorkflowRepository(db)
    company = await repo.create_company_profile(
        user_id=str(current_user.id),
        name=company_data.name,
        website=company_data.website,
        industry=company_data.industry,
        size=company_data.size,
        location=company_data.location,
        description=company_data.description,
    )
    return CompanyProfileResponse.model_validate(company)


@router.get("/companies", response_model=list[CompanyProfileResponse])
async def get_company_profiles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[CompanyProfileResponse]:
    """Get company profiles for the current user."""
    repo = WorkflowRepository(db)
    companies = await repo.get_company_profiles(str(current_user.id))
    return [CompanyProfileResponse.model_validate(company) for company in companies]


@router.post("/workflow/trigger", response_model=WorkflowTriggerResponse)
async def trigger_workflow(
    workflow_data: WorkflowTriggerRequest,
    current_user: User = Depends(get_current_user),
) -> WorkflowTriggerResponse:
    """Trigger a workflow based on an event."""
    result = await workflow_engine.trigger_workflow(
        workflow_data.event_type,
        workflow_data.context,
    )
    return WorkflowTriggerResponse(**result)


@router.post("/automation/analyze", response_model=AutomationAnalysisResponse)
async def analyze_automation(
    user_data: UserActivityData,
    current_user: User = Depends(get_current_user),
) -> AutomationAnalysisResponse:
    """Analyze user activity and generate recommendations."""
    result = await smart_automation_service.analyze_user_activity(user_data.model_dump())
    return AutomationAnalysisResponse(**result)


@router.get("/dashboard/morning-brief", response_model=MorningBriefResponse)
async def get_morning_brief(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MorningBriefResponse:
    """Get morning brief for the current user."""
    repo = WorkflowRepository(db)

    # Gather user data
    tasks = await repo.get_tasks(user_id=str(current_user.id), status="pending")
    notifications = await repo.get_notifications(user_id=str(current_user.id), unread_only=True)
    activity_feed = await repo.get_activity_feed(user_id=str(current_user.id), limit=10)

    user_data = {
        "tasks": [TaskResponse.model_validate(t).model_dump() for t in tasks],
        "notifications": [NotificationResponse.model_validate(n).model_dump() for n in notifications],
        "interviews": [],  # Would come from interview repository
        "career_health": {},  # Would come from career repository
    }

    brief = await smart_automation_service.generate_morning_brief(user_data)
    return MorningBriefResponse(**brief)


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DashboardResponse:
    """Get dashboard data for the current user."""
    try:
        repo = WorkflowRepository(db)

        # Get applications
        applications = await repo.get_applications(user_id=str(current_user.id))

        # Calculate metrics
        applications_by_stage = {}
        for app in applications:
            stage = app.status
            applications_by_stage[stage] = applications_by_stage.get(stage, 0) + 1

        # Get tasks
        pending_tasks = await repo.get_tasks(user_id=str(current_user.id), status="pending")

        # Get notifications
        unread_notifications = await repo.get_notifications(user_id=str(current_user.id), unread_only=True)

        # Get activity feed
        recent_activity = await repo.get_activity_feed(user_id=str(current_user.id), limit=10)

        # Get morning brief (non-critical)
        morning_brief_result = None
        try:
            morning_brief_result = await get_morning_brief(current_user, db)
        except Exception as e:
            logger.warning(f"Failed to generate morning brief: {e}")

        # Top recommendations (would come from automation analysis)
        top_recommendations = []

        return DashboardResponse(
            metrics=DashboardMetrics(
                total_applications=len(applications),
                applications_by_stage=applications_by_stage,
                pending_tasks=len(pending_tasks),
                upcoming_interviews=0,
                unread_notifications=len(unread_notifications),
                weekly_progress={},
                response_rate=0.0,
                interview_rate=0.0,
                offer_rate=0.0,
            ),
            morning_brief=morning_brief_result if morning_brief_result else None,
            recent_activity=[{
                "action": a.action,
                "entity_type": a.entity_type,
                "created_at": str(a.created_at),
            } for a in recent_activity],
            top_recommendations=top_recommendations,
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching dashboard: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch dashboard due to database error.",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error fetching dashboard: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching dashboard.",
        ) from e


@router.get("/kanban", response_model=KanbanBoardResponse)
async def get_kanban_board(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> KanbanBoardResponse:
    """Get kanban board data for the current user."""
    try:
        repo = WorkflowRepository(db)
        applications = await repo.get_applications(user_id=str(current_user.id))

        # Define columns
        columns = [
            {"id": "wishlist", "title": "Wishlist", "status": "wishlist"},
            {"id": "preparing", "title": "Preparing", "status": "preparing"},
            {"id": "applied", "title": "Applied", "status": "applied"},
            {"id": "oa_received", "title": "OA Received", "status": "oa_received"},
            {"id": "interview", "title": "Interview", "status": "interview"},
            {"id": "offer", "title": "Offer", "status": "offer"},
            {"id": "rejected", "title": "Rejected", "status": "rejected"},
            {"id": "accepted", "title": "Accepted", "status": "accepted"},
            {"id": "archive", "title": "Archive", "status": "archive"},
        ]

        kanban_columns = []
        for column in columns:
            column_apps = [app for app in applications if app.status == column["status"]]
            kanban_columns.append({
                "id": column["id"],
                "title": column["title"],
                "status": column["status"],
                "applications": [ApplicationResponse.model_validate(app) for app in column_apps],
            })

        return KanbanBoardResponse(columns=kanban_columns)
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching kanban board: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch kanban board due to database error.",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error fetching kanban board: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching kanban board.",
        ) from e


@router.get("/applications/{application_id}/career-case", response_model=CareerCaseResponse)
async def get_career_case(
    application_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CareerCaseResponse:
    """Get full career case for an application."""
    try:
        repo = WorkflowRepository(db)

        application = await repo.get_application(str(application_id))
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        if application.user_id != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this application",
            )

        # Get related data
        timeline = await repo.get_timeline_events(str(application_id))
        tasks = await repo.get_tasks(user_id=str(current_user.id), application_id=str(application_id))

        # Would fetch resume, job, company from respective repositories
        resume_data = {}
        job_data = {}
        company_data = None

        return CareerCaseResponse(
            application=ApplicationResponse.model_validate(application),
            resume=resume_data,
            job=job_data,
            company=company_data,
            timeline=[TimelineEventResponse.model_validate(event) for event in timeline],
            tasks=[TaskResponse.model_validate(task) for task in tasks],
            notes=[],
            documents=[],
            ai_insights={},
        )
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching career case {application_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch career case due to database error.",
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error fetching career case {application_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the career case.",
        ) from e
