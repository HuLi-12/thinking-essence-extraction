# install.ps1 — Full install (Codex + Claude) for Windows PowerShell
param(
    [string]$Target = "."
)

$RepoUrl = "https://github.com/HuLi-12/thinking-essence-extraction"
$Branch = "master"
$Target = Resolve-Path $Target -ErrorAction Stop

Write-Host "Installing thinking-essence-extraction skill to: $Target" -ForegroundColor Green

# --- Codex ---
Write-Host "[1/4] Installing Codex files..."
$codexDir = "$Target\.codex\skills\thinking-essence-extraction"
New-Item -ItemType Directory -Force -Path "$codexDir\docs" | Out-Null
New-Item -ItemType Directory -Force -Path "$codexDir\examples" | Out-Null
New-Item -ItemType Directory -Force -Path "$codexDir\evals" | Out-Null

Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/SKILL.md" -OutFile "$codexDir\SKILL.md"
@("variable_cards.md","anti_patterns.md","baseline_defect_taxonomy.md","module_cards.md","baseline_evolution_workflow.md") | ForEach-Object {
    Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/docs/$_" -OutFile "$codexDir\docs\$_"
}
@("remote_sensing_segmentation_examples.md","engineering_design_examples.md","baseline_evolution_examples.md") | ForEach-Object {
    Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/examples/$_" -OutFile "$codexDir\examples\$_"
}
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/evals/checkpoints.json" -OutFile "$codexDir\evals\checkpoints.json"
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/AGENTS.md" -OutFile "$Target\AGENTS.md"
Write-Host "  Codex files installed."

# --- Claude ---
Write-Host "[2/4] Installing Claude files..."
$claudeDir = "$Target\.claude\skills\thinking-essence-extraction"
New-Item -ItemType Directory -Force -Path $claudeDir | Out-Null
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/skills/thinking-essence-extraction/SKILL.md" `
    -OutFile "$claudeDir\SKILL.md"
Invoke-WebRequest -Uri "$RepoUrl/raw/$Branch/wrappers/claude/subagent.md" -OutFile "$Target\CLAUDE.md"
Write-Host "  Claude files installed."

# --- Verify ---
Write-Host "[3/4] Verifying installation..."
$missing = 0
@(
    "$codexDir\SKILL.md",
    "$claudeDir\SKILL.md",
    "$Target\AGENTS.md",
    "$Target\CLAUDE.md"
) | ForEach-Object {
    if (-not (Test-Path $_)) {
        Write-Host "  MISSING: $_" -ForegroundColor Red
        $missing++
    }
}
if ($missing -eq 0) {
    Write-Host "  All core files present." -ForegroundColor Green
}

# --- Summary ---
Write-Host "[4/4] Installation complete." -ForegroundColor Green
Write-Host ""
Write-Host "  Test with: claude ""用本质变量抽取分析：1×1 卷积的本质是什么？""" -ForegroundColor Cyan
if ($missing -gt 0) {
    Write-Host "  WARNING: $missing file(s) missing. Check network connection." -ForegroundColor Yellow
    exit 1
}
