
# Your in-memory repository here

from .models import SequenceSubmission
from django.db.models import QuerySet


class SubmissionRepository:
    """Repository class to handle submissions CRUD operations"""

    def get_all_submissions(self) -> QuerySet:
        """Retrieve all submissions from the database."""
        return SequenceSubmission.objects.all()

    def get_submission_by_id(self, submission_id: int) -> SequenceSubmission:
        """Retrieve a single submission by its ID."""
        return SequenceSubmission.objects.get(id=submission_id)

    def create_submission(self, title: str, content: str) -> SequenceSubmission:
        """Create and save a new submission."""
        submission = SequenceSubmission(title=title, content=content)
        submission.save()
        return submission

    def update_submission(self, submission_id: int, title: str, content: str) -> SequenceSubmission:
        """Update an existing submission."""
        submission = SequenceSubmission.objects.get(id=submission_id)
        submission.title = title
        submission.content = content
        submission.save()
        return submission

    def delete_submission(self, submission_id: int) -> None:
        """Delete a submission by its ID."""
        submission = SequenceSubmission.objects.get(id=submission_id)
        submission.delete()