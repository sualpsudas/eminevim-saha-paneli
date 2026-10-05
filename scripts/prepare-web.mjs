import { cp, mkdir, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const output = resolve(root, "www");
const runtimeFiles = [
  "index.html",
  "Eminevim Saha Paneli.dc.html",
  "assignment.js",
  "org-data.js",
  "support.js",
  "map.html",
  "manifest.json",
  "sw.js",
  "eminevim-qr.png"
];

await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });

for (const file of runtimeFiles) {
  const source = resolve(root, file);
  if (!existsSync(source)) throw new Error(`Eksik web dosyası: ${file}`);
  await cp(source, resolve(output, file));
}

await cp(resolve(root, "assets"), resolve(output, "assets"), { recursive: true });
await cp(resolve(root, "vendor"), resolve(output, "vendor"), { recursive: true });
console.log(`Native web paketi hazır: ${output}`);
