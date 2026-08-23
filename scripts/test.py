import requests

username = "Sweety-G"

# Get profile information
profile_url = f"https://api.github.com/users/{username}"
profile_response = requests.get(profile_url)
profile_data = profile_response.json()

repos = profile_data["public_repos"]
followers = profile_data["followers"]
following = profile_data["following"]

# Get repositories to calculate total stars
repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
repos_response = requests.get(repos_url)
repositories = repos_response.json()

total_stars = 0

for repo in repositories:
    total_stars += repo["stargazers_count"]

# Create SVG
svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="600" height="260">
    <rect width="600" height="260" rx="15" fill="white"/>

    <text x="40" y="55" font-size="32" font-family="Arial">
        {username}
    </text>

    <text x="40" y="105" font-size="22" font-family="Arial">
        Repositories: {repos}
    </text>

    <text x="40" y="145" font-size="22" font-family="Arial">
        Followers: {followers}
    </text>

    <text x="40" y="185" font-size="22" font-family="Arial">
        Following: {following}
    </text>

    <text x="40" y="225" font-size="22" font-family="Arial">
        Stars: {total_stars}
    </text>
</svg>
"""

# Save the SVG
with open("profile.svg", "w") as file:
    file.write(svg)

print("Profile stats generated!")
print(f"Repositories: {repos}")
print(f"Followers: {followers}")
print(f"Following: {following}")
print(f"Stars: {total_stars}")