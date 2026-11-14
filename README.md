<a id="top"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" alt="M Amirul. Firmware, kernels, and the automation that keeps them current. Auckland, New Zealand." width="100%">
</picture>

<p>
  <a href="https://github.com/AmirulAndalib?tab=followers"><img src="https://img.shields.io/github/followers/AmirulAndalib?style=flat&label=followers&color=0969da" alt="Followers"></a>
  <a href="https://github.com/AmirulAndalib?tab=repositories&type=source&sort=stargazers"><img src="https://img.shields.io/github/stars/AmirulAndalib?affiliations=OWNER&style=flat&label=stars&color=0969da" alt="Stars across my repositories"></a>
  <img src="https://komarev.com/ghpvc/?username=AmirulAndalib&style=flat&color=0969da&label=profile+views" alt="Profile views">
  <a href="https://github.com/AmirulAndalib/AmirulAndalib/actions/workflows/profile.yml"><img src="https://github.com/AmirulAndalib/AmirulAndalib/actions/workflows/profile.yml/badge.svg" alt="Profile cards workflow"></a>
  <img src="https://img.shields.io/badge/timezone-Pacific%2FAuckland-59636e?style=flat" alt="Timezone Pacific/Auckland">
</p>

I build, compile and tweak niche code. Most of what I ship is automation that keeps running
after I stop looking at it: a router that flashes its own firmware, a kernel that rebuilds the
moment upstream moves, and Windows packages that publish themselves every six hours.

