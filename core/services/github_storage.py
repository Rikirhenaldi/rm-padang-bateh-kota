import base64
import json
import urllib.error
import urllib.request

from django.conf import settings

from .base import StorageBackend, StorageError


class GitHubStorage(StorageBackend):
    def __init__(self):
        self.base_url = f"https://api.github.com/repos/{settings.GITHUB_OWNER}/{settings.GITHUB_REPOSITORY}/contents"
        self.cache = {}

    def _request(self, method, path, payload=None):
        if not settings.GITHUB_TOKEN or not settings.GITHUB_OWNER or not settings.GITHUB_REPOSITORY:
            raise StorageError("GitHub storage is not configured")
        body = None if payload is None else json.dumps(payload).encode()
        request = urllib.request.Request(
            f"{self.base_url}/{path.lstrip('/')}",
            data=body,
            method=method,
            headers={"Authorization": f"Bearer {settings.GITHUB_TOKEN}", "Accept": "application/vnd.github+json", "User-Agent": "rm-padang-django"},
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                raw = response.read()
                return response.status, json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return 404, None
            detail = exc.read().decode(errors="replace")
            raise StorageError(f"GitHub API {exc.code}: {detail[:300]}") from exc
        except urllib.error.URLError as exc:
            raise StorageError(f"GitHub connection failed: {exc.reason}") from exc

    def _get(self, path):
        status, result = self._request("GET", f"{path}?ref={settings.GITHUB_BRANCH}")
        if status == 404:
            return None, None
        try:
            content = base64.b64decode(result["content"].replace("\n", ""))
        except (KeyError, ValueError) as exc:
            raise StorageError("Invalid GitHub content response") from exc
        return content, result.get("sha")

    def _put(self, path, content, message, sha=None):
        payload = {"message": message, "content": base64.b64encode(content).decode(), "branch": settings.GITHUB_BRANCH}
        if sha:
            payload["sha"] = sha
        status, result = self._request("PUT", path, payload)
        if status not in (200, 201):
            raise StorageError("GitHub did not accept the change")
        return result

    def load_json(self, name):
        content, _ = self._get(name)
        if content is None:
            return None
        try:
            return json.loads(content.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise StorageError(f"Invalid JSON in GitHub file {name}") from exc

    def save_json(self, name, value, message):
        content, sha = self._get(name)
        raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()
        self._put(name, raw, message, sha)
        self.invalidate()

    def save_image(self, path, content, message):
        _, sha = self._get(path)
        self._put(path, content, message, sha)
        return "/media/" + path

    def delete_image(self, path, message):
        _, sha = self._get(path)
        if sha:
            self._request("DELETE", path, {"message": message, "sha": sha, "branch": settings.GITHUB_BRANCH})
        self.invalidate()

    def read_image(self, path):
        content, _ = self._get(path)
        if content is None:
            raise FileNotFoundError(path)
        return content

    def invalidate(self):
        self.cache.clear()
