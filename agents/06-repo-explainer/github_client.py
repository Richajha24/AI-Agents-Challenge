"""GitHub API client for fetching public repository metadata."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

import requests

GITHUB_API = "https://api.github.com"
REQUEST_TIMEOUT = 30

KEY_FILES = (
    "README.md",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
    "main.py",
    "app.py",
    "index.js",
    "tsconfig.json",
)

GITHUB_URL_PATTERN = re.compile(
    r"^(?:https?://)?(?:www\.)?github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+)/?$",
    re.IGNORECASE,
)


class GitHubClientError(Exception):
    """Base error for GitHub client operations."""


class InvalidRepoURLError(GitHubClientError):
    """Raised when the repository URL is malformed."""


class RepositoryNotFoundError(GitHubClientError):
    """Raised when the repository does not exist or is inaccessible."""


@dataclass
class RepositoryData:
    owner: str
    repo: str
    metadata: dict[str, Any]
    readme: str
    file_tree: list[str] = field(default_factory=list)
    key_file_contents: dict[str, str] = field(default_factory=dict)


def parse_github_url(url: str) -> tuple[str, str]:
    """Extract owner and repository name from a GitHub URL."""
    cleaned = url.strip().rstrip("/")
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]

    match = GITHUB_URL_PATTERN.match(cleaned)
    if match:
        return match.group("owner"), match.group("repo")

    parsed = urlparse(cleaned if "://" in cleaned else f"https://{cleaned}")
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        raise InvalidRepoURLError(
            f"Invalid GitHub repository URL: {url}\n"
            "Expected format: https://github.com/owner/repository"
        )

    parts = [part for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        raise InvalidRepoURLError(
            f"Invalid GitHub repository URL: {url}\n"
            "Expected format: https://github.com/owner/repository"
        )

    owner, repo = parts[0], parts[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    return owner, repo


class GitHubClient:
    """Fetch public repository information from the GitHub REST API."""

    def __init__(self, token: str | None = None) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "User-Agent": "repo-explainer-agent",
            }
        )
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = f"{GITHUB_API}{path}"
        try:
            response = self.session.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
        except requests.ConnectionError as exc:
            raise GitHubClientError(
                "Could not connect to GitHub API. Check your network connection."
            ) from exc
        except requests.Timeout as exc:
            raise GitHubClientError("GitHub API request timed out.") from exc
        except requests.RequestException as exc:
            raise GitHubClientError(f"GitHub request failed: {exc}") from exc

        if response.status_code == 404:
            raise RepositoryNotFoundError("Repository not found or not publicly accessible.")
        if response.status_code == 403:
            message = response.json().get("message", "Access forbidden.")
            if "rate limit" in message.lower():
                raise GitHubClientError(
                    "GitHub API rate limit exceeded. Set GITHUB_TOKEN in .env for higher limits."
                )
            raise GitHubClientError(f"GitHub API error: {message}")
        if response.status_code >= 400:
            message = response.json().get("message", response.text)
            raise GitHubClientError(f"GitHub API error ({response.status_code}): {message}")

        return response

    def fetch_repository(self, url: str) -> RepositoryData:
        owner, repo = parse_github_url(url)
        metadata = self._request("GET", f"/repos/{owner}/{repo}").json()
        readme = self._fetch_readme(owner, repo)
        file_tree = self._fetch_file_tree(owner, repo, metadata.get("default_branch", "main"))
        key_file_contents = self._fetch_key_files(owner, repo, file_tree)

        return RepositoryData(
            owner=owner,
            repo=repo,
            metadata=metadata,
            readme=readme,
            file_tree=file_tree,
            key_file_contents=key_file_contents,
        )

    def _fetch_readme(self, owner: str, repo: str) -> str:
        try:
            response = self._request(
                "GET",
                f"/repos/{owner}/{repo}/readme",
                headers={"Accept": "application/vnd.github.raw"},
            )
            return response.text[:8000]
        except RepositoryNotFoundError:
            return "(No README found)"

    def _fetch_file_tree(self, owner: str, repo: str, branch: str) -> list[str]:
        try:
            response = self._request("GET", f"/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
            tree = response.json().get("tree", [])
            return [
                item["path"]
                for item in tree
                if item.get("type") == "blob" and not item["path"].startswith(".git/")
            ]
        except GitHubClientError:
            return []

    def _fetch_key_files(self, owner: str, repo: str, file_tree: list[str]) -> dict[str, str]:
        tree_set = set(file_tree)
        contents: dict[str, str] = {}

        for filename in KEY_FILES:
            matches = [path for path in file_tree if path == filename or path.endswith(f"/{filename}")]
            for path in matches[:1]:
                if path not in tree_set:
                    continue
                try:
                    response = self._request(
                        "GET",
                        f"/repos/{owner}/{repo}/contents/{path}",
                        headers={"Accept": "application/vnd.github.raw"},
                    )
                    contents[path] = response.text[:4000]
                except GitHubClientError:
                    continue
        return contents


def build_repo_context(data: RepositoryData) -> str:
    """Format repository data for the LLM prompt."""
    meta = data.metadata
    topics = ", ".join(meta.get("topics") or []) or "None listed"
    languages = meta.get("language") or "Not detected"

    tree_preview = "\n".join(data.file_tree[:120])
    if len(data.file_tree) > 120:
        tree_preview += f"\n... and {len(data.file_tree) - 120} more files"

    key_files_section = ""
    for path, content in data.key_file_contents.items():
        key_files_section += f"\n### {path}\n```\n{content}\n```\n"

    return f"""Analyze this GitHub repository and produce the required structured report.

## Repository
- URL: https://github.com/{data.owner}/{data.repo}
- Name: {meta.get("full_name", f"{data.owner}/{data.repo}")}
- Description: {meta.get("description") or "No description provided"}
- Primary language: {languages}
- Stars: {meta.get("stargazers_count", 0)}
- Forks: {meta.get("forks_count", 0)}
- Default branch: {meta.get("default_branch", "main")}
- Topics: {topics}
- License: {(meta.get("license") or {}).get("spdx_id", "Unknown")}
- Open issues: {meta.get("open_issues_count", 0)}
- Created: {meta.get("created_at", "Unknown")}
- Last updated: {meta.get("updated_at", "Unknown")}

## README
{data.readme}

## File Tree ({len(data.file_tree)} files)
{tree_preview or "(File tree unavailable)"}

## Key File Contents
{key_files_section or "(No key configuration files fetched)"}
"""
