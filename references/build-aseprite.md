# Compilar o Aseprite do código-fonte

O Aseprite é *source-available* (EULA): compilar para uso próprio é permitido; redistribuir o binário compilado não. Comprá-lo (Steam, itch.io, aseprite.org) apoia o desenvolvedor e é a opção sem esforço.

## Automático
- Windows: `scripts/build-aseprite.ps1`
- Linux / macOS: `scripts/build-aseprite.sh`

Ambos clonam a tag estável `v1.3.*` mais recente com submódulos em `~/.aseprite-build/aseprite-src`, leem no `INSTALL.md` do próprio repositório a tag do **Skia** pré-compilado exigida, baixam essa versão, configuram com CMake/Ninja e compilam o alvo `aseprite`. Resultado: `~/.aseprite-build/build/bin/aseprite(.exe)`. Depois rode o `install-mcp`.

Situação: os scripts foram escritos a partir do procedimento documentado do Aseprite e não foram executados em todas as plataformas; se algum passo falhar, use o `INSTALL.md` do código clonado (ele é a autoridade).

## Pré-requisitos
| SO | Precisa de |
|---|---|
| Windows | git, CMake, Ninja, Visual Studio Build Tools com "Desenvolvimento para desktop com C++" (`winget install Git.Git Kitware.CMake Ninja-build.Ninja`; Build Tools pelo instalador do VS) |
| macOS | Ferramentas de linha de comando do Xcode, `brew install cmake ninja` |
| Linux | `sudo apt install -y g++ clang cmake ninja-build libx11-dev libxcursor-dev libxi-dev libgl1-mesa-dev libfontconfig1-dev` (confira a lista atual no INSTALL.md) |

Disco: ~3–5 GB. Tempo: 10–40 min.

## Falhas comuns
- *Submódulos vazios* → `git submodule update --init --recursive` na pasta do código.
- *Tag do Skia errada / erros de linkagem* → use exatamente a tag citada no `INSTALL.md`; versões diferentes falham na linkagem.
- *`cl.exe` / `ninja` não encontrados* → rode dentro do ambiente de desenvolvedor do VS (`VsDevCmd.bat -arch=x64`); o script já faz isso.
- *Cache de gerador do CMake incorreto* → apague a pasta `build` e rode de novo.
- *Antivírus em quarentena na saída* → libere a pasta de build.

## Depois de compilar
`scripts/find-aseprite.*` procura em `~/.aseprite-build/build/bin`, então o `install-mcp` o encontra sozinho. O Aseprite também precisa da pasta `data/` ao lado do executável (a compilação a gera).
