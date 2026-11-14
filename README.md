<a id="top"></a>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" alt="M Amirul. Firmware, kernels, and the automation that keeps them current. Auckland, New Zealand." width="100%">
</picture>

<p align="center">
  <a href="https://github.com/AmirulAndalib?tab=followers"><img src="https://img.shields.io/github/followers/AmirulAndalib?style=for-the-badge&label=followers&color=0969da&logo=github" alt="Followers"></a>
  <a href="https://github.com/AmirulAndalib?tab=repositories&type=source&sort=stargazers"><img src="https://img.shields.io/github/stars/AmirulAndalib?affiliations=OWNER&style=for-the-badge&label=stars&color=0969da&logo=github" alt="Stars across my repositories"></a>
  <img src="https://komarev.com/ghpvc/?username=AmirulAndalib&style=for-the-badge&color=0969da&label=profile+views" alt="Profile views">
  <a href="https://github.com/pulls?q=is%3Apr+author%3AAmirulAndalib+is%3Amerged+-user%3AAmirulAndalib"><img src="https://img.shields.io/badge/merged_upstream-openwrt%20%C2%B7%20winget--pkgs-34A853?style=for-the-badge&logo=git&logoColor=white" alt="Merged pull requests upstream"></a>
</p>

<p align="center">
  <a href="https://orcid.org/0009-0006-8898-2281"><img src="https://img.shields.io/badge/ORCID-0009--0006--8898--2281-A6CE39?style=flat-square&logo=orcid&logoColor=white" alt="ORCID"></a>
  <a href="https://wakatime.com/@AmirulAndalib"><img src="https://img.shields.io/badge/WakaTime-@AmirulAndalib-1f2328?style=flat-square&logo=wakatime&logoColor=white" alt="WakaTime"></a>
  <a href="https://steamcommunity.com/id/AmirulAndalib"><img src="https://img.shields.io/badge/Steam-AmirulAndalib-171a21?style=flat-square&logo=steam&logoColor=white" alt="Steam"></a>
  <a href="https://stackoverflow.com/users/15605896"><img src="https://img.shields.io/badge/Stack_Overflow-15605896-F58025?style=flat-square&logo=stackoverflow&logoColor=white" alt="Stack Overflow"></a>
  <img src="https://img.shields.io/badge/timezone-Pacific%2FAuckland-59636e?style=flat-square" alt="Timezone Pacific/Auckland">
</p>

I build, compile and tweak niche code. Most of what I ship is automation that keeps running
after I stop looking at it: a router that flashes its own firmware, a kernel that rebuilds the
moment upstream moves, and Windows packages that publish themselves every six hours.

<p align="center">
  <a href="#about">About</a> ·
  <a href="#toolbox">Toolbox</a> ·
  <a href="#current-work">Current work</a> ·
  <a href="#open-source-contributions">Upstream contributions</a> ·
  <a href="#earlier-projects">Earlier projects</a> ·
  <a href="#github-stats">GitHub stats</a> ·
  <a href="#activity">Activity</a> ·
  <a href="#how-this-profile-works">How this profile works</a>
</p>

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

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/skills-dark.svg">
    <img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/skills-light.svg" alt="Python, Bash, PowerShell, Docker, GitHub Actions, Git, Linux, Arch Linux, Windows, Android Studio, VS Code, Markdown" width="80%">
  </picture>
</p>

<p align="center">
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

## Open source contributions

Merged pull requests to projects I don't own.

