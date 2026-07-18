import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

const canonical = readFileSync(new URL('../src/content/pi-openrouter-canonical.txt', import.meta.url), 'utf8').trim();
const page = readFileSync(new URL('../src/pages/quickstart.astro', import.meta.url), 'utf8');
const expectedHash = '13444e06d2b6f665d8badee2cb5add002f74059d61279df4455132d6741f6e03';
const actualHash = createHash('sha256').update(canonical).digest('hex');
if (actualHash !== expectedHash) {
  throw new Error(`Canonical quickstart drifted from graphwork/wg README: ${actualHash}`);
}

const commands = [
  'wg init',
  'wg pi-plugin install',
  'WG_MODEL="pi:openrouter:$MODEL"',
  'wg profile pi --strong "$WG_MODEL" --weak "$WG_MODEL"',
  'wg profile use pi --no-reload',
  'wg pi-plugin status',
  'wg profile show',
  'wg config --models',
  'wg service start',
  'wg service status',
  'wg tui',
];
for (const command of commands) {
  if (!canonical.includes(command)) throw new Error(`Canonical quickstart missing: ${command}`);
}

const required = [
  '@worksgood/pi',
  'pi-worksgood',
  'Sign in with an API',
  'Enter OpenRouter API key',
  'No model',
  'nvidia/nemotron-3-ultra-550b-a55b:free',
  'hermetic',
  '@worksgood/wg-pi-plugin',
  'pi-web-access@0.13.0',
  'agent-browser@0.32.2',
  'pi-agent-browser-native@0.2.70',
  'graph viewer',
  'wg service restart',
  'Failed to run wg',
  'id="path-or-the-wrong-wg-command"',
  'id="pi-is-missing"',
  'id="plugin-is-missing-stale-or-duplicated"',
  'id="model-is-absent-or-no-longer-free"',
  'id="openrouter-authentication-fails"',
];
for (const text of required) {
  if (!page.includes(text)) throw new Error(`Website quickstart missing: ${text}`);
}
console.log('Pi/OpenRouter website quickstart contract: pass');
