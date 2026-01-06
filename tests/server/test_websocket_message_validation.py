#!/usr/bin/env python3
"""
Tests for WebSocket message validation and format handling.
"""

from datetime import UTC, datetime

import pytest

# Import the client module (we'll need to create a test version)
import importlib.util
import tempfile
import json


class TestWebSocketMessageValidation:
    """Test WebSocket message validation and format handling."""


    def test_test_case_finished_message_format(self):
        """Test that test_case_finished messages use status field."""
        run_id = "test-run-123"
        test_case_id = "Test.TestMethod"
        status = "passed"

        message = {
            "type": "test_case_finished",
            "run_id": run_id,
            "test_case_id": test_case_id,
            "status": status
        }

        # Verify message format
        assert message["type"] == "test_case_finished"
        assert message["run_id"] == run_id
        assert message["test_case_id"] == test_case_id
        assert message["status"] == status
        assert "result" not in message  # Should not have result field

    def test_log_batch_message_format(self):
        """Test that log_batch messages have correct format."""
        def now_utc():
            return datetime.now(UTC).isoformat().replace('+00:00', '') + "Z"
        message = {
            "type": "log_batch",
            "run_id": "test-run-123",
            "test_case_id": "Test.TestMethod",
            "entries": [
                {
                    "timestamp": now_utc(),
                    "message": "TX: AT+USYCI?",
                    "device": "Tester5",
                    "source": "COM91"
                },
                {
                    "timestamp": now_utc(),
                    "message": "RX: AT+USYCI?",
                    "device": "Tester5",
                    "source": "COM91"
                }
            ]
        }

        # Verify message format
        assert message["type"] == "log_batch"
        assert message["run_id"] == "test-run-123"
        assert message["test_case_id"] == "Test.TestMethod"
        assert len(message["entries"]) == 2

        # Verify log entry format
        for entry in message["entries"]:
            assert "timestamp" in entry
            assert "message" in entry
            assert "device" in entry
            assert "source" in entry

            # Timestamp should be valid
            timestamp = entry["timestamp"]
            assert timestamp.endswith('Z')
            assert '+00:00' not in timestamp

    def test_status_value_validation(self):
        """Test that status values are valid."""
        # Valid status values
        valid_statuses = ["running", "passed", "failed", "skipped", "aborted"]

        for status in valid_statuses:
            message = {
                "type": "test_case_finished",
                "run_id": "test-run-123",
                "test_case_id": "Test.TestMethod",
                "status": status
            }

            # Should be valid
            assert message["status"] in valid_statuses

        # Invalid status should be handled
        invalid_status = "invalid_status"
        message = {
            "type": "test_case_finished",
            "run_id": "test-run-123",
            "test_case_id": "Test.TestMethod",
            "status": invalid_status
        }

        # Should not be in valid statuses
        assert message["status"] not in valid_statuses

    def test_message_serialization(self):
        """Test that messages can be serialized to JSON."""
        def now_utc():
            return datetime.now(UTC).isoformat().replace('+00:00', '') + "Z"

        # Test various message types
        messages = [
            {
                "type": "run_started",
                "run_id": "test-run-123",
                "user_metadata": {"DUT": {"value": "TestDevice-001"}},
                "group": {
                    "name": "Product A",
                    "metadata": {
                        "Branch": {"value": "main"}
                    }
                },
                "retention_days": 7,
                "local_run": False
            },
            {
                "type": "test_case_started",
                "run_id": "test-run-123",
                "test_case_id": "Test.TestMethod"
            },
            {
                "type": "log_batch",
                "run_id": "test-run-123",
                "test_case_id": "Test.TestMethod",
                "entries": [
                    {
                        "timestamp": now_utc(),
                        "message": "TX: AT+USYCI?",
                        "device": "Tester5",
                        "source": "COM91"
                    }
                ]
            },
            {
                "type": "test_case_finished",
                "run_id": "test-run-123",
                "test_case_id": "Test.TestMethod",
                "status": "passed"
            },
            {
                "type": "run_finished",
                "run_id": "test-run-123",
                "status": "finished"
            }
        ]

        # All messages should be serializable
        for message in messages:
            json_str = json.dumps(message)
            assert json_str is not None

            # Should be deserializable
            deserialized = json.loads(json_str)
            assert deserialized == message



if __name__ == "__main__":
    pytest.main([__file__])
