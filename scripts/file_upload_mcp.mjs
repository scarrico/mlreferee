#!/usr/bin/env node
/** Local stdio adapter: upload one configured UTF-8 file without model transcription.
 * Public integration code only. OAuth stays in the existing child MCP transport.
 */
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';
import { constants, openSync, fstatSync, readSync, closeSync } from 'node:fs';
import { isAbsolute } from 'node:path';
import { createInterface } from 'node:readline';
import { pathToFileURL } from 'node:url';

export const TOOL = 'upload_private_dataset_file';
export const MAX_BYTES = 1_000_000;

export function readUpload(file, expected) {
  if (!isAbsolute(file) || !/^[a-f0-9]{64}$/.test(expected ?? '')) {
    throw new Error('absolute_file_and_expected_sha256_required');
  }
  const fd = openSync(file, constants.O_RDONLY | constants.O_NOFOLLOW | constants.O_NONBLOCK);
  let raw;
  try {
    const stat = fstatSync(fd);
    if (!stat.isFile() || stat.size < 1 || stat.size > MAX_BYTES) {
      throw new Error('file_must_be_regular_and_within_size_limit');
    }
    // Bound the read even if another process grows the file after fstat.
    const buffer = Buffer.alloc(MAX_BYTES + 1);
    let length = 0, count;
    while (length < buffer.length &&
      (count = readSync(fd, buffer, length, buffer.length - length, null)) > 0) length += count;
    raw = buffer.subarray(0, length);
  } finally { closeSync(fd); }
  if (!raw.length || raw.length > MAX_BYTES) throw new Error('invalid_file_size');
  const sha256 = createHash('sha256').update(raw).digest('hex');
  if (sha256 !== expected) throw new Error('file_sha256_mismatch_no_upload');
  const data = raw.toString('utf8');
  if (!Buffer.from(data, 'utf8').equals(raw)) throw new Error('file_must_be_valid_utf8');
  return { data, sha256, bytes: raw.length };
}

export function localTool(file, format) {
  return {
    name: TOOL,
    description: `Upload the exact bytes of the owner-configured ${format.toUpperCase()} file ${file}. ` +
      'Requires explicit permission to upload this file. Reads only this configured file, ' +
      'checks the expected SHA-256 before transmitting, then uses the existing remote ' +
      'upload_private_dataset tool. Synthetic/non-personal, non-regulated beta data only. ' +
      'Does not submit an evaluation or spend Referee credits. Obtain preflight and a quote next. ' +
      'On an uncertain outcome stop; do not reconnect or create another upload to retry.',
    inputSchema: {
      type: 'object', additionalProperties: false,
      properties: {
        expected_sha256: { type: 'string', pattern: '^[a-f0-9]{64}$',
          description: 'SHA-256 computed locally from the original approved file.' },
        retention_seconds: { type: 'integer', minimum: 60, maximum: 86400, default: 86400 },
      },
      required: ['expected_sha256'],
    },
    annotations: { readOnlyHint: false, destructiveHint: false,
      idempotentHint: false, openWorldHint: true },
  };
}

function options(argv) {
  const separator = argv.indexOf('--');
  if (separator < 0) throw new Error('usage');
  const flags = argv.slice(0, separator);
  const command = argv.slice(separator + 1);
  if (flags.length !== 4 || flags[0] !== '--file' || flags[2] !== '--format' ||
      !isAbsolute(flags[1]) || !['csv', 'json'].includes(flags[3]) || !command.length) {
    throw new Error('usage');
  }
  return { file: flags[1], format: flags[3], command };
}

