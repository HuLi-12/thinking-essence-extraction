# install_claude.ps1 — Install thinking-essence-extraction for Claude Code (Windows)
param(
    [string]$Target = "."
)

$RepoUrl = "https://github.com/<your-org>/thinking-essence-extraction"
$Branch = "main"
$Target = Resolve-Path $Target -ErrorAction Stop

Write-Host "Installing thinking-essence-extraction for Claude Code → $Target" -ForegroundColor Green

$claudeDir = "$Target\.claude\skills\thinking-essence-extraction"
New-Item -ItemType Directory -Force -Path $claudeDir | Out-Null
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/.claude/skills/thinking-essence-extraction/SKILL.md" `
    -OutFile "$claudeDir\SKILL.md"
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/CLAUDE.md" -OutFile "$Target\CLAUDE.md"

Write-Host "Done. Test with: claude ""用本质变量抽取分析：1×1 卷积的本质是什么？""" -ForegroundColor Cyan
