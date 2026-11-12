<# Imprime o caminho de um executável do Aseprite e sai com 0; sai com 2 (sem imprimir nada) se não achar. #>
$c = @()
if ($env:ASEPRITE_PATH) { $c += $env:ASEPRITE_PATH }
$cmd = Get-Command aseprite -ErrorAction SilentlyContinue; if ($cmd) { $c += $cmd.Source }
$c += @(
  "${env:ProgramFiles(x86)}\Steam\steamapps\common\Aseprite\Aseprite.exe",
  "$env:ProgramFiles\Steam\steamapps\common\Aseprite\Aseprite.exe",
  "$env:ProgramFiles\Aseprite\Aseprite.exe",
  "${env:ProgramFiles(x86)}\Aseprite\Aseprite.exe",
  "$HOME\Aseprite\Aseprite.exe",
  "$HOME\.aseprite-build\build\bin\aseprite.exe"   # output of build-aseprite.ps1
)
$found = $c | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if ($found) { (Resolve-Path $found).Path; exit 0 }
exit 2
