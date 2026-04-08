# TinyTranslate Repo Cleanup Work Order For Claude

Date: 2026-04-08
Scope: Tracked repo state only
Final cleanup requirement: archive this document out of the repo root when the work is complete

## Primary Goal

Keep TinyTranslate clean, understandable, and release-friendly with:
- one root master document
- app code grouped clearly
- installer/config/model helper scripts organized cleanly
- screenshots/docs/assets separated from core logic

## Current Issues To Fix

1. The root mixes app code, installers, config, screenshots, assets, helper scripts, and docs.
2. The README is strong, but the repo structure should match that clarity.
3. The project needs a cleaner separation between core translation logic, installation/configuration, and presentation assets.
4. Changelog/docs/supporting material should not compete with the root as equal entrypoints.

## Work Order

### 1. Keep One Root Master Document
- Keep `README.md` as the main root-level document.
- Ensure it is the only top-level master guide and links to any deeper docs cleanly.

### 2. Clean The Root Layout
- Group files by responsibility where practical:
  - core app logic
  - installation/setup scripts
  - docs/changelog
  - screenshots/assets
  - tools/helpers
- Keep the root limited to the master document and essential entrypoints.

### 3. Clarify Config And Model Helper Surface
- Ensure config example files, actual config handling, and model download helpers are easy to distinguish.
- Move any support utilities that do not need root visibility into a tools or scripts folder.

### 4. Separate Presentation Assets From Source
- Keep screenshots and visual assets organized under dedicated folders.
- Ensure the root does not become a mix of source and marketing/demo material.

### 5. Reconcile Install And Uninstall Flow
- Audit install/uninstall scripts and settings entrypoints so the supported workflow is obvious.
- Archive any outdated or redundant support scripts if needed.

### 6. Add Maintenance Guardrails
- Add a lightweight repo policy covering:
  - one root master document
  - screenshots/assets separated from source
  - helper scripts grouped intentionally
  - root kept clean and product-focused

## Acceptance Criteria
- The root is cleaner and easier to scan.
- Source, assets, scripts, and docs are grouped clearly.
- The installation and settings workflow is obvious from the root doc.

## Final Deliverable
- short cleanup report with files moved, removed, rewritten, archived, and any unresolved structure decisions

## Archive Instruction
- When done, move this file out of the repo root into an archive/docs-history location.
