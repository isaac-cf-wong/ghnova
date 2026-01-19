"""Unit tests for the base issue class."""

import pytest

from ghnova.issue.base import BaseIssue


class TestBaseIssue:
    """Test cases for the BaseIssue class."""

    def test_list_issues_endpoint_authenticated_user(self):
        """Test _list_issues_endpoint for authenticated user issues."""
        base_issue = BaseIssue()
        endpoint, issue_type = base_issue._list_issues_endpoint()
        assert endpoint == "/issues"
        assert issue_type == "authenticated user issues"

    def test_list_issues_endpoint_organization(self):
        """Test _list_issues_endpoint for organization issues."""
        base_issue = BaseIssue()
        endpoint, issue_type = base_issue._list_issues_endpoint(organization="test-org")
        assert endpoint == "/orgs/test-org/issues"
        assert issue_type == "organization issues"

    def test_list_issues_endpoint_repository_with_owner(self):
        """Test _list_issues_endpoint for repository issues with owner."""
        base_issue = BaseIssue()
        endpoint, issue_type = base_issue._list_issues_endpoint(owner="test-owner", repository="test-repo")
        assert endpoint == "/repos/test-owner/test-repo/issues"
        assert issue_type == "repository issues"

    def test_list_issues_endpoint_repository_with_organization(self):
        """Test _list_issues_endpoint for repository issues with organization."""
        base_issue = BaseIssue()
        endpoint, issue_type = base_issue._list_issues_endpoint(organization="test-org", repository="test-repo")
        assert endpoint == "/repos/test-org/test-repo/issues"
        assert issue_type == "repository issues"

    def test_list_issues_endpoint_invalid_combination(self):
        """Test _list_issues_endpoint with invalid parameter combination."""
        base_issue = BaseIssue()
        with pytest.raises(ValueError, match=r"Invalid combination of owner, organization, and repository parameters."):
            base_issue._list_issues_endpoint(owner="test-owner")

    def test_list_issues_helper_authenticated_user(self):
        """Test _list_issues_helper for authenticated user issues."""
        base_issue = BaseIssue()
        endpoint, params, kwargs = base_issue._list_issues_helper(
            filter_by="assigned", state="open", per_page=50, page=2
        )
        assert endpoint == "/issues"
        assert params == {
            "filter": "assigned",
            "state": "open",
            "per_page": 50,
            "page": 2,
        }
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_list_issues_helper_organization(self):
        """Test _list_issues_helper for organization issues."""
        base_issue = BaseIssue()
        endpoint, params, kwargs = base_issue._list_issues_helper(
            organization="test-org", filter_by="created", state="closed", issue_type="issue"
        )
        assert endpoint == "/orgs/test-org/issues"
        assert params == {
            "filter": "created",
            "state": "closed",
            "type": "issue",
            "page": 1,
            "per_page": 30,
        }
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_list_issues_helper_repository(self):
        """Test _list_issues_helper for repository issues."""
        base_issue = BaseIssue()
        endpoint, params, kwargs = base_issue._list_issues_helper(
            owner="test-owner",
            repository="test-repo",
            state="all",
            labels=["bug", "enhancement"],
            sort="created",
            direction="desc",
            milestone="v1.0",
            assignee="test-user",
        )
        assert endpoint == "/repos/test-owner/test-repo/issues"
        assert params == {
            "state": "all",
            "labels": "bug,enhancement",
            "sort": "created",
            "direction": "desc",
            "milestone": "v1.0",
            "assignee": "test-user",
            "page": 1,
            "per_page": 30,
        }
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_list_issues_helper_with_additional_headers(self):
        """Test _list_issues_helper with additional headers."""
        base_issue = BaseIssue()
        endpoint, params, kwargs = base_issue._list_issues_helper(
            headers={"Authorization": "Bearer token"}, state="open"
        )
        assert endpoint == "/issues"
        assert params == {
            "state": "open",
            "page": 1,
            "per_page": 30,
        }
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer token",
        }

    def test_create_issue_endpoint(self):
        """Test _create_issue_endpoint."""
        base_issue = BaseIssue()
        endpoint = base_issue._create_issue_endpoint("test-owner", "test-repo")
        assert endpoint == "/repos/test-owner/test-repo/issues"

    def test_create_issue_helper(self):
        """Test _create_issue_helper."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._create_issue_helper(
            owner="test-owner",
            repository="test-repo",
            title="Test Issue",
            body="This is a test issue.",
            assignee="test-user",
            labels=["bug"],
            assignees=["user1", "user2"],
        )
        assert endpoint == "/repos/test-owner/test-repo/issues"
        assert payload == {
            "title": "Test Issue",
            "body": "This is a test issue.",
            "assignee": "test-user",
            "labels": ["bug"],
            "assignees": ["user1", "user2"],
        }
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_create_issue_helper_minimal(self):
        """Test _create_issue_helper with minimal parameters."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._create_issue_helper(
            owner="test-owner", repository="test-repo", title="Minimal Issue"
        )
        assert endpoint == "/repos/test-owner/test-repo/issues"
        assert payload == {"title": "Minimal Issue"}
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_create_issue_helper_with_additional_headers(self):
        """Test _create_issue_helper with additional headers."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._create_issue_helper(
            owner="test-owner",
            repository="test-repo",
            title="Test Issue",
            headers={"Authorization": "Bearer token"},
        )
        assert endpoint == "/repos/test-owner/test-repo/issues"
        assert payload == {"title": "Test Issue"}
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer token",
        }

    def test_get_issue_endpoint(self):
        """Test _get_issue_endpoint."""
        base_issue = BaseIssue()
        endpoint = base_issue._get_issue_endpoint("test-owner", "test-repo", 123)
        assert endpoint == "/repos/test-owner/test-repo/issues/123"

    def test_get_issue_helper(self):
        """Test _get_issue_helper."""
        base_issue = BaseIssue()
        endpoint, kwargs = base_issue._get_issue_helper("test-owner", "test-repo", 123)
        assert endpoint == "/repos/test-owner/test-repo/issues/123"
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_get_issue_helper_with_additional_headers(self):
        """Test _get_issue_helper with additional headers."""
        base_issue = BaseIssue()
        endpoint, kwargs = base_issue._get_issue_helper(
            "test-owner", "test-repo", 123, headers={"Authorization": "Bearer token"}
        )
        assert endpoint == "/repos/test-owner/test-repo/issues/123"
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer token",
        }

    def test_update_issue_endpoint(self):
        """Test _update_issue_endpoint."""
        base_issue = BaseIssue()
        endpoint = base_issue._update_issue_endpoint("test-owner", "test-repo", 123)
        assert endpoint == "/repos/test-owner/test-repo/issues/123"

    def test_update_issue_helper(self):
        """Test _update_issue_helper."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._update_issue_helper(
            owner="test-owner",
            repository="test-repo",
            issue_number=123,
            title="Updated Title",
            body="Updated body.",
            state="closed",
            labels=["fixed"],
        )
        assert endpoint == "/repos/test-owner/test-repo/issues/123"
        assert payload == {
            "title": "Updated Title",
            "body": "Updated body.",
            "state": "closed",
            "labels": ["fixed"],
        }
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_update_issue_helper_minimal(self):
        """Test _update_issue_helper with minimal parameters."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._update_issue_helper(
            owner="test-owner", repository="test-repo", issue_number=123
        )
        assert endpoint == "/repos/test-owner/test-repo/issues/123"
        assert payload == {}
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_update_issue_helper_with_additional_headers(self):
        """Test _update_issue_helper with additional headers."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._update_issue_helper(
            owner="test-owner",
            repository="test-repo",
            issue_number=123,
            title="Updated Title",
            headers={"Authorization": "Bearer token"},
        )
        assert endpoint == "/repos/test-owner/test-repo/issues/123"
        assert payload == {"title": "Updated Title"}
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer token",
        }

    def test_lock_issue_endpoint(self):
        """Test _lock_issue_endpoint."""
        base_issue = BaseIssue()
        endpoint = base_issue._lock_issue_endpoint("test-owner", "test-repo", 123)
        assert endpoint == "/repos/test-owner/test-repo/issues/123/lock"

    def test_lock_issue_helper(self):
        """Test _lock_issue_helper."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._lock_issue_helper(
            owner="test-owner", repository="test-repo", issue_number=123, lock_reason="off-topic"
        )
        assert endpoint == "/repos/test-owner/test-repo/issues/123/lock"
        assert payload == {"lock_reason": "off-topic"}
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_lock_issue_helper_no_reason(self):
        """Test _lock_issue_helper without lock reason."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._lock_issue_helper(
            owner="test-owner", repository="test-repo", issue_number=123
        )
        assert endpoint == "/repos/test-owner/test-repo/issues/123/lock"
        assert payload == {}
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_lock_issue_helper_with_additional_headers(self):
        """Test _lock_issue_helper with additional headers."""
        base_issue = BaseIssue()
        endpoint, payload, kwargs = base_issue._lock_issue_helper(
            owner="test-owner",
            repository="test-repo",
            issue_number=123,
            lock_reason="spam",
            headers={"Authorization": "Bearer token"},
        )
        assert endpoint == "/repos/test-owner/test-repo/issues/123/lock"
        assert payload == {"lock_reason": "spam"}
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer token",
        }

    def test_unlock_issue_endpoint(self):
        """Test _unlock_issue_endpoint."""
        base_issue = BaseIssue()
        endpoint = base_issue._unlock_issue_endpoint("test-owner", "test-repo", 123)
        assert endpoint == "/repos/test-owner/test-repo/issues/123/lock"

    def test_unlock_issue_helper(self):
        """Test _unlock_issue_helper."""
        base_issue = BaseIssue()
        endpoint, kwargs = base_issue._unlock_issue_helper("test-owner", "test-repo", 123)
        assert endpoint == "/repos/test-owner/test-repo/issues/123/lock"
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_unlock_issue_helper_with_additional_headers(self):
        """Test _unlock_issue_helper with additional headers."""
        base_issue = BaseIssue()
        endpoint, kwargs = base_issue._unlock_issue_helper(
            "test-owner", "test-repo", 123, headers={"Authorization": "Bearer token"}
        )
        assert endpoint == "/repos/test-owner/test-repo/issues/123/lock"
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer token",
        }
