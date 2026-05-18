# install_claude.ps1 — Install thinking-essence-extraction for Claude Code (Windows)
param(
    [string]$Target = "."
)

$RepoUrl = "https://github.com/HuLi-12/thinking-essence-extraction"
$Branch = "master"
$Target = Resolve-Path $Target -ErrorAction Stop

Write-Host "Installing thinking-essence-extraction for Claude Code → $Target" -ForegroundColor Green

$claudeDir = "$Target\.claude\skills\thinking-essence-extraction"
New-Item -ItemType Directory -Force -Path "$claudeDir\docs" | Out-Null
New-Item -ItemType Directory -Force -Path "$claudeDir\examples" | Out-Null
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/.claude/skills/thinking-essence-extraction/SKILL.md" `
    -OutFile "$claudeDir\SKILL.md"
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/CLAUDE.md" -OutFile "$Target\CLAUDE.md"

@("variable_cards.md","anti_patterns.md","baseline_defect_taxonomy.md","module_cards.md","baseline_evolution_workflow.md") | ForEach-Object {
    Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/docs/$_" -OutFile "$claudeDir\docs\$_"
}
@("remote_sensing_segmentation_examples.md","engineering_design_examples.md","baseline_evolution_examples.md") | ForEach-Object {
    Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/examples/$_" -OutFile "$claudeDir\examples\$_"
}

Write-Host "Done. Test with: claude ""用本质变量抽取分析：1×1 卷积的本质是什么？""" -ForegroundColor Cyan
