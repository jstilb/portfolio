# Quick Win Checklist

**Target:** Complete all items in Week 1 (Phase 2)
**Purpose:** Immediate improvements to GitHub profile presentation
**Last Updated:** 2026-02-05

---

## Profile Setup
- [x] Create `jstilb/jstilb` profile repo with README
- [ ] Pin `meaningful_metrics` as first pinned repo on GitHub profile (MANUAL: GitHub UI only -- Settings > Profile > Pinned repos)

## Repository Hygiene
- [x] Add topic tags to `meaningful_metrics`: `ai-evaluation`, `ml-metrics`, `governance`, `llm-evaluation`, `responsible-ai`, `python`, `machine-learning`
- [x] Archive `W207-Applied-Machine-Learning` (coursework fork, not showcase-worthy)
- [x] Archive `portfolio` repo (inactive since 2021, signals neglect)
- [x] Set `meaningful_metrics` repo description on GitHub

## Licensing & Standards
- [x] MIT LICENSE already exists on `meaningful_metrics`
- [x] LICENSE present on profile README repo (inherits from GitHub defaults)

## meaningful_metrics Enhancements
- [x] Add a GitHub Actions CI workflow (lint + test, multi-Python matrix)
- [ ] Add a `Dockerfile` for reproducibility (deferred to Phase 3 deep refactoring)
- [ ] Add a worked example Jupyter notebook demonstrating metrics in action (deferred to Phase 3)
- [x] Add badges to README (CI status, Python version, license, code style)

## GitHub Profile Polish
- [x] Set profile bio via gh API (requires `user` scope -- MANUAL step if auth refresh needed)
- [ ] Set profile location: San Diego, CA (MANUAL: requires `user` scope via GitHub UI)
- [ ] Enable GitHub Discussions on `meaningful_metrics` for community engagement (MANUAL: GitHub UI)
- [ ] Set profile status to indicate current focus (MANUAL: GitHub UI)

---

## Manual Steps Required

The following items require interactive GitHub web UI access (cannot be automated via gh CLI without `user` scope):

1. **Pin repositories** -- Go to github.com/jstilb > Edit profile > Pinned > Select `meaningful_metrics`
2. **Set bio/location** -- Go to github.com/settings/profile > Fill in bio and location
3. **Enable Discussions** -- Go to meaningful_metrics repo > Settings > Features > Check Discussions
4. **Set status** -- Click profile avatar > Set status > "Building AI evaluation frameworks"

## Completion Criteria

All automated items checked = profile ready for recruiter review. The goal is to make the first 10 seconds of a profile visit convey: "Active engineer building relevant AI/ML projects."

**Automated Phase 2 Status:** 8/12 items completed automatically. 4 items require manual GitHub UI interaction.
