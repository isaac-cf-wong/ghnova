"""Unit tests for the base pull request class."""

from ghnova.pull_request.base import BasePullRequest


class TestBasePullRequest:
    """Test cases for the BasePullRequest class."""

    def test_list_pull_requests_endpoint(self):
        """Test _list_pull_requests_endpoint method."""
        base_pr = BasePullRequest()
        endpoint = base_pr._list_pull_requests_endpoint(owner="test-owner", repository="test-repo")
        assert endpoint == "/repos/test-owner/test-repo/pulls"

    def test_list_pull_requests_helper_no_params(self):
        """Test _list_pull_requests_helper with no optional parameters."""
        base_pr = BasePullRequest()
        endpoint, params, kwargs = base_pr._list_pull_requests_helper(owner="test-owner", repository="test-repo")
        assert endpoint == "/repos/test-owner/test-repo/pulls"
        assert params == {}
        assert "headers" in kwargs
        assert kwargs["headers"]["Accept"] == "application/vnd.github+json"
        assert kwargs["headers"]["X-GitHub-Api-Version"] == "2022-11-28"

    def test_list_pull_requests_helper_with_params(self):
        """Test _list_pull_requests_helper with all parameters."""
        base_pr = BasePullRequest()
        endpoint, params, kwargs = base_pr._list_pull_requests_helper(
            owner="test-owner",
            repository="test-repo",
            state="open",
            head="feature-branch",
            base="main",
            sort="created",
            direction="desc",
            per_page=50,
            page=2,
        )
        assert endpoint == "/repos/test-owner/test-repo/pulls"
        expected_params = {
            "state": "open",
            "head": "feature-branch",
            "base": "main",
            "sort": "created",
            "direction": "desc",
            "per_page": 50,
            "page": 2,
        }
        assert params == expected_params
        assert "headers" in kwargs
        assert kwargs["headers"]["Accept"] == "application/vnd.github+json"
        assert kwargs["headers"]["X-GitHub-Api-Version"] == "2022-11-28"

    def test_list_pull_requests_helper_with_existing_headers(self):
        """Test _list_pull_requests_helper with existing headers in kwargs."""
        base_pr = BasePullRequest()
        existing_headers = {"Authorization": "token abc123"}
        kwargs = {"headers": existing_headers}
        endpoint, params, kwargs_out = base_pr._list_pull_requests_helper(
            owner="test-owner", repository="test-repo", **kwargs
        )
        assert endpoint == "/repos/test-owner/test-repo/pulls"
        assert params == {}
        assert "headers" in kwargs_out
        assert kwargs_out["headers"]["Accept"] == "application/vnd.github+json"
        assert kwargs_out["headers"]["X-GitHub-Api-Version"] == "2022-11-28"
        assert kwargs_out["headers"]["Authorization"] == "token abc123"

    def test_list_pull_requests_helper_partial_params(self):
        """Test _list_pull_requests_helper with some parameters."""
        base_pr = BasePullRequest()
        endpoint, params, _kwargs = base_pr._list_pull_requests_helper(
            owner="test-owner", repository="test-repo", state="closed", per_page=10
        )
        assert endpoint == "/repos/test-owner/test-repo/pulls"
        expected_params = {"state": "closed", "per_page": 10}
        assert params == expected_params
