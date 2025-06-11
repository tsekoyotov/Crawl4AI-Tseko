import dns.resolver
import logging
import yaml
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from fastapi import Request
from typing import Dict, Optional
import aiohttp
from aiohttp import ClientTimeout

class TaskStatus(str, Enum):
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETED = "completed"

class FilterType(str, Enum):
    RAW = "raw"
    FIT = "fit"
    BM25 = "bm25"
    LLM = "llm"

def load_config() -> Dict:
    """Load and return application configuration."""
    config_path = Path(__file__).parent / "config.yml"
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    # Allow port override via environment variable
    config["app"]["port"] = int(os.getenv("PORT", config["app"]["port"]))
    return config

def setup_logging(config: Dict) -> None:
    """Configure application logging."""
    logging.basicConfig(
        level=config["logging"]["level"],
        format=config["logging"]["format"]
    )

def get_base_url(request: Request) -> str:
    """Get base URL including scheme and host."""
    return f"{request.url.scheme}://{request.url.netloc}"

def is_task_id(value: str) -> bool:
    """Check if the value matches task ID pattern."""
    return value.startswith("llm_") and "_" in value

def datetime_handler(obj: any) -> Optional[str]:
    """Handle datetime serialization for JSON."""
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def should_cleanup_task(created_at: str, ttl_seconds: int = 3600) -> bool:
    """Check if task should be cleaned up based on creation time."""
    created = datetime.fromisoformat(created_at)
    return (datetime.now() - created).total_seconds() > ttl_seconds

def decode_redis_hash(hash_data: Dict[bytes, bytes]) -> Dict[str, str]:
    """Decode Redis hash data from bytes to strings."""
    return {k.decode('utf-8'): v.decode('utf-8') for k, v in hash_data.items()}



def verify_email_domain(email: str) -> bool:
    domain = email.split('@')[1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return True if records else False
    except dns.exception.DNSException as e:
        logging.warning("DNS lookup failed for %s: %s", domain, e)
        return False
    except Exception as e:
        logging.error("Unexpected error verifying %s: %s", domain, e, exc_info=True)
        return False


async def quick_url_check(url: str, timeout: int = 3) -> bool:
    """Fast check to see if a URL is reachable within the given timeout.

    Performs a HEAD request (falling back to GET) with a short timeout so
    the caller can quickly fail before starting a full crawl.

    Args:
        url: Target URL to test.
        timeout: Timeout in seconds for the request.

    Returns:
        True if the response status is < 400 within the timeout, False otherwise.
    """
    try:
        client_timeout = ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            try:
                async with session.head(url, allow_redirects=True) as resp:
                    return resp.status < 400
            except aiohttp.ClientResponseError as e:
                if e.status != 405:
                    return False
            except Exception:
                pass

            try:
                async with session.get(
                    url,
                    allow_redirects=True,
                    headers={"Range": "bytes=0-0"},
                ) as resp:
                    return resp.status < 400
            except Exception:
                return False
    except Exception:
        return False