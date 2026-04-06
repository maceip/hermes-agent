#!/usr/bin/env python3
"""Dedicated entry point for the Web Browsing Agent.

Launches Hermes in web-browsing-agent mode with browser-only tools and
browser-native identity. Equivalent to:

    python run_agent.py --enabled_toolsets=web-browsing-agent

but also forces the persona config so the system prompt, memory guidance,
and all behavioral instructions are fully browser-specific.

Usage:
    python run_web_agent.py
    python run_web_agent.py --query "Go to github.com/settings and find my SSH keys"
    python run_web_agent.py --model anthropic/claude-sonnet-4
"""

import os
import sys


def main():
    # Force web-browsing-agent persona before anything loads config
    os.environ.setdefault("HERMES_WEB_BROWSING_AGENT", "1")

    # Import after env setup
    from run_agent import main as agent_main, AIAgent  # noqa: F401

    # Inject --enabled_toolsets if not already specified
    if not any(arg.startswith("--enabled_toolsets") for arg in sys.argv):
        sys.argv.append("--enabled_toolsets=web-browsing-agent")

    # Run the agent
    agent_main()


if __name__ == "__main__":
    main()
