"""Unit tests for the synchronous PullRequest class."""

from unittest.mock import MagicMock, patch

from ghnova.pull_request.pull_request import PullRequest


class TestPullRequest:
    """Test cases for the PullRequest class."""

    def test_list_pull_requests_endpoint(self):
        """Test _list_pull_requests_endpoint method."""
        mock_client = MagicMock()
        pr = PullRequest(client=mock_client)
        endpoint = pr._list_pull_requests_endpoint(owner="test-owner", repository="test-repo")
        assert endpoint == "/repos/test-owner/test-repo/pulls"

    def test_list_pull_requests_helper_no_params(self):
        """Test _list_pull_requests_helper with no optional parameters."""
        mock_client = MagicMock()
        pr = PullRequest(client=mock_client)
        endpoint, params, kwargs = pr._list_pull_requests_helper(owner="test-owner", repository="test-repo")
        assert endpoint == "/repos/test-owner/test-repo/pulls"
        assert params == {}
        assert "headers" in kwargs
        assert kwargs["headers"]["Accept"] == "application/vnd.github+json"
        assert kwargs["headers"]["X-GitHub-Api-Version"] == "2022-11-28"

    def test_list_pull_requests_helper_with_params(self):
        """Test _list_pull_requests_helper with all parameters."""
        mock_client = MagicMock()
        pr = PullRequest(client=mock_client)
        endpoint, params, kwargs = pr._list_pull_requests_helper(
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
        mock_client = MagicMock()
        pr = PullRequest(client=mock_client)
        existing_headers = {"Authorization": "token abc123"}
        kwargs = {"headers": existing_headers}
        endpoint, params, kwargs_out = pr._list_pull_requests_helper(
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
        mock_client = MagicMock()
        pr = PullRequest(client=mock_client)
        endpoint, params, _kwargs = pr._list_pull_requests_helper(
            owner="test-owner", repository="test-repo", state="closed", per_page=10
        )
        assert endpoint == "/repos/test-owner/test-repo/pulls"
        expected_params = {"state": "closed", "per_page": 10}
        assert params == expected_params

    def test_list_pull_requests(self):
        """Test list_pull_requests method."""
        mock_client = MagicMock()
        pr = PullRequest(client=mock_client)
        mock_response = MagicMock()
        mock_data = [{"id": 1, "title": "Test PR"}]
        mock_status = 200
        mock_etag = '"test-etag"'
        mock_last_mod = "Wed, 21 Oct 2015 07:28:00 GMT"

        with (
            patch.object(pr, "_list_pull_requests", return_value=mock_response) as mock_private,
            patch(
                "ghnova.pull_request.pull_request.process_response_with_last_modified",
                return_value=(mock_data, mock_status, mock_etag, mock_last_mod),
            ) as mock_process,
        ):
            result = pr.list_pull_requests(owner="test-owner", repository="test-repo", state="open")

            mock_private.assert_called_once_with(
                owner="test-owner",
                repository="test-repo",
                state="open",
                head=None,
                base=None,
                sort=None,
                direction=None,
                per_page=None,
                page=None,
                etag=None,
                last_modified=None,
            )
            mock_process.assert_called_once_with(mock_response)
            assert result == (mock_data, mock_status, mock_etag, mock_last_mod)

    def test_list_pull_requests_with_all_params(self):
        """Test list_pull_requests method with all parameters."""
        mock_client = MagicMock()
        pr = PullRequest(client=mock_client)
        mock_response = MagicMock()
        mock_data = [{"id": 1, "title": "Test PR"}]
        mock_status = 200
        mock_etag = '"test-etag"'
        mock_last_mod = "Wed, 21 Oct 2015 07:28:00 GMT"

        with (
            patch.object(pr, "_list_pull_requests", return_value=mock_response) as mock_private,
            patch(
                "ghnova.pull_request.pull_request.process_response_with_last_modified",
                return_value=(mock_data, mock_status, mock_etag, mock_last_mod),
            ) as mock_process,
        ):
            result = pr.list_pull_requests(
                owner="test-owner",
                repository="test-repo",
                state="closed",
                head="feature-branch",
                base="main",
                sort="updated",
                direction="asc",
                per_page=25,
                page=3,
                etag='"old-etag"',
                last_modified="Wed, 20 Oct 2015 07:28:00 GMT",
            )

            mock_private.assert_called_once_with(
                owner="test-owner",
                repository="test-repo",
                state="closed",
                head="feature-branch",
                base="main",
                sort="updated",
                direction="asc",
                per_page=25,
                page=3,
                etag='"old-etag"',
                last_modified="Wed, 20 Oct 2015 07:28:00 GMT",
            )
            mock_process.assert_called_once_with(mock_response)
            assert result == (mock_data, mock_status, mock_etag, mock_last_mod)

    def test_private_list_pull_requests(self):
        """Test _list_pull_requests method."""
        mock_client = MagicMock()
        pr = PullRequest(client=mock_client)
        mock_response = MagicMock()

        with (
            patch.object(
                pr,
                "_list_pull_requests_helper",
                return_value=(
                    "/repos/test-owner/test-repo/pulls",
                    {"state": "open"},
                    {"headers": {"Accept": "application/vnd.github+json"}},
                ),
            ) as mock_helper,
            patch.object(pr, "_get", return_value=mock_response) as mock_get,
        ):
            result = pr._list_pull_requests(
                owner="test-owner",
                repository="test-repo",
                state="open",
                head=None,
                base=None,
                sort=None,
                direction=None,
                per_page=None,
                page=None,
                etag=None,
                last_modified=None,
            )

            mock_helper.assert_called_once_with(
                owner="test-owner",
                repository="test-repo",
                state="open",
                head=None,
                base=None,
                sort=None,
                direction=None,
                per_page=None,
                page=None,
            )
            mock_get.assert_called_once_with(
                endpoint="/repos/test-owner/test-repo/pulls",
                params={"state": "open"},
                etag=None,
                last_modified=None,
                headers={"Accept": "application/vnd.github+json"},
            )
            assert result == mock_response
