<#
Instala o servidor pixel-mcp (MIT, github.com/willibrandon/pixel-mcp, de willibrandon) e o registra no Claude Code.
Uso: .\install-mcp.ps1 [-AsepritePath "C:\caminho\aseprite.exe"] [-Version v0.5.0]
Sem -AsepritePath ele detecta o Aseprite sozinho; se não achar, imprime ASEPRITE_NOT_FOUND e sai com código 2.
Requer: tar (incluído no Windows 10+), Aseprite 1.3.10+.
#>
param(
  [string]$AsepritePath = "",
  [string]$Version = "v0.5.0"
)
$ErrorActionPreference = "Stop"
if (-not $AsepritePath) { $AsepritePath = & (Join-Path $PSScriptRoot "find-aseprite.ps1") }
if (-not $AsepritePath -or -not (Test-Path $AsepritePath)) { Write-Host "ASEPRITE_NOT_FOUND"; exit 2 }

$ver = $Version.TrimStart("v")
$dir = Join-Path $HOME ".claude\mcp\pixel-mcp"
New-Item -ItemType Directory -Force $dir | Out-Null
$archive = "pixel-mcp_${ver}_Windows_x86_64.tar.gz"
$base = "https://github.com/willibrandon/pixel-mcp/releases/download/$Version"
Invoke-WebRequest "$base/$archive" -OutFile (Join-Path $dir $archive)
Invoke-WebRequest "$base/checksums.txt" -OutFile (Join-Path $dir "checksums.txt")

$expected = ((Get-Content (Join-Path $dir "checksums.txt") | Select-String $archive).Line -split "\s+")[0]
$actual = (Get-FileHash (Join-Path $dir $archive) -Algorithm SHA256).Hash
if ($expected.ToLower() -ne $actual.ToLower()) { throw "Checksum SHA-256 não confere para $archive" }

tar -xzf (Join-Path $dir $archive) -C $dir

$cfgDir = Join-Path $HOME ".config\pixel-mcp"
New-Item -ItemType Directory -Force $cfgDir | Out-Null
@{
  aseprite_path = (Resolve-Path $AsepritePath).Path
  temp_dir      = (Join-Path $env:TEMP "pixel-mcp")
  timeout       = 60
  log_level     = "info"
  log_file      = ""
  enable_timing = $false
} | ConvertTo-Json | Set-Content (Join-Path $cfgDir "config.json") -Encoding ascii

claude mcp add --scope user aseprite -- (Join-Path $dir "pixel-mcp.exe")
Write-Host "Pronto. Reinicie o cliente e rode: claude mcp list"
