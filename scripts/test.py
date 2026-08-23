import os
import html
import requests
from collections import Counter

USERNAME = "Sweety-G"

API_HEADERS = {
    "Accept": "application/vnd.github+json"
}

GRAPHQL_URL = "https://api.github.com/graphql"


def get_profile():
    url = f"https://api.github.com/users/{USERNAME}"

    response = requests.get(url, headers=API_HEADERS)
    response.raise_for_status()

    return response.json()


def get_repositories():
    url = (
        f"https://api.github.com/users/{USERNAME}/repos"
        "?per_page=100&sort=updated"
    )

    response = requests.get(url, headers=API_HEADERS)
    response.raise_for_status()

    return response.json()


def get_contributions():
    token = os.environ.get("GH_TOKEN")

    if not token:
        print("GH_TOKEN not found. Contributions will be 0.")
        return 0, []

    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        GRAPHQL_URL,
        json={
            "query": query,
            "variables": {
                "login": USERNAME
            }
        },
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    calendar = data["data"]["user"]["contributionsCollection"][
        "contributionCalendar"
    ]

    total = calendar["totalContributions"]

    days = []

    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            days.append(day)

    return total, days


def get_languages(repositories):
    languages = Counter()

    for repo in repositories:
        language = repo.get("language")

        if language:
            languages[language] += 1

    return languages.most_common(5)


def create_svg(profile, repositories, contributions, contribution_days, languages):
    username = html.escape(profile["login"])

    repos = profile["public_repos"]
    followers = profile["followers"]
    following = profile["following"]

    total_stars = sum(
        repo.get("stargazers_count", 0)
        for repo in repositories
    )

    # -----------------------------
    # Contribution graph
    # -----------------------------

    graph = ""

    # GitHub contribution calendar normally contains 53 weeks.
    weeks = []

    current_week = []

    for day in contribution_days:
        current_week.append(day)

        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []

    if current_week:
        weeks.append(current_week)

    start_x = 40
    start_y = 365

    square_size = 12
    gap = 4

    for week_index, week in enumerate(weeks[-53:]):
        for day_index, day in enumerate(week):
            count = day["contributionCount"]

            if count == 0:
                fill = "#161b22"
            elif count <= 2:
                fill = "#0e4429"
            elif count <= 5:
                fill = "#006d32"
            elif count <= 10:
                fill = "#26a641"
            else:
                fill = "#39d353"

            x = start_x + week_index * (square_size + gap)
            y = start_y + day_index * (square_size + gap)

            graph += f"""
            <rect
                x="{x}"
                y="{y}"
                width="{square_size}"
                height="{square_size}"
                rx="2"
                fill="{fill}">
                <title>{day['date']}: {count} contributions</title>
            </rect>
            """

    # -----------------------------
    # Languages
    # -----------------------------

    language_text = ""

    for index, (language, count) in enumerate(languages):
        y = 175 + index * 25

        language_text += f"""
        <text
            x="390"
            y="{y}"
            fill="#c9d1d9"
            font-size="14"
            font-family="Arial">
            {html.escape(language)} ({count})
        </text>
        """

    if not language_text:
        language_text = """
        <text
            x="390"
            y="175"
            fill="#8b949e"
            font-size="14"
            font-family="Arial">
            No language data yet
        </text>
        """

    # -----------------------------
    # SVG
    # -----------------------------

    svg = f"""
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="900"
        height="500"
        viewBox="0 0 900 500">

        <rect
            width="900"
            height="500"
            rx="18"
            fill="#0d1117"
            stroke="#30363d"
            stroke-width="2"/>

        <!-- Header -->

        <text
            x="40"
            y="55"
            fill="#ffffff"
            font-size="32"
            font-family="Arial"
            font-weight="bold">
            {username}
        </text>

        <text
            x="40"
            y="82"
            fill="#8b949e"
            font-size="15"
            font-family="Arial">
            GitHub Profile • Automatically Generated
        </text>

        <!-- Stats -->

        <text
            x="40"
            y="125"
            fill="#8b949e"
            font-size="14"
            font-family="Arial">
            REPOSITORIES
        </text>

        <text
            x="40"
            y="150"
            fill="#ffffff"
            font-size="24"
            font-family="Arial"
            font-weight="bold">
            {repos}
        </text>

        <text
            x="180"
            y="125"
            fill="#8b949e"
            font-size="14"
            font-family="Arial">
            FOLLOWERS
        </text>

        <text
            x="180"
            y="150"
            fill="#ffffff"
            font-size="24"
            font-family="Arial"
            font-weight="bold">
            {followers}
        </text>

        <text
            x="300"
            y="125"
            fill="#8b949e"
            font-size="14"
            font-family="Arial">
            FOLLOWING
        </text>

        <text
            x="300"
            y="150"
            fill="#ffffff"
            font-size="24"
            font-family="Arial"
            font-weight="bold">
            {following}
        </text>

        <text
            x="520"
            y="125"
            fill="#8b949e"
            font-size="14"
            font-family="Arial">
            STARS
        </text>

        <text
            x="520"
            y="150"
            fill="#ffffff"
            font-size="24"
            font-family="Arial"
            font-weight="bold">
            {total_stars}
        </text>

        <text
            x="650"
            y="125"
            fill="#8b949e"
            font-size="14"
            font-family="Arial">
            CONTRIBUTIONS
        </text>

        <text
            x="650"
            y="150"
            fill="#ffffff"
            font-size="24"
            font-family="Arial"
            font-weight="bold">
            {contributions}
        </text>

        <!-- Languages -->

        <text
            x="390"
            y="170"
            fill="#ffffff"
            font-size="16"
            font-family="Arial"
            font-weight="bold">
            Top Languages
        </text>

        {language_text}

        <!-- Contribution graph -->

        <text
            x="40"
            y="330"
            fill="#ffffff"
            font-size="16"
            font-family="Arial"
            font-weight="bold">
            Contribution Activity
        </text>

        {graph}

        <text
            x="40"
            y="470"
            fill="#8b949e"
            font-size="13"
            font-family="Arial">
            Updated automatically by GitHub Actions
        </text>

    </svg>
    """

    return svg


def main():
    print("Getting GitHub profile...")

    profile = get_profile()

    print("Getting repositories...")

    repositories = get_repositories()

    print("Getting contribution data...")

    contributions, contribution_days = get_contributions()

    print("Calculating languages...")

    languages = get_languages(repositories)

    print("Generating SVG...")

    svg = create_svg(
        profile,
        repositories,
        contributions,
        contribution_days,
        languages
    )

    with open("profile.svg", "w", encoding="utf-8") as file:
        file.write(svg)

    print()
    print("Profile SVG created!")
    print(f"Repositories: {profile['public_repos']}")
    print(f"Followers: {profile['followers']}")
    print(f"Following: {profile['following']}")
    print(
        "Stars:",
        sum(repo.get("stargazers_count", 0) for repo in repositories)
    )
    print(f"Contributions: {contributions}")


if __name__ == "__main__":
    main()
