from unittest.mock import patch

import pytest

from photo_enhancer_tg_bot.cache.serialization import (
    AbstractSerializer,
    JSONSerializer,
    PickleSerializer,
)


class TestAbstractSerializer:
    def test_interface(self):
        """Verify abstract methods must be implemented"""
        with pytest.raises(TypeError):
            AbstractSerializer()  # Can't instantiate abstract class


class TestPickleSerializer:
    @pytest.fixture
    def serializer(self):
        return PickleSerializer()

    def test_roundtrip(self, serializer):
        """Test pickle serialization/deserialization"""
        original = {"key": "value", "num": 42}
        serialized = serializer.serialize(original)
        assert isinstance(serialized, bytes)

        deserialized = serializer.deserialize(serialized)
        assert deserialized == original

    @patch("pickle.loads")
    def test_deserialize_security(self, mock_loads, serializer):
        """Verify pickle security warning is suppressed"""
        test_data = b"test"
        serializer.deserialize(test_data)
        mock_loads.assert_called_once_with(test_data)


class TestJSONSerializer:
    @pytest.fixture
    def serializer(self):
        return JSONSerializer()

    @pytest.mark.parametrize(
        "data", [{"simple": "dict"}, ["list", 1, 2.5], "string", 42, None]
    )
    def test_roundtrip(self, serializer, data):
        """Test JSON serialization with various types"""
        serialized = serializer.serialize(data)
        assert isinstance(serialized, bytes)

        deserialized = serializer.deserialize(serialized)
        assert deserialized == data

    def test_datetime_support(self, serializer):
        """Verify orjson handles datetime"""
        from datetime import datetime

        original = {"time": datetime(2023, 1, 1)}
        serialized = serializer.serialize(original)
        assert b"2023-01-01" in serialized
