import os
import urllib.request
import json
from datetime import datetime, timedelta


USERNAME = os.environ.get("GH_LOGIN", "Sweety-G")
TOKEN = os.environ.get("GITHUB_TOKEN")


def github_graphql(query, variables):
    data = json.dumps({
        "query": query,
        "variables": variables
    }).encode("utf-8")

    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=data,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def get_contributions():
    today = datetime.utcnow().date()

    start = today - timedelta(days=364)

    from_date = f"{start}T00:00:00Z"
    to_date = f"{today}T23:59:59Z"

    query = """
    query($login: String!, $from: DateTime!, $to: DateTime!) {
      user(login: $login) {
        contributionsCollection(
          from: $from
          to: $to
        ) {
          totalCommitContributions
          totalPullRequestContributions
          totalIssueContributions
          totalPullRequestReviewContributions

          contributionCalendar {
            totalContributions

            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """

    result = github_graphql(
        query,
        {
            "login": USERNAME,
            "from": from_date,
            "to": to_date
        }
    )

    return result["data"]["user"]["contributionsCollection"]


def flatten_days(calendar):
    days = []

    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            days.append(day)

    return days


def calculate_streak(days):
    counts = {
        day["date"]: day["contributionCount"]
        for day in days
    }

    dates = sorted(counts.keys(), reverse=True)

    current = 0

    for date in dates:
        if counts[date] > 0:
            current += 1
        else:
            break

    longest = 0
    running = 0

    for date in sorted(counts.keys()):
        if counts[date] > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0

    return current, longest


def write_svg(filename, title, value, subtitle):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="860"
height="180"
viewBox="0 0 860 180">

<rect
width="860"
height="180"
rx="14"
fill="#0d1117"
stroke="#30363d"/>

<text
x="40"
y="55"
fill="#8b949e"
font-family="monospace"
font-size="15">
{title}
</text>

<text
x="40"
y="105"
fill="#ffffff"
font-family="monospace"
font-size="38"
font-weight="bold">
{value}
</text>

<text
x="40"
y="140"
fill="#8b949e"
font-family="monospace"
font-size="14">
{subtitle}
</text>

</svg>"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(svg)


def main():
    contributions = get_contributions()

    calendar = contributions["contributionCalendar"]

    total = calendar["totalContributions"]

    days = flatten_days(calendar)

    current, longest = calculate_streak(days)

    write_svg(
        "stats.svg",
        "GITHUB ACTIVITY",
        str(total),
        "contributions in the last year"
    )

    write_svg(
        "streak.svg",
        "STREAK",
        str(current),
        f"current streak · longest: {longest}"
    )

    write_svg(
        "langs.svg",
        "LANGUAGES",
        "software",
        "AI / ML · full stack · cloud · research"
    )

    write_svg(
        "year.svg",
        "YEAR",
        str(total),
        "contribution activity"
    )

    print("Profile graphics generated successfully.")


if __name__ == "__main__":
    main()
