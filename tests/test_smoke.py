"""Smoke tests for ml-automation-nlp — validate plugin layout invariants."""

import json
import re
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def test_manifest_validity() -> None:
    """Validate that .cortex-plugin/plugin.json is valid JSON with required fields."""
    manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"

    assert manifest_path.exists(), f"Manifest not found at {manifest_path}"

    with open(manifest_path) as f:
        manifest = json.load(f)

    # Required fields per plugin.md
    required_fields = {"name", "version", "description", "cortex"}
    assert required_fields.issubset(
        manifest.keys()
    ), f"Missing required fields. Got: {manifest.keys()}"

    # Cortex config must have directory pointers
    cortex = manifest.get("cortex", {})
    assert "agents_dir" in cortex, "Missing cortex.agents_dir"
    assert "skills_dir" in cortex, "Missing cortex.skills_dir"
    assert "commands_dir" in cortex, "Missing cortex.commands_dir"
    assert "hooks_dir" in cortex, "Missing cortex.hooks_dir"

    # Version must be semver-like
    assert re.match(r"^\d+\.\d+\.\d+", manifest["version"]), (
        f"Version '{manifest['version']}' does not match semver"
    )


def test_agents_md_referential_integrity() -> None:
    """Verify AGENTS.md references match actual agent and skill files on disk."""
    agents_md_path = PLUGIN_ROOT / "AGENTS.md"
    assert agents_md_path.exists(), f"AGENTS.md not found at {agents_md_path}"

    with open(agents_md_path) as f:
        content = f.read()

    # Extract agent names from "Available Agents" table
    agents_section = re.search(
        r"## Available Agents\s*\|\s*Agent\s*\|\s*When.*?\n(.*?)(?=##|$)",
        content,
        re.DOTALL,
    )
    assert agents_section, "No 'Available Agents' section found in AGENTS.md"

    agents_text = agents_section.group(1)
    agent_names = re.findall(r"^\|\s*`([^`]+)`", agents_text, re.MULTILINE)

    # Verify each agent has a corresponding .md file
    agents_dir = PLUGIN_ROOT / "agents"
    for agent_name in agent_names:
        agent_file = agents_dir / f"{agent_name}.md"
        assert agent_file.exists(), (
            f"Agent '{agent_name}' referenced in AGENTS.md but {agent_file} not found"
        )

    # Extract skill names from "Available Skills" table
    skills_section = re.search(
        r"## Available Skills\s*\|\s*Skill\s*\|\s*Trigger.*?\n(.*?)(?=##|$)",
        content,
        re.DOTALL,
    )
    assert skills_section, "No 'Available Skills' section found in AGENTS.md"

    skills_text = skills_section.group(1)
    skill_names = re.findall(r"^\|\s*`/([^`]+)`", skills_text, re.MULTILINE)

    # Verify each skill has a corresponding SKILL.md file
    skills_dir = PLUGIN_ROOT / "skills"
    for skill_name in skill_names:
        skill_file = skills_dir / skill_name / "SKILL.md"
        assert skill_file.exists(), (
            f"Skill '/{skill_name}' referenced in AGENTS.md but {skill_file} not found"
        )
