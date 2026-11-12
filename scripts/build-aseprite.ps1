<#
Builds Aseprite from source (Windows). Output: $HOME\.aseprite-build\build\bin\aseprite.exe
Requires: git, CMake, Ninja, Visual Studio 2022+ Build Tools with the "Desktop development with C++" workload.
Aseprite is source-available (EULA): build for your own use; do not redistribute the binary.
Usage: .\build-aseprite.ps1 [-Tag v1.3.x] [-Root "$HOME\.aseprite-build"]
#>
param([string]$Tag = "", [string]$Root = "$HOME\.aseprite-build")
$ErrorActionPreference = "Stop"
foreach ($n in "git", "cmake", "ninja") {
  if (-not (Get-Command $n -ErrorAction SilentlyContinue)) {
    throw "Missing tool: $n. Install with: winget install Git.Git Kitware.CMake Ninja-build.Ninja"
  }
}
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
if (-not (Test-Path $vswhere)) {
  throw "Visual Studio Build Tools not found. Install: winget install Microsoft.VisualStudio.2022.BuildTools --override '--add Microsoft.VisualStudio.Workload.VCTools --includeRecommended --passive'"
}
$vs = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if (-not $vs) { throw "C++ build tools workload missing in Visual Studio." }

New-Item -ItemType Directory -Force $Root | Out-Null
$src = Join-Path $Root "aseprite-src"; $build = Join-Path $Root "build"; $skia = Join-Path $Root "deps\skia"

if (-not $Tag) {  # newest stable v1.3.* tag
  $Tag = git ls-remote --tags --refs https://github.com/aseprite/aseprite.git "v1.3.*" |
    ForEach-Object { ($_ -split "refs/tags/")[1] } |
    Where-Object { $_ -match '^v1\.3\.\d+(\.\d+)?$' } |
    Sort-Object { [version]($_.TrimStart('v')) } | Select-Object -Last 1
}
Write-Host "Aseprite tag: $Tag"
if (-not (Test-Path $src)) { git clone --recursive --depth 1 --branch $Tag https://github.com/aseprite/aseprite.git $src }

# Skia: the prebuilt tag required by this Aseprite version is written in INSTALL.md
$install = Get-Content (Join-Path $src "INSTALL.md") -Raw
$skiaTag = [regex]::Match($install, 'aseprite/skia/releases/tag/(m\d+-[0-9a-f]+)').Groups[1].Value
if (-not $skiaTag) {
  throw "Could not read the Skia tag from INSTALL.md; download Skia-Windows-Release-x64.zip from github.com/aseprite/skia/releases into $skia manually."
}
if (-not (Test-Path "$skia\out\Release-x64\skia.lib")) {
  New-Item -ItemType Directory -Force $skia | Out-Null
  $zip = Join-Path $Root "skia.zip"
  Invoke-WebRequest "https://github.com/aseprite/skia/releases/download/$skiaTag/Skia-Windows-Release-x64.zip" -OutFile $zip
  Expand-Archive $zip -DestinationPath $skia -Force; Remove-Item $zip
}

# Configure + build inside the Visual Studio developer environment
$bat = Join-Path $Root "_build.bat"
$lines = @(
  "@echo off",
  "call `"$vs\Common7\Tools\VsDevCmd.bat`" -arch=x64 || exit /b 1",
  "if not exist `"$build`" mkdir `"$build`"",
  "cd /d `"$build`"",
  "cmake -DCMAKE_BUILD_TYPE=Release -DLAF_BACKEND=skia -DSKIA_DIR=`"$skia`" -DSKIA_LIBRARY_DIR=`"$skia\out\Release-x64`" -DSKIA_LIBRARY=`"$skia\out\Release-x64\skia.lib`" -G Ninja `"$src`" || exit /b 1",
  "ninja aseprite || exit /b 1"
)
Set-Content $bat $lines -Encoding ascii
cmd /c $bat
if ($LASTEXITCODE -ne 0) { throw "Build failed (see output above)." }
$exe = Join-Path $build "bin\aseprite.exe"
if (-not (Test-Path $exe)) { throw "Build finished but $exe was not found." }
Write-Host "OK: $exe"
