"""Unit tests for the asynchronous User resource."""

from unittest.mock import AsyncMock, patch

import pytest

from ghnova.user.async_user import AsyncUser


class TestAsyncUser:
    """Test cases for the AsyncUser class."""

    @pytest.mark.asyncio
    async def test_get_user_authenticated(self):
        """Test get_user for authenticated user."""
        mock_client = AsyncMock()
        user = AsyncUser(client=mock_client)
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.headers = {"ETag": '"test-etag"', "Last-Modified": "Wed, 21 Oct 2015 07:28:00 GMT"}
        mock_response.json = AsyncMock(return_value={"login": "octocat"})

        with patch.object(user, "_get_user", new_callable=AsyncMock) as mock_get_user:
            mock_get_user.return_value = mock_response
            data, status, etag, last_mod = await user.get_user()

        assert data == {"login": "octocat"}
        assert status == 200  # noqa: PLR2004
        assert etag == '"test-etag"'
        assert last_mod == "Wed, 21 Oct 2015 07:28:00 GMT"
        mock_get_user.assert_called_once_with(username=None, account_id=None, etag=None, last_modified=None)

    @pytest.mark.asyncio
    async def test_get_user_by_username(self):
        """Test get_user by username."""
        mock_client = AsyncMock()
        user = AsyncUser(client=mock_client)
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.headers = {}
        mock_response.json = AsyncMock(return_value={"login": "octocat"})

        with patch.object(user, "_get_user", new_callable=AsyncMock) as mock_get_user:
            mock_get_user.return_value = mock_response
            data, status, etag, last_mod = await user.get_user(username="octocat")

        assert data == {"login": "octocat"}
        assert status == 200  # noqa: PLR2004
        assert etag is None
        assert last_mod is None
        mock_get_user.assert_called_once_with(username="octocat", account_id=None, etag=None, last_modified=None)

    @pytest.mark.asyncio
    async def test_get_user_not_modified(self):
        """Test get_user with 304 Not Modified."""
        mock_client = AsyncMock()
        user = AsyncUser(client=mock_client)
        mock_response = AsyncMock()
        mock_response.status = 304
        mock_response.headers = {"ETag": '"new-etag"'}

        with patch.object(user, "_get_user", new_callable=AsyncMock) as mock_get_user:
            mock_get_user.return_value = mock_response
            data, status, etag, last_mod = await user.get_user(username="octocat", etag='"old-etag"')

        assert data == {}
        assert status == 304  # noqa: PLR2004
        assert etag == '"new-etag"'
        assert last_mod is None

    @pytest.mark.asyncio
    async def test_get_user_with_conditional_headers(self):
        """Test get_user with etag and last_modified."""
        mock_client = AsyncMock()
        user = AsyncUser(client=mock_client)
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.headers = {}
        mock_response.json = AsyncMock(return_value={"login": "octocat"})

        with patch.object(user, "_get_user", new_callable=AsyncMock) as mock_get_user:
            mock_get_user.return_value = mock_response
            data, status, _etag, _last_mod = await user.get_user(
                username="octocat", etag='"test-etag"', last_modified="Wed, 21 Oct 2015 07:28:00 GMT"
            )

        assert data == {"login": "octocat"}
        assert status == 200  # noqa: PLR2004
        mock_get_user.assert_called_once_with(
            username="octocat", account_id=None, etag='"test-etag"', last_modified="Wed, 21 Oct 2015 07:28:00 GMT"
        )

    @pytest.mark.asyncio
    @patch("ghnova.user.async_user.BaseUser._get_user_helper")
    @patch("ghnova.user.async_user.AsyncResource._get")
    async def test_get_user_internal(self, mock_get, mock_helper):
        """Test _get_user method."""
        mock_client = AsyncMock()
        user = AsyncUser(client=mock_client)
        mock_helper.return_value = ("/users/octocat", {"headers": {}})
        mock_get.return_value = AsyncMock()

        result = await user._get_user(username="octocat", etag='"test-etag"')

        mock_helper.assert_called_once_with(username="octocat", account_id=None)
        mock_get.assert_called_once_with(endpoint="/users/octocat", etag='"test-etag"', last_modified=None, headers={})
        assert result == mock_get.return_value
