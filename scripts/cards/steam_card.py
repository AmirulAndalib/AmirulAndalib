"""Render the Steam card from the Steam Web API.

Reads STEAM_API_KEY and STEAM_ID (a 17-digit SteamID64 or a custom profile URL name) and
writes steam-light.svg and steam-dark.svg.
"""

from __future__ import annotations

import os
import re
import sys
import urllib.parse
from pathlib import Path

from common import (
    PAD,
    WIDTH,
    CardError,
    Palette,
    card,
    data_uri,
    divider,
    fmt_duration,
    get_json,
    text,
    truncate,
    write_cards,
)

API = "https://api.steampowered.com"
CAPSULE = "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/{appid}/capsule_184x69.jpg"
RECENT_ROWS = 4
ROW = 46


def _call(path: str, key: str, **params: str) -> dict:
    query = urllib.parse.urlencode({"key": key, "format": "json", **params})
    return get_json(f"{API}/{path}/?{query}")


def resolve_steam_id(key: str, value: str) -> str:
    if re.fullmatch(r"\d{17}", value):
        return value
    response = _call("ISteamUser/ResolveVanityURL/v1", key, vanityurl=value)["response"]
    if response.get("success") != 1:
        raise CardError(
            f"STEAM_ID '{value}' is neither a SteamID64 nor a known custom profile URL name"
        )
    return response["steamid"]


def fetch(key: str, steam_id: str) -> dict:
    players = _call("ISteamUser/GetPlayerSummaries/v2", key, steamids=steam_id)[
        "response"
    ].get("players", [])
    if not players:
        raise CardError(f"Steam returned no profile for {steam_id}")
    player = players[0]
    if player.get("communityvisibilitystate") != 3:
        raise CardError(
            "the Steam profile is private; set Profile and Game details to Public"
        )

    owned = _call(
        "IPlayerService/GetOwnedGames/v1",
        key,
        steamid=steam_id,
        include_played_free_games="1",
    )["response"]
    if "game_count" not in owned:
        raise CardError(
            "Steam hides the game library; set Game details to Public in Steam privacy settings"
        )
    recent = _call("IPlayerService/GetRecentlyPlayedGames/v1", key, steamid=steam_id)[
        "response"
    ]
    level = _call("IPlayerService/GetSteamLevel/v1", key, steamid=steam_id)[
        "response"
    ].get("player_level")

    games = recent.get("games", [])[:RECENT_ROWS]
    for game in games:
        game["image"] = data_uri(CAPSULE.format(appid=game["appid"]))
    return {
        "name": player.get("personaname", "Steam"),
        "avatar": data_uri(player["avatarmedium"])
        if player.get("avatarmedium")
        else None,
        "in_game": player.get("gameextrainfo"),
        "level": level,
        "game_count": owned.get("game_count", 0),
        "minutes_total": sum(
            game.get("playtime_forever", 0) for game in owned.get("games", [])
        ),
        "recent": games,
    }


def render(profile: dict, palette: Palette) -> str:
    defs = '<clipPath id="avatar"><circle cx="48" cy="44" r="24"/></clipPath><clipPath id="capsule">'
    defs += "".join(
        f'<rect x="{PAD}" y="{130 + index * ROW}" width="92" height="34" rx="4"/>'
        for index in range(RECENT_ROWS)
    )
    defs += "</clipPath>"

    body = []
    if profile["avatar"]:
        body.append(
            f'<image href="{profile["avatar"]}" x="24" y="20" width="48" height="48" clip-path="url(#avatar)"/>'
        )
    else:
        body.append(f'<circle cx="48" cy="44" r="24" fill="{palette.track}"/>')
    body.append(
        text(
            88, 40, truncate(profile["name"], 32), size=15, weight=600, fill=palette.fg
        )
    )

    facts = [
        f"{profile['game_count']:,} games",
        f"{fmt_duration(profile['minutes_total'] * 60)} on record",
    ]
    if profile["level"] is not None:
        facts.insert(0, f"Level {profile['level']}")
    body.append(text(88, 60, " · ".join(facts), size=12, fill=palette.muted))
    if profile["in_game"]:
        body.append(
            text(
                WIDTH - PAD,
                40,
                "In game",
                size=12,
                weight=600,
                fill=palette.accent,
                anchor="end",
            )
        )
        body.append(
            text(
                WIDTH - PAD,
                60,
                truncate(profile["in_game"], 26),
                size=12,
                fill=palette.muted,
                anchor="end",
            )
        )
    body.append(divider(88, palette))
    body.append(
        text(PAD, 114, "Last two weeks", size=12, weight=600, fill=palette.muted)
    )

    if not profile["recent"]:
        body.append(
            text(PAD, 140, "No games played in the last two weeks.", fill=palette.muted)
        )
        return card(162, "Steam profile", "".join(body), palette, defs)

    for index, game in enumerate(profile["recent"]):
        top = 130 + index * ROW
        if game.get("image"):
            body.append(
                f'<image href="{game["image"]}" x="{PAD}" y="{top}" width="92" height="34" '
                f'preserveAspectRatio="xMidYMid slice" clip-path="url(#capsule)"/>'
            )
        else:
            body.append(
                f'<rect x="{PAD}" y="{top}" width="92" height="34" rx="4" fill="{palette.track}"/>'
            )
        recent = fmt_duration(game.get("playtime_2weeks", 0) * 60)
        total = fmt_duration(game.get("playtime_forever", 0) * 60)
        body.append(
            text(
                130,
                top + 14,
                truncate(game.get("name", "Unknown title"), 40),
                fill=palette.fg,
            )
        )
        body.append(
            text(
                130,
                top + 31,
                f"{recent} in two weeks · {total} total",
                size=12,
                fill=palette.muted,
            )
        )
    height = 130 + len(profile["recent"]) * ROW + 10
    return card(height, "Steam profile", "".join(body), palette, defs)


def main() -> int:
    key = os.environ.get("STEAM_API_KEY", "").strip()
    steam_id = os.environ.get("STEAM_ID", "").strip()
    if not key or not steam_id:
        print("error: STEAM_API_KEY and STEAM_ID must both be set", file=sys.stderr)
        return 1
    out_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    try:
        profile = fetch(key, resolve_steam_id(key, steam_id))
    except CardError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    write_cards("steam", lambda palette: render(profile, palette), out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
