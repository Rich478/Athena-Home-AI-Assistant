#!/usr/bin/env python3
"""
Simple script to start the Athena LangGraph server
"""

from langgraph_cli.__main__ import cli
import sys

# Set up arguments for the dev server
sys.argv = ['langgraph', 'dev', '--host', '127.0.0.1', '--port', '2024']

# Start the server
cli()