| Project | Merged | What I contributed |
| --- | --- | --- |
| [openwrt/luci](https://github.com/openwrt/luci/pulls?q=is%3Apr+author%3AAmirulAndalib+is%3Amerged) | <img src="https://img.shields.io/github/issues-search?query=repo%3Aopenwrt%2Fluci%20author%3AAmirulAndalib%20is%3Apr%20is%3Amerged&label=merged&style=flat&color=34A853" alt="Merged PRs to openwrt/luci"> | Added the `luci-app-openspeedtest` package to the OpenWrt web interface |
| [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs/pulls?q=is%3Apr+author%3AAmirulAndalib) | <img src="https://img.shields.io/github/issues-search?query=repo%3Amicrosoft%2Fwinget-pkgs%20author%3AAmirulAndalib%20is%3Apr%20is%3Amerged&label=merged&style=flat&color=34A853" alt="Merged PRs to microsoft/winget-pkgs"> | Package manifests, including b00nz.mVolt releases |
| [yash-dk/TorToolkit-Telegram](https://github.com/yash-dk/TorToolkit-Telegram/pulls?q=is%3Apr+author%3AAmirulAndalib) | <img src="https://img.shields.io/github/issues-search?query=repo%3Ayash-dk%2FTorToolkit-Telegram%20author%3AAmirulAndalib%20is%3Apr%20is%3Amerged&label=merged&style=flat&color=34A853" alt="Merged PRs to TorToolkit-Telegram"> | Server and home page fixes for the upstream TorToolkit bot |
| Others | <img src="https://img.shields.io/github/issues-search?query=author%3AAmirulAndalib%20is%3Apr%20is%3Amerged%20-user%3AAmirulAndalib&label=merged%20in%20total&style=flat&color=34A853" alt="All merged upstream PRs"> | Docker build for MERGE-BOT, a compiler-flag fix for megasdkrest, a CI fix for slimhub_actions, and fixes to boibrary-astro |

<p align="right"><a href="#top">back to top</a></p>

## Earlier projects

| Project | What it does | Reach |
| --- | --- | --- |
| [TL-GD](https://github.com/AmirulAndalib/TL-GD) | Telegram bot that leeches torrents and direct links to Google Drive. A modified fork of TorrentLeech-Gdrive. | <img src="https://img.shields.io/github/stars/AmirulAndalib/TL-GD?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/TL-GD?style=flat&label=forks" alt="Forks"> |
| [Tor-Toolkit](https://github.com/AmirulAndalib/Tor-Toolkit) | Telegram torrent and youtube-dl leecher built on qBittorrent, adapted to run on Heroku. | <img src="https://img.shields.io/github/stars/AmirulAndalib/Tor-Toolkit?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/Tor-Toolkit?style=flat&label=forks" alt="Forks"> |
| [GdriveTools](https://github.com/AmirulAndalib/GdriveTools) | Python tool for Google Drive: creates service accounts, adds them to shared drives, and generates OAuth tokens. | <img src="https://img.shields.io/github/stars/AmirulAndalib/GdriveTools?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/GdriveTools?style=flat&label=forks" alt="Forks"> |
| [MLTB-ALPINE-DOCKER](https://github.com/AmirulAndalib/MLTB-ALPINE-DOCKER) | Alpine Edge Docker image for Mirror Leech Telegram Bot, built for amd64, arm64 and armv7. | <img src="https://img.shields.io/github/stars/AmirulAndalib/MLTB-ALPINE-DOCKER?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/MLTB-ALPINE-DOCKER?style=flat&label=forks" alt="Forks"> |
| [Scene7_ExtremeGT](https://github.com/AmirulAndalib/Scene7_ExtremeGT) | Unofficial Extreme GT Magisk module with power and thermal profiles for Samsung Exynos devices. | <img src="https://img.shields.io/github/stars/AmirulAndalib/Scene7_ExtremeGT?style=flat&label=stars" alt="Stars"> <img src="https://img.shields.io/github/forks/AmirulAndalib/Scene7_ExtremeGT?style=flat&label=forks" alt="Forks"> |

<details open>
<summary>Repository cards</summary>
<br>
<p align="center">
<a href="https://github.com/AmirulAndalib/gl-inet-mt6000-auto-snapshot"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-gl-inet-mt6000-auto-snapshot-dark.svg"><img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-gl-inet-mt6000-auto-snapshot-light.svg" alt="gl-inet-mt6000-auto-snapshot" width="49%"></picture></a>
<a href="https://github.com/AmirulAndalib/asus-nuc16pro-cachyos-server-edge-kernel"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-asus-nuc16pro-cachyos-server-edge-kernel-dark.svg"><img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-asus-nuc16pro-cachyos-server-edge-kernel-light.svg" alt="asus-nuc16pro-cachyos-server-edge-kernel" width="49%"></picture></a>
<a href="https://github.com/AmirulAndalib/nvpi-r-auto"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-nvpi-r-auto-dark.svg"><img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-nvpi-r-auto-light.svg" alt="nvpi-r-auto" width="49%"></picture></a>
<a href="https://github.com/AmirulAndalib/mvolt-scoop"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-mvolt-scoop-dark.svg"><img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-mvolt-scoop-light.svg" alt="mvolt-scoop" width="49%"></picture></a>
<a href="https://github.com/AmirulAndalib/TL-GD"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-TL-GD-dark.svg"><img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-TL-GD-light.svg" alt="TL-GD" width="49%"></picture></a>
<a href="https://github.com/AmirulAndalib/Tor-Toolkit"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-Tor-Toolkit-dark.svg"><img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-Tor-Toolkit-light.svg" alt="Tor-Toolkit" width="49%"></picture></a>
<a href="https://github.com/AmirulAndalib/GdriveTools"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-GdriveTools-dark.svg"><img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-GdriveTools-light.svg" alt="GdriveTools" width="49%"></picture></a>
<a href="https://github.com/AmirulAndalib/MLTB-ALPINE-DOCKER"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-MLTB-ALPINE-DOCKER-dark.svg"><img src="https://raw.githubusercontent.com/AmirulAndalib/AmirulAndalib/output/pin-MLTB-ALPINE-DOCKER-light.svg" alt="MLTB-ALPINE-DOCKER" width="49%"></picture></a>
</p>
</details>

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
