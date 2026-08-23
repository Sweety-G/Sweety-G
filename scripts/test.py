import requests

USERNAME = "Sweety-G"

url = f"https://api.github.com/users/{USERNAME}"

response = requests.get(url)
response.raise_for_status()

data = response.json()

print("GitHub profile found!")
print("Username:", data["login"])
print("Repositories:", data["public_repos"])
print("Followers:", data["followers"])
print("Following:", data["following"])
