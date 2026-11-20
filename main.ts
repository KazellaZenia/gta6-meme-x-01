// Round 3 entry program for gta6-meme-x-01.
//
// The entry itself is a post on X, so this program's only job is to
// carry that post's address from POST.json into the output directory:
// it reads the file, makes sure it names a real X status posted by
// @KazellaZeniaHQ, writes the canonical form to <output>/POST.json
// and prints it.
//
// Run it from the repo root, e.g.:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HANDLE = "KazellaZeniaHQ";

function die(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const here = dirname(fileURLToPath(import.meta.url));
const postPath = join(here, "POST.json");

let doc: unknown;
try {
  doc = JSON.parse(readFileSync(postPath, "utf8"));
} catch {
  die("POST.json is not valid JSON");
}

const rawUrl = (doc as { url?: unknown }).url;
if (typeof rawUrl !== "string" || rawUrl.length === 0) {
  die('POST.json has no string "url" field');
}

let parsed: URL;
try {
  parsed = new URL(rawUrl);
} catch {
  die(`not a valid URL: ${rawUrl}`);
}

if (parsed.protocol !== "https:") die(`URL must use https: ${rawUrl}`);
if (parsed.hostname !== "x.com") die(`URL must be on x.com: ${rawUrl}`);

const parts = parsed.pathname.match(/^\/([A-Za-z0-9_]+)\/status\/(\d+)\/?$/);
if (!parts) die(`URL is not an X status URL: ${rawUrl}`);
if (parts[1] !== HANDLE) {
  die(`status must be posted by @${HANDLE}, got @${parts[1]}`);
}

const canonical = `https://x.com/${parts[1]}/status/${parts[2]}`;
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out");
mkdirSync(outDir, { recursive: true });
const outPath = join(outDir, "POST.json");
writeFileSync(outPath, `${JSON.stringify({ url: canonical })}\n`);
// Re-read what was written: the copy must round-trip exactly, so a
// half-written file can never pass as a good entry.
const written = JSON.parse(readFileSync(outPath, "utf8")) as { url?: unknown };
if (written.url !== canonical) die(`wrote ${outPath} but it does not hold ${canonical}`);
console.log(canonical);
