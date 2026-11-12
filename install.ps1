<#
Instalação em um comando: copia as skills para ~/.claude/skills e instala/registra o servidor MCP do Aseprite.
Uso: .\install.ps1 [-AsepritePath "C:\caminho\aseprite.exe"]
Se o Aseprite não for encontrado, as skills são instaladas mesmo assim; no primeiro uso a IA oferece compilá-lo do código-fonte.
#>
param([string]$AsepritePath = "")
$ErrorActionPreference = "Stop"
$dest = Join-Path $HOME ".claude\skills"
New-Item -ItemType Directory -Force $dest | Out-Null
foreach ($s in Get-ChildItem (Join-Path $PSScriptRoot "skills") -Directory) {
  $target = Join-Path $dest $s.Name
  if ($s.Name -eq "grill-me" -and (Test-Path $target)) { Write-Host "grill-me já instalada, pulando"; continue }
  Copy-Item -Recurse -Force $s.FullName $dest
  Write-Host "skill instalada: $($s.Name)"
}
$mcp = Join-Path $PSScriptRoot "skills\omni-sprite\scripts\install-mcp.ps1"
if ($AsepritePath) { & $mcp -AsepritePath $AsepritePath } else { & $mcp }
if ($LASTEXITCODE -eq 2) {
  Write-Host "Aseprite não encontrado. As skills estão instaladas. Peça um sprite à sua IA: ela oferecerá compilar o Aseprite do código-fonte,"
  Write-Host "ou instale o Aseprite você mesmo e rode de novo: .\install.ps1 -AsepritePath <caminho>"
}
