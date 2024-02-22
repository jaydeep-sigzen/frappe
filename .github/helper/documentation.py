import sys
from urllib.parse import urlparse

import requests

docs_repos = [
	"frappe_docs",
	"erpnext_documentation",
	"erpnext_com",
	"frappe_io",
]


def uri_validator(x):
	result = urlparse(x)
	return all([result.scheme, result.netloc, result.path])

<<<<<<< HEAD
def docs_link_exists(body):
	for line in body.splitlines():
		for word in line.split():
			if word.startswith('http') and uri_validator(word):
				parsed_url = urlparse(word)
				if parsed_url.netloc == "github.com":
					parts = parsed_url.path.split('/')
					if len(parts) == 5 and parts[1] == "frappe" and parts[2] in docs_repos:
						return True
				if parsed_url.netloc in ["docs.erpnext.com", "frappeframework.com"]:
					return True
=======
def is_valid_url(url: str) -> bool:
	parts = urlparse(url)
	return all((parts.scheme, parts.netloc, parts.path))


def is_documentation_link(word: str) -> bool:
	if not word.startswith("http") or not is_valid_url(word):
		return False

	parsed_url = urlparse(word)
	if parsed_url.netloc in DOCUMENTATION_DOMAINS:
		return True

	if parsed_url.netloc == "github.com":
		parts = parsed_url.path.split("/")
		if len(parts) == 5 and parts[1] == "frappe" and parts[2] in WEBSITE_REPOS:
			return True

	return False


def contains_documentation_link(body: str) -> bool:
	return any(is_documentation_link(word) for line in body.splitlines() for word in line.split())


def check_pull_request(number: str) -> "tuple[int, str]":
	response = requests.get(f"https://api.github.com/repos/frappe/frappe/pulls/{number}")
	if not response.ok:
		return 1, "Pull Request Not Found! ⚠️"

	payload = response.json()
	title = (payload.get("title") or "").lower().strip()
	head_sha = (payload.get("head") or {}).get("sha")
	body = (payload.get("body") or "").lower()

	if not title.startswith("feat") or not head_sha or "no-docs" in body or "backport" in body:
		return 0, "Skipping documentation checks... 🏃"

	if contains_documentation_link(body):
		return 0, "Documentation Link Found. You're Awesome! 🎉"

	return 1, "Documentation Link Not Found! ⚠️"
>>>>>>> 26ae0f3460 (fix: ruff fixes)


if __name__ == "__main__":
	pr = sys.argv[1]
	response = requests.get(f"https://api.github.com/repos/frappe/frappe/pulls/{pr}")

	if response.ok:
		payload = response.json()
		title = (payload.get("title") or "").lower()
		head_sha = (payload.get("head") or {}).get("sha")
		body = (payload.get("body") or "").lower()

		if title.startswith("feat") and head_sha and "no-docs" not in body:
			if docs_link_exists(body):
				print("Documentation Link Found. You're Awesome! 🎉")

			else:
				print("Documentation Link Not Found! ⚠️")
				sys.exit(1)

		else:
			print("Skipping documentation checks... 🏃")