**Contents:** [About](#about) · [Toolbox](#toolbox) · [Current work](#current-work) ·
[Earlier projects](#earlier-projects) · [GitHub stats](#github-stats) ·
[Activity](#activity) · [How this profile works](#how-this-profile-works)

## About

- **Working on:** keeping a GL.iNet Flint 2 on SNAPSHOT firmware without touching it, and a
  CachyOS server kernel tuned for an ASUS NUC 16 Pro.
- **Home lab:** OpenWrt-based router, an Arch-based server running a custom kernel with
  sched-ext schedulers, and Windows packages that update themselves.
- **Ask me about:** firmware update pipelines, kernel builds in CI, Telegram bots, packaging for
  WinGet and Scoop.
- **Earlier:** Telegram leech and mirror bots that were forked hundreds of times, Google Drive
  tooling, and an Android Magisk module for Exynos devices.

<p align="right"><a href="#top">back to top</a></p>

## Toolbox

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Shell-4EAA25?style=flat&logo=gnubash&logoColor=white" alt="Shell">
  <img src="https://img.shields.io/badge/PowerShell-012456?style=flat" alt="PowerShell">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat&logo=githubactions&logoColor=white" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/Arch_Linux-1793D1?style=flat&logo=archlinux&logoColor=white" alt="Arch Linux">
  <img src="https://img.shields.io/badge/Linux_kernel-FCC624?style=flat&logo=linux&logoColor=black" alt="Linux kernel">
  <img src="https://img.shields.io/badge/OpenWrt-00B5E2?style=flat&logo=openwrt&logoColor=white" alt="OpenWrt">
  <img src="https://img.shields.io/badge/Android-34A853?style=flat&logo=android&logoColor=white" alt="Android">
  <img src="https://img.shields.io/badge/Telegram_bots-26A5E4?style=flat&logo=telegram&logoColor=white" alt="Telegram bots">
  <img src="https://img.shields.io/badge/Google_Drive_API-4285F4?style=flat&logo=googledrive&logoColor=white" alt="Google Drive API">
  <img src="https://img.shields.io/badge/WinGet_%26_Scoop-0078D4?style=flat" alt="WinGet and Scoop">
  <img src="https://img.shields.io/badge/WakaTime-1f2328?style=flat&logo=wakatime&logoColor=white" alt="WakaTime">
  <img src="https://img.shields.io/badge/Claude_Code-D97757?style=flat&logo=claude&logoColor=white" alt="Claude Code">
</p>

<p align="right"><a href="#top">back to top</a></p>

## Current work

| Project | What it does | Status |
| --- | --- | --- |
| [gl-inet-mt6000-auto-snapshot](https://github.com/AmirulAndalib/gl-inet-mt6000-auto-snapshot) | Keeps a GL.iNet Flint 2 (GL-MT6000) on the latest SNAPSHOT firmware. Pure POSIX shell and AWK, checks SHA256 before every flash, and survives its own upgrades. | <img src="https://img.shields.io/github/stars/AmirulAndalib/gl-inet-mt6000-auto-snapshot?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/last-commit/AmirulAndalib/gl-inet-mt6000-auto-snapshot?style=flat&label=updated" alt="Last commit"> |
| [asus-nuc16pro-cachyos-server-edge-kernel](https://github.com/AmirulAndalib/asus-nuc16pro-cachyos-server-edge-kernel) | Builds the CachyOS server kernel and sched-ext schedulers for an ASUS NUC 16 Pro, and triggers a rebuild as soon as it drifts from upstream. | <img src="https://img.shields.io/github/v/release/AmirulAndalib/asus-nuc16pro-cachyos-server-edge-kernel?style=flat&label=release&display_name=release" alt="Latest release"> <img src="https://img.shields.io/github/last-commit/AmirulAndalib/asus-nuc16pro-cachyos-server-edge-kernel?style=flat&label=updated" alt="Last commit"> |
| [nvpi-r-auto](https://github.com/AmirulAndalib/nvpi-r-auto) | Unofficial WinGet and Scoop packaging for NVIDIA Profile Inspector and NVPI Revamped, checked for new releases every six hours. | <img src="https://github.com/AmirulAndalib/nvpi-r-auto/actions/workflows/update.yml/badge.svg" alt="Update workflow"> <img src="https://img.shields.io/github/last-commit/AmirulAndalib/nvpi-r-auto?style=flat&label=updated" alt="Last commit"> |
| [mvolt-scoop](https://github.com/AmirulAndalib/mvolt-scoop) | Unofficial Scoop bucket for mVolt+, the NVIDIA GPU tuning tool. | <img src="https://img.shields.io/github/last-commit/AmirulAndalib/mvolt-scoop?style=flat&label=updated" alt="Last commit"> |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/repos-dark.svg">
  <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/repos-light.svg" alt="My most recently updated repositories" width="49%">
</picture>

<p align="right"><a href="#top">back to top</a></p>

## Earlier projects

| Project | What it does | Reach |
| --- | --- | --- |
| [TL-GD](https://github.com/AmirulAndalib/TL-GD) | Telegram bot that leeches torrents and direct links to Google Drive. A modified fork of TorrentLeech-Gdrive. | <img src="https://img.shields.io/github/stars/AmirulAndalib/TL-GD?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/TL-GD?style=flat&label=forks" alt="Forks"> |
| [Tor-Toolkit](https://github.com/AmirulAndalib/Tor-Toolkit) | Telegram torrent and youtube-dl leecher built on qBittorrent, adapted to run on Heroku. | <img src="https://img.shields.io/github/stars/AmirulAndalib/Tor-Toolkit?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/Tor-Toolkit?style=flat&label=forks" alt="Forks"> |
| [GdriveTools](https://github.com/AmirulAndalib/GdriveTools) | Python tool for Google Drive: creates service accounts, adds them to shared drives, and generates OAuth tokens. | <img src="https://img.shields.io/github/stars/AmirulAndalib/GdriveTools?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/GdriveTools?style=flat&label=forks" alt="Forks"> |
| [MLTB-ALPINE-DOCKER](https://github.com/AmirulAndalib/MLTB-ALPINE-DOCKER) | Alpine Edge Docker image for Mirror Leech Telegram Bot, built for amd64, arm64 and armv7. | <img src="https://img.shields.io/github/stars/AmirulAndalib/MLTB-ALPINE-DOCKER?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/MLTB-ALPINE-DOCKER?style=flat&label=forks" alt="Forks"> |
| [Scene7_ExtremeGT](https://github.com/AmirulAndalib/Scene7_ExtremeGT) | Unofficial Extreme GT Magisk module with power and thermal profiles for Samsung Exynos devices. | <img src="https://img.shields.io/github/stars/AmirulAndalib/Scene7_ExtremeGT?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/Scene7_ExtremeGT?style=flat&label=forks" alt="Forks"> |

<details>
<summary>Star history of the bots and tools</summary>
<br>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/star-history-dark.svg">
  <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/star-history-light.svg" alt="Star history of TL-GD, Tor-Toolkit, GdriveTools and MLTB-ALPINE-DOCKER" width="100%">
</picture>
</details>

<p align="right"><a href="#top">back to top</a></p>

## GitHub stats

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/stats-dark.svg">
    <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/stats-light.svg" alt="GitHub stats: stars, commits, pull requests, issues and contributions" width="49%">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/languages-dark.svg">
    <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/languages-light.svg" alt="Most used languages across my repositories" width="49%">
  </picture>
</p>
<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/streak-dark.svg">
    <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/streak-light.svg" alt="Contribution streak" width="49%">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/productive-time-dark.svg">
    <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/productive-time-light.svg" alt="Commits by hour of day in New Zealand time" width="49%">
  </picture>
</p>
<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/repos-per-language-dark.svg">
    <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/repos-per-language-light.svg" alt="Top languages by repository" width="49%">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/commit-language-dark.svg">
    <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/commit-language-light.svg" alt="Top languages by commit" width="49%">
  </picture>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/trophy-dark.svg">
  <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/trophy-light.svg" alt="GitHub trophies" width="100%">
</picture>

<p align="right"><a href="#top">back to top</a></p>

## Activity

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/activity-dark.svg">
  <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/activity-light.svg" alt="Contributions per day over the last 90 days" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/contributions-3d-dark.svg">
  <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/contributions-3d-light.svg" alt="Contribution calendar for the last year in 3D" width="100%">
</picture>

<!-- Coding and gaming: enabled once the profile workflow can run with the WakaTime and Steam secrets.
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/wakatime-dark.svg">
  <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/wakatime-light.svg" alt="WakaTime coding time by language and editor" width="49%">
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/steam-dark.svg">
  <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/steam-light.svg" alt="Steam profile and games played in the last two weeks" width="49%">
</picture>
-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/snake-dark.svg">
  <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/snake-light.svg" alt="Snake eating my contribution graph" width="100%">
</picture>

<p align="right"><a href="#top">back to top</a></p>

## How this profile works

<details>
<summary>Every card here is rendered by my own workflow, not by a hosted service</summary>
<br>

Most profile cards you see on GitHub point at shared Vercel instances. In November 2026 those
returned HTTP 503 or 402, so this profile renders everything itself and commits the results to
the [output](https://github.com/AmirulAndalib/AmirulAndalib/tree/output) branch. A run that
produces a broken card fails instead of publishing it.

```mermaid
flowchart LR
  cron["profile.yml<br/>daily at 02:23 NZDT"] --> stats["github-stats<br/>stats, languages, streak"]
  cron --> graphs["contribution-graphs<br/>snake, 3D calendar, summary cards"]
  cron --> extras["extras<br/>trophies, activity graph, star history"]
  cron --> custom["custom-cards<br/>WakaTime, Steam, recent repos"]
  stats --> validate{"validate_cards.py<br/>XML, size, error text"}
  graphs --> validate
  extras --> validate
  custom --> validate
  validate -- all pass --> output[("output branch")]
  validate -- any fail --> stop["run fails,<br/>previous cards stay live"]
  output --> readme["README.md"]
```

All third-party actions are pinned to full commit SHAs. The WakaTime, Steam and recent-repos
cards come from small standard-library Python scripts in [scripts/cards](scripts/cards).

</details>

<sub>Rendered by [profile.yml](.github/workflows/profile.yml) · cards published to the
[output](https://github.com/AmirulAndalib/AmirulAndalib/tree/output) branch</sub>
