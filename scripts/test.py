import requests

# Get GitHub data
url = "https://api.github.com/users/Sweety-G"
response = requests.get(url)
data = response.json()

username = data["login"]
repos = data["public_repos"]
followers = data["followers"]

# Create SVG using the GitHub data
svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="150">
    <rect width="500" height="150" fill="white"/>

    <text x="30" y="45" font-size="28">
        {username}
    </text>

    <text x="30" y="85" font-size="20">
        Repositories: {repos}
    </text>

    <text x="30" y="120" font-size="20">
        Followers: {followers}
    </text>
</svg>
"""

# Save SVG
with open("profile.svg", "w") as file:
    file.write(svg)

print("Profile SVG created!")