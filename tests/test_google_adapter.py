from unittest.mock import patch, MagicMock
from adapters.google_adapter import mark_as_read, mark_as_unread, move_to_inbox


class TestMarkAsRead:
    @patch('adapters.google_adapter.print')
    def test_mark_as_read_success(self, mock_print):
        mock_service = MagicMock()
        mock_execute = MagicMock()
        mock_service.users.return_value.messages.return_value.modify.return_value.execute = mock_execute

        message_id = "example_message_id"
        mark_as_read(mock_service, message_id)

        mock_service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=message_id,
            body={"removeLabelIds": ["UNREAD"]}
        )
        mock_execute.assert_called_once()

        mock_print.assert_called_once_with(f"Email message with ID '{message_id}' marked as read.")

    @patch('adapters.google_adapter.print')
    def test_mark_as_read_failure(self, mock_print):
        mock_service = MagicMock()
        mock_service.users.return_value.messages.return_value.modify.side_effect = Exception("Error message")

        message_id = "example_message_id"
        mark_as_read(mock_service, message_id)

        mock_service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=message_id,
            body={"removeLabelIds": ["UNREAD"]}
        )

        mock_print.assert_called_once_with(f"Failed to mark email message with ID '{message_id}' as read: Error message")


class TestMarkAsUnread:
    @patch('adapters.google_adapter.print')
    def test_mark_as_unread_success(self, mock_print):
        mock_service = MagicMock()
        mock_execute = MagicMock()
        mock_service.users.return_value.messages.return_value.modify.return_value.execute = mock_execute

        message_id = "example_message_id"
        mark_as_unread(mock_service, message_id)

        mock_service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=message_id,
            body={"addLabelIds": ["UNREAD"]}
        )
        mock_execute.assert_called_once()

        mock_print.assert_called_once_with(f"Email message with ID '{message_id}' marked as unread.")

    @patch('adapters.google_adapter.print')
    def test_mark_as_unread_failure(self, mock_print):
        mock_service = MagicMock()
        mock_service.users.return_value.messages.return_value.modify.side_effect = Exception("Error message")

        message_id = "example_message_id"
        mark_as_unread(mock_service, message_id)

        mock_service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=message_id,
            body={"addLabelIds": ["UNREAD"]}
        )

        mock_print.assert_called_once_with(
            f"Failed to mark email message with ID '{message_id}' as unread: Error message"
        )


class TestMoveToInbox:
    @patch('adapters.google_adapter.print')
    def test_move_to_inbox_success(self, mock_print):
        mock_service = MagicMock()
        mock_execute = MagicMock()
        mock_service.users.return_value.messages.return_value.modify.return_value.execute = mock_execute

        message_id = "example_message_id"
        move_to_inbox(mock_service, message_id)

        mock_service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=message_id,
            body={"addLabelIds": ["INBOX"], "removeLabelIds": []}
        )
        mock_execute.assert_called_once()

        mock_print.assert_called_once_with(f"Email message with ID '{message_id}' moved to Inbox.")

    @patch('adapters.google_adapter.print')
    def test_move_to_inbox_failure(self, mock_print):
        mock_service = MagicMock()
        mock_service.users.return_value.messages.return_value.modify.side_effect = Exception("Error message")

        message_id = "example_message_id"
        move_to_inbox(mock_service, message_id)

        mock_service.users.return_value.messages.return_value.modify.assert_called_once_with(
            userId='me',
            id=message_id,
            body={"addLabelIds": ["INBOX"], "removeLabelIds": []}
        )

        mock_print.assert_called_once_with(
            f"Failed to move email message with ID '{message_id}' to Inbox: Error message"
        )
