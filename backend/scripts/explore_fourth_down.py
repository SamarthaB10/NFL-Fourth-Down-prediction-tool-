import argparse

from app.services.data_cleaning import clean_fourth_down_plays
from app.services.pbp_cache import load_pbp_from_cache


def main():
    parser = argparse.ArgumentParser(description="Explore cached fourth-down EPA data.")
    parser.add_argument("--season", type=int, default=2025)
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch missing PBP data from nflreadpy and write it to the local cache.",
    )
    args = parser.parse_args()

    pbp = load_pbp_from_cache(args.season, allow_fetch=args.fetch)
    clean_plays = clean_fourth_down_plays(pbp)

    punt_epa = round(clean_plays[clean_plays["decision"] == "punt"]["epa"].mean(), 2)
    go_epa = round(clean_plays[clean_plays["decision"] == "go"]["epa"].mean(), 2)
    field_goal_epa = round(clean_plays[clean_plays["decision"] == "field_goal"]["epa"].mean(), 2)
    print("Season: ", args.season)
    print("Statistics\n")
    print("Punt: count", (clean_plays["decision"] == "punt").sum(), "Average epa: ", punt_epa)
    print("Go: count", (clean_plays["decision"] == "go").sum(), "Average epa: ", go_epa)
    print(
        "Field_goal: count",
        (clean_plays["decision"] == "field_goal").sum(),
        "Average epa:",
        field_goal_epa,
    )


if __name__ == "__main__":
    main()
