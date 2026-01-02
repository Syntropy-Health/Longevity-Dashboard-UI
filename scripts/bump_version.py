#!/usr/bin/env python3
"""Version bump script for Longevity Clinic.

Usage:
    python scripts/bump_version.py [patch|minor|major] [--feature "feature-name"]

Examples:
    python scripts/bump_version.py patch                    # 0.2.1 -> 0.2.2
    python scripts/bump_version.py patch --feature "auth"   # 0.2.1 -> 0.2.2 + update feature tag
    python scripts/bump_version.py minor                    # 0.2.1 -> 0.3.0
    python scripts/bump_version.py major                    # 0.2.1 -> 1.0.0

This script:
1. Reads current version from pyproject.toml
2. Increments the specified part (patch by default)
3. Updates pyproject.toml
4. Optionally updates FEATURE_TAG in version.py
"""

import argparse
import re
import sys
from pathlib import Path


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse version string into (major, minor, patch) tuple."""
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(version: str, part: str) -> str:
    """Bump version by specified part."""
    major, minor, patch = parse_version(version)

    if part == "major":
        return f"{major + 1}.0.0"
    elif part == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"


def update_pyproject(new_version: str) -> bool:
    """Update version in pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    if not pyproject_path.exists():
        print(f"❌ pyproject.toml not found at {pyproject_path}")
        return False

    content = pyproject_path.read_text()
    # Match version = "x.y.z" in [project] section
    new_content = re.sub(
        r'(version\s*=\s*")[^"]+(")',
        f"\\g<1>{new_version}\\g<2>",
        content,
        count=1,
    )

    if content == new_content:
        print("❌ Failed to update version in pyproject.toml")
        return False

    pyproject_path.write_text(new_content)
    return True


def update_feature_tag(feature: str) -> bool:
    """Update FEATURE_TAG in version.py."""
    version_path = (
        Path(__file__).parent.parent / "longevity_clinic" / "app" / "version.py"
    )

    if not version_path.exists():
        print(f"❌ version.py not found at {version_path}")
        return False

    content = version_path.read_text()
    new_content = re.sub(
        r'(FEATURE_TAG\s*=\s*")[^"]*(")',
        f"\\g<1>{feature}\\g<2>",
        content,
        count=1,
    )

    if content == new_content:
        print("❌ Failed to update FEATURE_TAG in version.py")
        return False

    version_path.write_text(new_content)
    return True


def get_current_version() -> str:
    """Read current version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text()
    match = re.search(r'version\s*=\s*"([^"]+)"', content)
    return match.group(1) if match else "0.0.0"


def main():
    parser = argparse.ArgumentParser(description="Bump version for Longevity Clinic")
    parser.add_argument(
        "part",
        nargs="?",
        default="patch",
        choices=["patch", "minor", "major"],
        help="Version part to bump (default: patch)",
    )
    parser.add_argument(
        "--feature",
        "-f",
        type=str,
        help="Feature tag to set (e.g., 'auth-improvements')",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes",
    )

    args = parser.parse_args()

    current = get_current_version()
    new_version = bump_version(current, args.part)

    print(f"📦 Version bump: {current} → {new_version}")

    if args.dry_run:
        print("🔍 Dry run - no changes made")
        if args.feature:
            print(f'   Would set FEATURE_TAG = "{args.feature}"')
        return 0

    # Update pyproject.toml
    if not update_pyproject(new_version):
        return 1
    print("✓ Updated pyproject.toml")

    # Update feature tag if provided
    if args.feature:
        if not update_feature_tag(args.feature):
            return 1
        print(f'✓ Updated FEATURE_TAG to "{args.feature}"')

    print(f"\n✅ Version bumped to {new_version}")
    print("   Run: git add pyproject.toml longevity_clinic/app/version.py")
    print(f"   Then: git commit -m 'chore: bump version to {new_version}'")

    return 0


if __name__ == "__main__":
    sys.exit(main())
