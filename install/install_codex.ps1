# install_codex.ps1 — Install thinking-essence-extraction for Codex CLI (Windows)
param(
    [string]$Target = "."
)

$RepoUrl = "https://github.com/HuLi-12/thinking-essence-extraction"
$Branch = "master"
$Target = Resolve-Path $Target -ErrorAction Stop

Write-Host "Installing thinking-essence-extraction for Codex CLI → $Target" -ForegroundColor Green

$codexDir = "$Target\.codex\skills\thinking-essence-extraction"
New-Item -ItemType Directory -Force -Path "$codexDir\docs" | Out-Null
New-Item -ItemType Directory -Force -Path "$codexDir\examples" | Out-Null
New-Item -ItemType Directory -Force -Path "$codexDir\evals" | Out-Null

Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/skills/thinking-essence-extraction/SKILL.md" -OutFile "$codexDir\SKILL.md"
@("variable_cards.md","anti_patterns.md","baseline_defect_taxonomy.md","module_cards.md","baseline_evolution_workflow.md") | ForEach-Object {
    Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/skills/thinking-essence-extraction/docs/$_" -OutFile "$codexDir\docs\$_"
}
@("remote_sensing_segmentation_examples.md","engineering_design_examples.md","baseline_evolution_examples.md") | ForEach-Object {
    Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/skills/thinking-essence-extraction/examples/$_" -OutFile "$codexDir\examples\$_"
}
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/skills/thinking-essence-extraction/evals/checkpoints.json" -OutFile "$codexDir\evals\checkpoints.json"
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/wrappers/codex/AGENTS.md" -OutFile "$Target\AGENTS.md"

Write-Host "Done. Test with: codex ""用本质变量抽取分析：1×1 卷积的本质是什么？""" -ForegroundColor Cyan
