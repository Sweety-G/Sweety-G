import requests
from datetime import datetime, timedelta

username = "Sweety-G"

# GitHub API
headers = {
    "Accept": "application/vnd.github+json"
}

# Get profile information
profile_url = f"https://api.github.com/users/{username}"
profile_response = requests.get(profile_url, headers=headers)
profile_data = profile_response.json()

repos = profile_data["public_repos"]
followers = profile_data["followers"]
following = profile_data["following"]

# Get repositories
repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
repos_response = requests.get(repos_url, headers=headers)
repositories = repos_response.json()

# Calculate total stars
total_stars = 0

for repo in repositories:
    total_stars += repo["stargazers_count"]

# Get contribution count
today = datetime.utcnow().date()
one_year_ago = today - timedelta(days=365)

events_url = f"https://api.github.com/users/{username}/events/public?per_page=100"
events_response = requests.get(events_url, headers=headers)
events = events_response.json()

contributions = 0

for event in events:
    event_date = event["created_at"][:10]

    if event_date >= str(one_year_ago):
        if event["type"] in [
            "PushEvent",
            "PullRequestEvent",
            "IssuesEvent",
            "IssueCommentEvent",
            "CreateEvent"
        ]:
            contributions += 1

# Create SVG
svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="650" height="320">
    <rect width="650" height="320" rx="15" fill="white"/>

    <text x="40" y="55"
          font-size="32"
          font-family="Arial">
        {username}
    </text>

    <text x="40" y="105"
          font-size="22"
          font-family="Arial">
        Repositories: {repos}
    </text>

    <text x="40" y="145"
          font-size="22"
          font-family="Arial">
        Followers: {followers}
    </text>

    <text x="40" y="185"
          font-size="22"
          font-family="Arial">
        Following: {following}
    </text>

    <text x="40" y="225"
          font-size="22"
          font-family="Arial">
        Stars: {total_stars}
    </text>

    <text x="40" y="265"
          font-size="22"
          font-family="Arial">
        Contributions: {contributions}
    </text>
</svg>
"""

with open("profile.svg", "w") as file:
    file.write(svg)

print("Profile stats generated!")
print(f"Repositories: {repos}")
print(f"Followers: {followers}")
print(f"Following: {following}")
print(f"Stars: {total_stars}")
print(f"Contributions: {contributions}")
