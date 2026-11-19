// Round 2 entry validator for gta6-meme-x-01.
//
// Reads POST.json, checks the entry post URL is a real X status URL
// posted by @KazellaZeniaHQ, canonicalises it (https, x.com host,
// no query string or trailing junk) and prints it to stdout.
// Exits non-zero with a message on stderr if anything is off.

import { readFileSync } from "node:fs";

const ACCOUNT = "KazellaZeniaHQ";

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const raw = readFileSync(new URL("./POST.json", import.meta.url), "utf8");

let parsed: unknown;
try {
  parsed = JSON.parse(raw);
} catch {
  fail("POST.json is not valid JSON");
}

const url = (parsed as { url?: unknown }).url;
if (typeof url !== "string" || url.length === 0) {
  fail("POST.json has no string \"url\" field");
}

let u: URL;
try {
  u = new URL(url);
} catch {
  fail(`not a valid URL: ${url}`);
}

if (u.protocol !== "https:") fail(`URL must be https: ${url}`);
if (u.hostname !== "x.com") fail(`URL must be on x.com: ${url}`);

const match = u.pathname.match(/^\/([A-Za-z0-9_]+)\/status\/(\d+)\/?$/);
if (!match) fail(`URL is not an X status URL: ${url}`);
if (match[1] !== ACCOUNT) {
  fail(`status must be posted by @${ACCOUNT}, got @${match[1]}`);
}

const canonical = `https://x.com/${match[1]}/status/${match[2]}`;
console.log(canonical);
