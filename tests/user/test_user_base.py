"""Unit tests for the base user class."""

import pytest

from ghnova.user.base import BaseUser


class TestBaseUser:
    """Test cases for the BaseUser class."""

    def test_get_user_endpoint_authenticated(self):
        """Test _get_user_endpoint for authenticated user."""
        base_user = BaseUser()
        endpoint = base_user._get_user_endpoint(username=None, account_id=None)
        assert endpoint == "/user"

    def test_get_user_endpoint_by_username(self):
        """Test _get_user_endpoint by username."""
        base_user = BaseUser()
        endpoint = base_user._get_user_endpoint(username="octocat", account_id=None)
        assert endpoint == "/users/octocat"

    def test_get_user_endpoint_by_account_id(self):
        """Test _get_user_endpoint by account ID."""
        base_user = BaseUser()
        endpoint = base_user._get_user_endpoint(username=None, account_id=123)
        assert endpoint == "/user/123"

    def test_get_user_endpoint_both_specified(self):
        """Test _get_user_endpoint with both username and account_id raises error."""
        base_user = BaseUser()
        with pytest.raises(ValueError, match=r"Specify either username or account_id, not both."):
            base_user._get_user_endpoint(username="octocat", account_id=123)

    def test_get_user_helper_authenticated(self):
        """Test _get_user_helper for authenticated user."""
        base_user = BaseUser()
        endpoint, kwargs = base_user._get_user_helper(username=None, account_id=None)
        assert endpoint == "/user"
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_get_user_helper_by_username(self):
        """Test _get_user_helper by username."""
        base_user = BaseUser()
        endpoint, kwargs = base_user._get_user_helper(username="octocat", account_id=None)
        assert endpoint == "/users/octocat"
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def test_get_user_helper_with_additional_headers(self):
        """Test _get_user_helper with additional headers."""
        base_user = BaseUser()
        endpoint, kwargs = base_user._get_user_helper(username="octocat", headers={"Authorization": "Bearer token"})
        assert endpoint == "/users/octocat"
        assert kwargs["headers"] == {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": "Bearer token",
        }
