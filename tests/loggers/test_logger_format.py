import io
from crawl4ai.async_logger import AsyncLogger
from rich.console import Console


def test_float_formatting():
    """Ensure logger handles float formatting without corrupting colors."""
    buffer = io.StringIO()
    logger = AsyncLogger(verbose=True)
    logger.console = Console(file=buffer, record=True)
    logger.url_status("http://example.com", True, 0.23333)
    output = logger.console.export_text()
    assert "0.23s" in output
