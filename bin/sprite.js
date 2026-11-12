#!/usr/bin/env node
// OmniSprite 🎮✨ — instalador no estilo do omni-rsm (menu interativo ou direto).

const fs = require('fs');
const path = require('path');
const os = require('os');
const { spawnSync } = require('child_process');
const prompts = require('prompts');

const CFG = {
  "name": "sprite",
  "pkg": "omni-sprite",
  "title": "OmniSprite 🎮✨",
  "display": "OmniSprite",
  "command": "/sprite",
  "doctor": "sprite",
  "mcp": true,
  "tagline": "Pixel art e animação no Aseprite guiadas por IA",
  "description": "Pixel art grande e detalhada e animações no Aseprite (/sprite)",
  "payload": [
    "SKILL.md",
    "references",
    "scripts"
  ],
  "companions": [
    "grill-me"
  ]
};
const ROOT = path.resolve(__dirname, '..');
const HOME = os.homedir();

const TARGET_OPTIONS = [
  { title: '🪐 Antigravity / Gemini CLI', value: 'antigravity', selected: true, description: `~/.gemini/config/skills/${CFG.name}` },
  { title: '🟣 Claude Code', value: 'claude', selected: true, description: `~/.claude/skills/${CFG.name}` },
  { title: '⚡ Cursor IDE', value: 'cursor', description: `.cursor/skills/${CFG.name} + .cursor/rules/${CFG.name}.mdc` },
  { title: '🌊 Windsurf', value: 'windsurf', description: `.windsurf/skills/${CFG.name} + .windsurfrules` },
  { title: '📁 Projeto Local', value: 'local', description: `./${CFG.name}/` }
];

function printHelp() {
  console.log(`
${CFG.title} — ${CFG.tagline}

Uso:
  npx ${CFG.pkg} install            Menu interativo com caixas de seleção
  npx ${CFG.pkg} install <destinos> Instalação direta (ex.: npx ${CFG.pkg} install claude antigravity)
${CFG.mcp ? `  npx ${CFG.pkg} mcp                Baixa/registra o servidor MCP do Aseprite (pixel-mcp)\n` : ''}  npx ${CFG.pkg} doctor             Diagnóstico do ambiente
  npx ${CFG.pkg} print              Imprime o SKILL.md no terminal
  npx ${CFG.pkg} info               Mostra destinos e comandos

Destinos:
  antigravity  ~/.gemini/config/skills/${CFG.name}/
  claude       ~/.claude/skills/${CFG.name}/
  cursor       .cursor/skills/${CFG.name}/ + regra .cursor/rules/${CFG.name}.mdc (pasta atual)
  windsurf     .windsurf/skills/${CFG.name}/ + ponteiro em .windsurfrules (pasta atual)
  local        ./${CFG.name}/ (pasta atual)
  all          todos os acima

Flags:
${CFG.mcp ? '  --mcp / --no-mcp   instala (ou não) o servidor MCP do Aseprite sem perguntar\n  --aseprite <caminho>  caminho do aseprite, se a detecção automática não achar\n' : ''}  --yes              não pergunta nada (usa o padrão)

Comando nos agentes: ${CFG.command}
`);
}

function skillsRoot(target) {
  switch (target) {
    case 'antigravity': case 'gemini': return path.join(HOME, '.gemini', 'config', 'skills');
    case 'claude': return path.join(HOME, '.claude', 'skills');
    case 'cursor': return path.join(process.cwd(), '.cursor', 'skills');
    case 'windsurf': return path.join(process.cwd(), '.windsurf', 'skills');
    case 'local': case '.': return process.cwd();
    default: return null;
  }
}

function copyPayload(destDir) {
  fs.mkdirSync(destDir, { recursive: true });
  for (const item of CFG.payload) {
    const src = path.join(ROOT, item);
    if (!fs.existsSync(src)) { console.error(`  ✗ Arquivo ausente no pacote: ${item}`); process.exit(1); }
    fs.cpSync(src, path.join(destDir, item), { recursive: true, force: true });
  }
}

