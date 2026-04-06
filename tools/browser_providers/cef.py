"""CEF (Chromium Embedded Framework) browser provider — stub for maceip/cef.

This provider is a forward-looking integration point for the CEF-based browser
backend at https://github.com/maceip/cef.  It is NOT functional yet — all
methods raise NotImplementedError or return False.

When CEF is ready, this provider will:
  - Connect to a CEF instance via its REST/WebSocket API
  - Create isolated browser contexts for each task
  - Expose the same CDP-compatible interface that agent-browser expects
  - Support local-only mode (no cloud, no third-party data transit)

Activation (future):
    # ~/.hermes/config.yaml
    browser:
      cloud_provider: "cef"

    # Environment
    CEF_URL=http://localhost:9222
"""

import logging
import os
from typing import Dict

from tools.browser_providers.base import CloudBrowserProvider

logger = logging.getLogger(__name__)


class CefProvider(CloudBrowserProvider):
    """CEF browser backend (stub — not yet functional).

    Planned to integrate with https://github.com/maceip/cef for a fully
    local, privacy-preserving browser backend without cloud dependencies.
    """

    def provider_name(self) -> str:
        return "cef"

    def is_configured(self) -> bool:
        """True when CEF_URL is set, indicating a running CEF instance."""
        return bool(os.environ.get("CEF_URL"))

    def create_session(self, task_id: str) -> Dict[str, object]:
        """Create a CEF browser session.

        TODO: Implement when maceip/cef exposes a session management API.
        Expected flow:
          1. POST {CEF_URL}/sessions with task_id
          2. Receive CDP websocket URL for the new context
          3. Return session metadata dict
        """
        cef_url = os.environ.get("CEF_URL", "http://localhost:9222")
        raise NotImplementedError(
            f"CEF provider is a stub — maceip/cef integration pending. "
            f"CEF_URL={cef_url}. Use 'local' or 'browserbase' backend for now."
        )

    def close_session(self, session_id: str) -> bool:
        """Close a CEF browser session.

        TODO: Implement DELETE {CEF_URL}/sessions/{session_id}
        """
        logger.warning("CEF close_session stub called for %s", session_id)
        return False

    def emergency_cleanup(self, session_id: str) -> None:
        """Best-effort cleanup during process exit."""
        logger.debug("CEF emergency_cleanup stub for %s", session_id)
