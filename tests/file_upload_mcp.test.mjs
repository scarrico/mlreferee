/** Offline transport tests: no OAuth, network, service calls or credits. */
import test from 'node:test';
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { mkdtempSync, writeFileSync, symlinkSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
import { readUpload, TOOL } from '../scripts/file_upload_mcp.mjs';

const digest = raw => createHash('sha256').update(raw).digest('hex');
const adapter = fileURLToPath(new URL('../scripts/file_upload_mcp.mjs', import.meta.url));
const fake = `
const {createInterface}=require('node:readline');
const {createHash}=require('node:crypto');let uploads=0;
createInterface({input:process.stdin}).on('line',line=>{
 const m=JSON.parse(line);if(m.id===undefined)return;
 let result;
 if(m.method==='tools/list') result={tools:[{name:'upload_private_dataset',inputSchema:{type:'object'}}]};
 else if(m.method==='tools/call'&&m.params.name==='upload_private_dataset'){
   uploads++; const a=m.params.arguments;const bytes=Buffer.from(a.data,'utf8');
   const sha256=process.env.TEST_BAD_MANIFEST?'0'.repeat(64):createHash('sha256').update(bytes).digest('hex');
   const body={upload_id:'synthetic-offline-only',input_manifest:{manifest:{sha256,bytes:bytes.length}},retention_seconds:a.retention_seconds};
   result={content:[{type:'text',text:JSON.stringify(body)}],structuredContent:body};
 }else result={uploads};
 process.stdout.write(JSON.stringify({jsonrpc:'2.0',id:m.id,result})+'\\n');
});`;

function connection(t, file, badManifest = false) {
  const child = spawn(process.execPath, [adapter, '--file', file, '--format', 'csv', '--',
    process.execPath, '-e', fake], { env: { ...process.env, TEST_BAD_MANIFEST: badManifest ? '1' : '' } });
  let id = 0;
  const pending = new Map();
  createInterface({ input: child.stdout }).on('line', line => {
    const m = JSON.parse(line); const resolve = pending.get(m.id);
    if (resolve) { pending.delete(m.id); resolve(m.result); }
  });
  t.after(() => { child.stdin.end(); child.kill(); });
  return (method, params) => new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('offline RPC timeout')), 3000);
    pending.set(++id, result => { clearTimeout(timer); resolve(result); });
    child.stdin.write(JSON.stringify({ jsonrpc: '2.0', id, method, params }) + '\n');
  });
}

test('exact UTF-8 bytes include CRLF, BOM and final newline; reject wrong hashes and invalid UTF-8', t => {
  const directory = mkdtempSync(join(tmpdir(), 'mlreferee-file-test-'));
  t.after(() => rmSync(directory, { recursive: true }));
  const file = join(directory, 'synthetic.csv');
  const raw = Buffer.from('\uFEFFsynthetic,café\r\n1,2\r\n', 'utf8');
  writeFileSync(file, raw);
  assert.deepEqual(readUpload(file, digest(raw)), { data: raw.toString('utf8'), sha256: digest(raw), bytes: raw.length });
  assert.throws(() => readUpload(file, '0'.repeat(64)), /sha256_mismatch/);
  writeFileSync(file, Buffer.from([255]));
  assert.throws(() => readUpload(file, digest(Buffer.from([255]))), /valid_utf8/);
  const link = join(directory, 'link.csv'); symlinkSync(file, link);
  assert.throws(() => readUpload(link, digest(Buffer.from([255]))));
});

test('proxy forwards original file bytes, checks server manifest, and reuses completed result', async t => {
  const directory = mkdtempSync(join(tmpdir(), 'mlreferee-file-test-'));
  t.after(() => rmSync(directory, { recursive: true }));
  const file = join(directory, 'synthetic.csv');
  const raw = Buffer.from('synthetic,café\r\n1,2\r\n'); writeFileSync(file, raw);
  const rpc = connection(t, file);
  const tools = await rpc('tools/list', {});
  assert.equal(tools.tools.some(tool => tool.name === TOOL), true);
  const bad = await rpc('tools/call', { name: TOOL, arguments: { expected_sha256: '0'.repeat(64) } });
  assert.equal(bad.isError, true);
  assert.equal((await rpc('offline/count', {})).uploads, 0);
  const args = { expected_sha256: digest(raw), retention_seconds: 86400 };
  const result = await rpc('tools/call', { name: TOOL, arguments: args });
  assert.notEqual(result.isError, true);
  assert.deepEqual(result.structuredContent.input_manifest.manifest, { sha256: digest(raw), bytes: raw.length });
  assert.equal(JSON.parse(result.content.at(-1).text).local_file_verification.server_manifest_match, true);
  assert.equal(result.structuredContent.local_file_verification.server_manifest_match, true);
  const repeated = await rpc('tools/call', { name: TOOL, arguments: args });
  assert.deepEqual(repeated, result);
  assert.equal((await rpc('offline/count', {})).uploads, 1);
});

test('missing or mismatched server evidence fails and arbitrary file arguments cannot redirect reads', async t => {
  const directory = mkdtempSync(join(tmpdir(), 'mlreferee-file-test-'));
  t.after(() => rmSync(directory, { recursive: true }));
  const file = join(directory, 'synthetic.csv'); const raw = Buffer.from('synthetic\n'); writeFileSync(file, raw);
  const rpc = connection(t, file, true); await rpc('tools/list', {});
  const changed = await rpc('tools/call', { name: TOOL,
    arguments: { expected_sha256: digest(raw), file: '/not-allowed.csv' } });
  assert.equal(changed.isError, true);
  assert.equal((await rpc('offline/count', {})).uploads, 0);
  const result = await rpc('tools/call', { name: TOOL, arguments: { expected_sha256: digest(raw) } });
  assert.equal(result.isError, true);
  assert.equal(JSON.parse(result.content.at(-2).text).local_file_verification.server_manifest_match, false);
  assert.equal((await rpc('offline/count', {})).uploads, 1);
});
