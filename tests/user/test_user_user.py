"""Unit tests for the User resource."""

from unittest.mock import MagicMock, patch

from ghnova.user.user import User


class TestUser:
    """Test cases for the User class."""

    def test_get_user_authenticated(self):
        """Test get_user for authenticated user."""
        mock_client = MagicMock()
        user = User(client=mock_client)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"ETag": '"test-etag"', "Last-Modified": "Wed, 21 Oct 2015 07:28:00 GMT"}
        mock_response.json.return_value = {"login": "octocat"}

        with patch.object(user, "_get_user") as mock_get_user:
            mock_get_user.return_value = mock_response
            data, status, etag, last_mod = user.get_user()

        assert data == {"login": "octocat"}
        assert status == 200  # noqa: PLR2004
        assert etag == '"test-etag"'
        assert last_mod == "Wed, 21 Oct 2015 07:28:00 GMT"
        mock_get_user.assert_called_once_with(username=None, account_id=None, etag=None, last_modified=None)

    def test_get_user_by_username(self):
        """Test get_user by username."""
        mock_client = MagicMock()
        user = User(client=mock_client)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"login": "octocat"}

        with patch.object(user, "_get_user") as mock_get_user:
            mock_get_user.return_value = mock_response
            data, status, etag, last_mod = user.get_user(username="octocat")

        assert data == {"login": "octocat"}
        assert status == 200  # noqa: PLR2004
        assert etag is None
        assert last_mod is None
        mock_get_user.assert_called_once_with(username="octocat", account_id=None, etag=None, last_modified=None)

    def test_get_user_not_modified(self):
        """Test get_user with 304 Not Modified."""
        mock_client = MagicMock()
        user = User(client=mock_client)
        mock_response = MagicMock()
        mock_response.status_code = 304
        mock_response.headers = {"ETag": '"new-etag"'}

        with patch.object(user, "_get_user") as mock_get_user:
            mock_get_user.return_value = mock_response
            data, status, etag, last_mod = user.get_user(username="octocat", etag='"old-etag"')

        assert data == {}
        assert status == 304  # noqa: PLR2004
        assert etag == '"new-etag"'
        assert last_mod is None

    def test_get_user_with_conditional_headers(self):
        """Test get_user with etag and last_modified."""
        mock_client = MagicMock()
        user = User(client=mock_client)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {}
        mock_response.json.return_value = {"login": "octocat"}

        with patch.object(user, "_get_user") as mock_get_user:
            mock_get_user.return_value = mock_response
            data, status, _etag, _last_mod = user.get_user(
                username="octocat", etag='"test-etag"', last_modified="Wed, 21 Oct 2015 07:28:00 GMT"
            )

        assert data == {"login": "octocat"}
        assert status == 200  # noqa: PLR2004
        mock_get_user.assert_called_once_with(
            username="octocat", account_id=None, etag='"test-etag"', last_modified="Wed, 21 Oct 2015 07:28:00 GMT"
        )

    @patch("ghnova.user.user.BaseUser._get_user_helper")
    @patch("ghnova.user.user.Resource._get")
    def test_get_user_internal(self, mock_get, mock_helper):
        """Test _get_user method."""
        mock_client = MagicMock()
        user = User(client=mock_client)
        mock_helper.return_value = ("/users/octocat", {"headers": {}})
        mock_get.return_value = MagicMock()

        result = user._get_user(username="octocat", etag='"test-etag"')

        mock_helper.assert_called_once_with(username="octocat", account_id=None)
        mock_get.assert_called_once_with(endpoint="/users/octocat", etag='"test-etag"', last_modified=None, headers={})
        assert result == mock_get.return_value