function installCompanions(root) {
  for (const c of CFG.companions) {
    const dest = path.join(root, c);
    const src = path.join(ROOT, 'bundled', c);
    if (fs.existsSync(dest)) { console.log(`    · ${c} já instalada, mantendo a sua`); continue; }
    fs.cpSync(src, dest, { recursive: true });
    console.log(`    + ${c} (por Matt Pocock, MIT) instalada em: ${dest}`);
  }
}

function installToTarget(target) {
  const root = skillsRoot(target.toLowerCase());
  if (!root) { console.warn(`  ⚠ Destino desconhecido ignorado: ${target}`); return false; }
  const dest = path.join(root, CFG.name);
  copyPayload(dest);
  console.log(`  ✓ [${target}] Instalado em: ${dest}`);
  installCompanions(root);

  if (target === 'cursor') {
    const rules = path.join(process.cwd(), '.cursor', 'rules');
    fs.mkdirSync(rules, { recursive: true });
    fs.writeFileSync(path.join(rules, `${CFG.name}.mdc`),
      `---\ndescription: ${CFG.description}\nalwaysApply: false\n---\nQuando o usuário usar ${CFG.command} ou pedir algo desta área, siga as instruções de .cursor/skills/${CFG.name}/SKILL.md e carregue os arquivos de references/ sob demanda.\n`, 'utf8');
    console.log(`  ✓ [cursor] Regra criada em: .cursor/rules/${CFG.name}.mdc`);
  }
  if (target === 'windsurf') {
    const f = path.join(process.cwd(), '.windsurfrules');
    const marker = `# ${CFG.title}`;
    const cur = fs.existsSync(f) ? fs.readFileSync(f, 'utf8') : '';
    if (!cur.includes(marker)) {
      fs.appendFileSync(f, `\n\n${marker}\nQuando o usuário usar ${CFG.command} ou pedir algo desta área, siga as instruções de .windsurf/skills/${CFG.name}/SKILL.md.\n`, 'utf8');
    }
    console.log(`  ✓ [windsurf] Ponteiro adicionado em: ${f}`);
  }
  return true;
}

function runMcp(extra) {
  const dir = path.join(ROOT, 'scripts');
  let r;
  if (process.platform === 'win32') {
    const args = ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', path.join(dir, 'install-mcp.ps1')];
    if (extra.aseprite) args.push('-AsepritePath', extra.aseprite);
    r = spawnSync('powershell', args, { stdio: 'inherit' });
  } else {
    const args = [path.join(dir, 'install-mcp.sh')];
    if (extra.aseprite) args.push(extra.aseprite);
    r = spawnSync('bash', args, { stdio: 'inherit' });
  }
  if (r.status === 2) {
    console.log('\n  ⚠ Aseprite não encontrado. A skill continua instalada: no primeiro /sprite a IA pergunta se você quer que ela');
    console.log('    baixe o código do GitHub, compile e configure o Aseprite (ou rode de novo com --aseprite <caminho>).');
  } else if (r.status !== 0) {
    console.log(`\n  ⚠ A instalação do MCP terminou com código ${r.status}. Veja as mensagens acima.`);
  }
  return r.status;
}