export function main(argv = process.argv.slice(2)) {
  let config;
  try { config = options(argv); }
  catch {
    process.stderr.write('Usage: node file_upload_mcp.mjs --file /absolute/input.csv --format csv -- command args...\n');
    process.exitCode = 1; return;
  }
  const { file, format, command } = config;
  const child = spawn(command[0], command.slice(1), { stdio: ['pipe', 'pipe', 'inherit'] });
  const lists = new Set();
  let remoteUploadAvailable = false, attempt = null;
  const emit = message => process.stdout.write(JSON.stringify(message) + '\n');
  const forward = message => child.stdin.write(JSON.stringify(message) + '\n');
  const failure = (id, code) => emit({ jsonrpc: '2.0', id, result: {
    isError: true, content: [{ type: 'text', text: code }],
  } });
  const input = createInterface({ input: process.stdin, crlfDelay: Infinity });
  input.on('line', line => {
    let message;
    try { message = JSON.parse(line); }
    catch { process.stderr.write('Invalid local MCP JSON.\n'); return; }
    if (message.method === 'tools/list') lists.add(message.id);
    if (message.method !== 'tools/call' || message.params?.name !== TOOL) {
      forward(message); return;
    }
    if (!remoteUploadAvailable) { failure(message.id, 'remote_upload_tool_not_discovered'); return; }
    const args = message.params.arguments ?? {};
    const retention = args.retention_seconds ?? 86400;
    if (Object.keys(args).some(k => !['expected_sha256', 'retention_seconds'].includes(k)) ||
        !Number.isInteger(retention) || retention < 60 || retention > 86400) {
      failure(message.id, 'invalid_file_upload_arguments'); return;
    }
    if (attempt) {
      if (attempt.result && attempt.sha256 === args.expected_sha256 && attempt.retention === retention) {
        emit({ jsonrpc: '2.0', id: message.id, result: attempt.result });
      } else failure(message.id, 'upload_already_attempted_do_not_retry_or_reconnect');
      return;
    }
    let snapshot;
    try { snapshot = readUpload(file, args.expected_sha256); }
    catch (error) {
      const known = ['absolute_file_and_expected_sha256_required', 'file_sha256_mismatch_no_upload',
        'file_must_be_valid_utf8', 'invalid_file_size', 'file_must_be_regular_and_within_size_limit'];
      failure(message.id, known.includes(error.message) ? error.message : 'cannot_read_configured_file');
      return;
    }
    attempt = { id: message.id, sha256: snapshot.sha256, bytes: snapshot.bytes, retention };
    forward({ ...message, params: { ...message.params, name: 'upload_private_dataset',
      arguments: { data: snapshot.data, format, retention_seconds: retention } } });
  });
  createInterface({ input: child.stdout, crlfDelay: Infinity }).on('line', line => {
    let message;
    try { message = JSON.parse(line); }
    catch { process.stderr.write('Invalid child MCP JSON; stopping.\n'); child.kill(); return; }
    if (!message.method && lists.delete(message.id) && message.result?.tools) {
      if (message.result.tools.some(t => t.name === 'upload_private_dataset')) {
        remoteUploadAvailable = true;
        message.result.tools.push(localTool(file, format));
      }
    }
    if (attempt && message.id === attempt.id && !message.method) {
      if (message.result && !message.result.isError) {
        let body = message.result.structuredContent;
        if (!body) {
          try { body = JSON.parse(message.result.content?.find(c => c.type === 'text')?.text); }
          catch { /* Missing evidence is an error, never a success claim. */ }
        }
        const manifest = body?.input_manifest?.manifest;
        const match = manifest?.sha256 === attempt.sha256 && manifest?.bytes === attempt.bytes;
        const evidence = { local_file_verification: { sha256: attempt.sha256,
          bytes: attempt.bytes, server_manifest_match: match } };
        // Some clients prefer structuredContent and omit additional text blocks.
        // Keep this explicitly local evidence visible in both representations.
        if (body && typeof body === 'object' && !Array.isArray(body)) {
          message.result.structuredContent = { ...body, ...evidence };
        }
        message.result.content = [...(message.result.content ?? []),
          { type: 'text', text: JSON.stringify(evidence) }];
        if (!match) {
          message.result.isError = true;
          message.result.content.push({ type: 'text',
            text: 'upload_returned_without_matching_manifest_stop_do_not_retry' });
        }
        attempt.result = message.result;
      }
    }
    emit(message);
  });
  input.on('close', () => child.stdin.end());
  child.stdin.on('error', () => { process.stderr.write('MCP transport closed; upload outcome may be unknown.\n'); });
  child.on('error', () => { process.stderr.write('Cannot start configured MCP transport.\n'); process.exitCode = 1; input.close(); });
  child.on('exit', code => { process.exitCode = code ?? 1; input.close(); process.stdin.destroy(); });
  for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => child.kill(signal));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main();
