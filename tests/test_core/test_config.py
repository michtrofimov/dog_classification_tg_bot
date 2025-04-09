from pydantic import SecretStr

from photo_enhancer_tg_bot.core.config import Settings


def test_config_loads():
    """Test that config loads without errors"""
    config = Settings()
    assert config is not None


def test_token_is_secret_type():
    """Verify token is properly protected as SecretStr"""
    config = Settings()
    assert isinstance(config.bot.token, SecretStr)
    assert "**********" in str(config.bot.token)  # Test masking


def test_token_accessible():
    """Verify token can be accessed when needed"""
    config = Settings()
    assert len(config.bot.token.get_secret_value()) > 5  # Basic length check
