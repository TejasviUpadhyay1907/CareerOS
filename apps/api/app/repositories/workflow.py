"""Repository layer for workflow engine data access."""
from typing import Any, Optional
from datetime import datetime

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.db.models import (
    ActivityLog,
    Application,
    ApplicationDocument,
    ApplicationEvent,
    ApplicationFollowup,
    ApplicationNote,
    ApplicationStatusHistory,
    ApplicationTask,
    CompanyProfile,
    Contact,
    Notification,
    TimelineEvent,
)

logger = get_logger(__name__)


class WorkflowRepository:
    """Repository for workflow engine operations."""

    def __init__(self, db: AsyncSession):
        """Initialize repository.

        Args:
            db: Database session
        """
        self.db = db

    async def create_application(
        self,
        user_id: str,
        resume_id: str,
        job_id: Optional[str] = None,
        company_id: Optional[str] = None,
        status: str = "wishlist",
        priority: str = "medium",
        probability: int = 50,
        notes: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> Application:
        """Create application record.

        Args:
            user_id: User ID
            resume_id: Resume ID
            job_id: Job ID
            company_id: Company ID
            status: Application status
            priority: Application priority
            probability: Success probability
            notes: Notes
            metadata: Additional metadata

        Returns:
            Created application
        """
        application = Application(
            user_id=user_id,
            resume_id=resume_id,
            job_id=job_id,
            company_id=company_id,
            status=status,
            priority=priority,
            probability=probability,
            notes=notes,
            extra_metadata=metadata or {},
        )

        self.db.add(application)
        await self.db.commit()
        await self.db.refresh(application)

        logger.info(f"Created application: {application.id}")
        return application

    async def update_application_status(
        self,
        application_id: str,
        new_status: str,
        reason: Optional[str] = None,
        changed_by: str = "user",
    ) -> Application:
        """Update application status.

        Args:
            application_id: Application ID
            new_status: New status
            reason: Reason for change
            changed_by: Who made the change

        Returns:
            Updated application
        """
        application = await self.get_application(application_id)
        old_status = application.status

        # Create status history record
        status_history = ApplicationStatusHistory(
            application_id=application_id,
            old_status=old_status,
            new_status=new_status,
            reason=reason,
            changed_by=changed_by,
        )
        self.db.add(status_history)

        # Update application
        application.status = new_status
        await self.db.commit()
        await self.db.refresh(application)

        logger.info(f"Updated application {application_id} status from {old_status} to {new_status}")
        return application

    async def get_application(self, application_id: str) -> Optional[Application]:
        """Get application by ID.

        Args:
            application_id: Application ID

        Returns:
            Application or None
        """
        query = select(Application).where(
            Application.id == application_id, Application.is_deleted == False
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_applications(
        self,
        user_id: str,
        status: Optional[str] = None,
        company_id: Optional[str] = None,
    ) -> list[Application]:
        """Get applications for user.

        Args:
            user_id: User ID
            status: Filter by status
            company_id: Filter by company

        Returns:
            List of applications
        """
        query = select(Application).where(
            Application.user_id == user_id, Application.is_deleted == False
        )

        if status:
            query = query.where(Application.status == status)
        if company_id:
            query = query.where(Application.company_id == company_id)

        query = query.order_by(Application.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_application_task(
        self,
        application_id: str,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: str = "medium",
        task_type: str = "general",
    ) -> ApplicationTask:
        """Create application task.

        Args:
            application_id: Application ID
            user_id: User ID
            title: Task title
            description: Task description
            due_date: Due date
            priority: Task priority
            task_type: Task type

        Returns:
            Created task
        """
        task = ApplicationTask(
            application_id=application_id,
            user_id=user_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            task_type=task_type,
            status="pending",
        )

        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)

        logger.info(f"Created task: {task.id}")
        return task

    async def get_tasks(
        self,
        user_id: str,
        application_id: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[ApplicationTask]:
        """Get tasks for user.

        Args:
            user_id: User ID
            application_id: Filter by application
            status: Filter by status

        Returns:
            List of tasks
        """
        query = select(ApplicationTask).where(
            ApplicationTask.user_id == user_id, ApplicationTask.is_deleted == False
        )

        if application_id:
            query = query.where(ApplicationTask.application_id == application_id)
        if status:
            query = query.where(ApplicationTask.status == status)

        query = query.order_by(ApplicationTask.due_date.asc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_application_note(
        self,
        application_id: str,
        user_id: str,
        content: str,
        note_type: str = "general",
    ) -> ApplicationNote:
        """Create application note.

        Args:
            application_id: Application ID
            user_id: User ID
            content: Note content
            note_type: Note type

        Returns:
            Created note
        """
        note = ApplicationNote(
            application_id=application_id,
            user_id=user_id,
            content=content,
            note_type=note_type,
        )

        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)

        logger.info(f"Created note: {note.id}")
        return note

    async def create_timeline_event(
        self,
        application_id: str,
        event_type: str,
        title: str,
        description: Optional[str] = None,
        event_date: Optional[datetime] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> TimelineEvent:
        """Create timeline event.

        Args:
            application_id: Application ID
            event_type: Event type
            title: Event title
            description: Event description
            event_date: Event date
            metadata: Additional metadata

        Returns:
            Created timeline event
        """
        event = TimelineEvent(
            application_id=application_id,
            event_type=event_type,
            title=title,
            description=description,
            event_date=event_date or datetime.now(),
            extra_metadata=metadata or {},
        )

        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)

        logger.info(f"Created timeline event: {event.id}")
        return event

    async def get_timeline_events(self, application_id: str) -> list[TimelineEvent]:
        """Get timeline events for application.

        Args:
            application_id: Application ID

        Returns:
            List of timeline events
        """
        query = select(TimelineEvent).where(
            TimelineEvent.application_id == application_id, TimelineEvent.is_deleted == False
        ).order_by(TimelineEvent.event_date.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_notification(
        self,
        user_id: str,
        notification_type: str,
        title: str,
        message: str,
        priority: str = "medium",
        application_id: Optional[str] = None,
        action_url: Optional[str] = None,
    ) -> Notification:
        """Create notification.

        Args:
            user_id: User ID
            notification_type: Notification type
            title: Notification title
            message: Notification message
            priority: Notification priority
            application_id: Related application ID
            action_url: Action URL

        Returns:
            Created notification
        """
        notification = Notification(
            user_id=user_id,
            application_id=application_id,
            notification_type=notification_type,
            title=title,
            message=message,
            priority=priority,
            is_read=False,
            action_url=action_url,
        )

        self.db.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)

        logger.info(f"Created notification: {notification.id}")
        return notification

    async def get_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
    ) -> list[Notification]:
        """Get notifications for user.

        Args:
            user_id: User ID
            unread_only: Only return unread notifications

        Returns:
            List of notifications
        """
        query = select(Notification).where(
            Notification.user_id == user_id, Notification.is_deleted == False
        )

        if unread_only:
            query = query.where(Notification.is_read == False)

        query = query.order_by(Notification.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def mark_notification_read(self, notification_id: str) -> Notification:
        """Mark notification as read.

        Args:
            notification_id: Notification ID

        Returns:
            Updated notification
        """
        query = select(Notification).where(Notification.id == notification_id)
        result = await self.db.execute(query)
        notification = result.scalar_one_or_none()

        if notification:
            notification.is_read = True
            await self.db.commit()
            await self.db.refresh(notification)

        return notification

    async def create_company_profile(
        self,
        user_id: str,
        name: str,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        size: Optional[str] = None,
        location: Optional[str] = None,
        description: Optional[str] = None,
    ) -> CompanyProfile:
        """Create company profile.

        Args:
            user_id: User ID
            name: Company name
            website: Company website
            industry: Industry
            size: Company size
            location: Location
            description: Description

        Returns:
            Created company profile
        """
        company = CompanyProfile(
            user_id=user_id,
            name=name,
            website=website,
            industry=industry,
            size=size,
            location=location,
            description=description,
        )

        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)

        logger.info(f"Created company profile: {company.id}")
        return company

    async def get_company_profiles(self, user_id: str) -> list[CompanyProfile]:
        """Get company profiles for user.

        Args:
            user_id: User ID

        Returns:
            List of company profiles
        """
        query = select(CompanyProfile).where(
            CompanyProfile.user_id == user_id, CompanyProfile.is_deleted == False
        ).order_by(CompanyProfile.name.asc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def log_activity(
        self,
        user_id: str,
        action: str,
        entity_type: str,
        entity_id: Optional[str] = None,
        application_id: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> ActivityLog:
        """Log user activity.

        Args:
            user_id: User ID
            action: Action performed
            entity_type: Entity type
            entity_id: Entity ID
            application_id: Application ID
            metadata: Additional metadata

        Returns:
            Created activity log
        """
        activity = ActivityLog(
            user_id=user_id,
            application_id=application_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            extra_metadata=metadata or {},
        )

        self.db.add(activity)
        await self.db.commit()
        await self.db.refresh(activity)

        logger.info(f"Logged activity: {activity.id}")
        return activity

    async def get_activity_feed(self, user_id: str, limit: int = 20) -> list[ActivityLog]:
        """Get activity feed for user.

        Args:
            user_id: User ID
            limit: Number of activities to return

        Returns:
            List of activities
        """
        query = select(ActivityLog).where(
            ActivityLog.user_id == user_id, ActivityLog.is_deleted == False
        ).order_by(ActivityLog.created_at.desc()).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()
