"""Test that config.toml hero params are consistent with published post dates."""
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_trip_date_range_year_matches_posts():
    """tripDateRange year should match the year of published posts."""
    config_path = ROOT / "config.toml"
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    # Load all post dates
    posts_dir = ROOT / "content" / "posts"
    post_dates = []
    for md in posts_dir.glob("*.md"):
        text = md.read_text()
        m = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
        if m:
            post_dates.append(m.group(1))

    assert post_dates, "No post dates found"
    post_year = int(post_dates[0][:4])

    # Parse year from tripDateRange — format is 'D.–M.YYYY' or 'D.–D.M.YYYY'
    range_str = config["params"]["tripDateRange"]
    # Match the last .YYYY part
    m = re.search(r"\.(\d{4})\s*['\"]?$", range_str)
    assert m, f"tripDateRange '{range_str}' could not find year"
    range_year = int(m.group(1))

    assert range_year == post_year, (
        f"tripDateRange year {range_year} doesn't match post year {post_year}"
    )


def test_hero_subtitle_mentions_trip_country():
    """heroSubtitle should mention Japan when posts are from Japan (Shibuya/Tokyo)."""
    config_path = ROOT / "config.toml"
    with open(config_path, "rb") as f:
        config = tomllib.load(f)

    hero_subtitle = config["params"]["heroSubtitle"].lower()
    posts_dir = ROOT / "content" / "posts"

    japan_posted = any(
        "japan" in f.stem.lower() or "shibuya" in f.stem.lower() or "tokio" in f.stem.lower()
        for f in posts_dir.glob("*.md")
    )

    if japan_posted:
        assert "japan" in hero_subtitle, (
            f"Posts appear to be from Japan but heroSubtitle "
            f"'{config['params']['heroSubtitle']}' does not mention Japan"
        )
