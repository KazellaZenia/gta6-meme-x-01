// gta6-meme-x-01 entry (Node 22, standard library only).
//
// The entry is the X post itself: a GTA 6 meme posted from a public account
// with make.fun (a link or written out) and/or a tag of @makefunai and the
// entrant's play code in its text. POST.json names that post, and this program
// hands it to the gate: it reads POST.json, checks the url really is an X
// status link, and writes it to /output/POST.json, where the house reads it
// and fetches the post from X (its first picture and its text) for the judge.
// Nothing this program writes about the post is judged.
//
// The POST.json the kit starter ships holds a placeholder address, so the gate
// refuses it as it stands (valid 0). The post's real address goes in before
// submitting.
//
// Outside the grader's container, MAKEFUN_BOT_DIR and MAKEFUN_OUTPUT_DIR
// stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// An X status address: https://x.com/<handle>/status/<digits>.
// http is tolerated too, as is twitter.com (X still redirects it). A trailing
// slash, query string (?s=… tracking from Share) or fragment are accepted
// here and stripped when the address is canonicalised below.
const POST_URL = /^https?:\/\/(?:www\.)?(?:x\.com|twitter\.com)\/([A-Za-z0-9_]{1,15})\/status\/(\d+)(?:\/)?(?:[?#].*)?$/;

function fail(message: string): never {
  console.error(`gta6-meme-x-01: ${message}`);
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });

let raw: string;
try {
  raw = readFileSync(join(BOT_DIR, 'POST.json'), 'utf8');
} catch (err) {
  fail(`POST.json could not be read from ${BOT_DIR}: ${(err as Error).message}`);
}

let post: unknown;
try {
  post = JSON.parse(raw);
} catch (err) {
  fail(`POST.json is not valid JSON: ${(err as Error).message}`);
}

const url = (post as { url?: unknown } | null)?.url;
const match = typeof url === 'string' ? POST_URL.exec(url) : null;
if (match === null) {
  fail(
    'POST.json must name the entry post as {"url": "https://x.com/<handle>/status/<id>"}; ' +
      `got ${JSON.stringify(url)}. Replace the placeholder with the real post address before submitting.`,
  );
}

// Canonical form: x.com, no www, no query string or fragment, no trailing
// slash — so the address handed to the gate is the same no matter how the
// post link was copied (Share adds ?s=… and similar tracking).
const canonicalUrl = `https://x.com/${match[1]}/status/${match[2]}`;

try {
  writeFileSync(join(OUTPUT_DIR, 'POST.json'), JSON.stringify({ url: canonicalUrl }) + '\n', 'utf8');
} catch (err) {
  fail(`POST.json could not be written to ${OUTPUT_DIR}: ${(err as Error).message}`);
}

console.log(`post: ${canonicalUrl}`);