function doctor() {
  console.log(`\n${CFG.title} — diagnóstico\n`);
  const node = process.versions.node;
  console.log(`  Node: ${node}`);
  if (CFG.doctor === 'sprite') {
    const dir = path.join(ROOT, 'scripts');
    const r = process.platform === 'win32'
      ? spawnSync('powershell', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', path.join(dir, 'find-aseprite.ps1')], { encoding: 'utf8' })
      : spawnSync('bash', [path.join(dir, 'find-aseprite.sh')], { encoding: 'utf8' });
    console.log(r.status === 0 ? `  Aseprite: ${r.stdout.trim()}` : '  Aseprite: não encontrado (a IA oferece compilar no primeiro /sprite)');
    const m = spawnSync('claude', ['mcp', 'list'], { encoding: 'utf8', shell: process.platform === 'win32' });
    if (m.error || m.status !== 0) console.log('  MCP: não foi possível consultar `claude mcp list` (Claude Code instalado?)');
    else console.log(/aseprite/i.test(m.stdout) ? '  MCP aseprite: registrado ✓' : '  MCP aseprite: NÃO registrado (rode: npx ' + CFG.pkg + ' mcp)');
  } else {
    const py = ['python', 'python3'].map(c => spawnSync(c, ['--version'], { encoding: 'utf8', shell: process.platform === 'win32' })).find(r => r.status === 0);
    console.log(py ? `  Python: ${(py.stdout || py.stderr).trim()} ✓` : '  Python 3: não encontrado (a IA oferece instalar quando precisar)');
  }
  for (const t of ['antigravity', 'claude']) {
    const p = path.join(skillsRoot(t), CFG.name, 'SKILL.md');
    console.log(`  ${t}: ${fs.existsSync(p) ? 'skill instalada ✓' : 'skill não instalada'}`);
  }
  console.log('');
}

async function main() {
  const args = process.argv.slice(2);
  const flags = { yes: args.includes('--yes'), mcp: args.includes('--mcp'), noMcp: args.includes('--no-mcp') };
  const ai = args.indexOf('--aseprite');
  const aseprite = ai >= 0 ? args[ai + 1] : '';
  const positional = args.filter((a, i) => !a.startsWith('--') && !(ai >= 0 && i === ai + 1));
  const command = positional[0] ? positional[0].toLowerCase() : 'install';

  if (['info', 'help', '--help', '-h'].includes(command) || args.includes('--help') || args.includes('-h')) { printHelp(); return; }
  if (command === 'doctor') { doctor(); return; }
  if (command === 'mcp' && CFG.mcp) { process.exit(runMcp({ aseprite }) || 0); }
  if (command === 'print') {
    const f = path.join(ROOT, 'SKILL.md');
    if (fs.existsSync(f)) process.stdout.write(fs.readFileSync(f, 'utf8')); else console.error('Erro: SKILL.md não encontrado.');
    return;
  }

  let targets = [];
  const names = TARGET_OPTIONS.map(o => o.value);
  if (command === 'install') {
    const raw = positional.slice(1);
    targets = raw.flatMap(t => t.toLowerCase() === 'all' ? names : t.toLowerCase().split(/[\s,]+/)).filter(Boolean);
  } else if (names.includes(command) || command === 'all') {
    targets = command === 'all' ? names : [command];
  } else {
    console.error(`Comando desconhecido: ${command}`); printHelp(); process.exit(1);
  }

  if (targets.length === 0) {
    if (flags.yes || !process.stdin.isTTY) {
      targets = ['claude'];
    } else {
      console.log(`\n${CFG.title} Installer`);
      const response = await prompts({
        type: 'multiselect', name: 'selected',
        message: `Em quais IAs você deseja instalar a ${CFG.display}?`,
        choices: TARGET_OPTIONS, hint: '- Espaço para marcar/desmarcar. Enter para confirmar', instructions: false
      }, { onCancel: () => { console.log('\nInstalação cancelada pelo usuário.'); process.exit(0); } });
      targets = response.selected || [];
      if (targets.length === 0) { console.log('Nenhuma IA selecionada. Usando Claude Code como padrão.'); targets = ['claude']; }
    }
  }

  console.log(`\nInstalando ${CFG.display} em [${targets.join(', ')}]...`);
  let ok = 0;
  for (const t of targets) if (installToTarget(t)) ok++;

  if (CFG.mcp && ok > 0 && !flags.noMcp) {
    let doMcp = flags.mcp;
    if (!flags.mcp && !flags.yes && process.stdin.isTTY) {
      const a = await prompts({ type: 'confirm', name: 'v', message: 'Instalar/registrar agora o servidor MCP do Aseprite (pixel-mcp)?', initial: true },
        { onCancel: () => process.exit(0) });
      doMcp = !!a.v;
    }
    if (doMcp) runMcp({ aseprite });
    else console.log(`\n  ℹ Para instalar o MCP depois: npx ${CFG.pkg} mcp`);
  }

  console.log(`\n🎉 ${CFG.display} configurada com sucesso! Utilize o comando ${CFG.command} em seus agentes.\n`);
}

main().catch(err => { console.error('Erro fatal:', err); process.exit(1); });
