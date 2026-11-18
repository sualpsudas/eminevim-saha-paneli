import { cp, mkdir, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const output = resolve(root, "www");
const runtimeFiles = [
  "index.html",
  "Eminevim Saha Paneli.dc.html",
  "manifest.json",
  "sw.js",
  "eminevim-qr.png",
  "merkez/takip.html"
];
// Klasörler bütünüyle kopyalanır: uygulama/ (kapılar ve yardımcılar), harita/, assets/, vendor/ ve veri/'nin uygulamaya giden dosyaları
const runtimeDirs = ["uygulama", "harita", "assets", "vendor"];
const veriFiles = ["veri/spyler.js", "veri/org-data.js"];

await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });

for (const file of runtimeFiles) {
  const source = resolve(root, file);
  if (!existsSync(source)) throw new Error(`Eksik web dosyası: ${file}`);
  await cp(source, resolve(output, file));
}

for (const dir of runtimeDirs) await cp(resolve(root, dir), resolve(output, dir), { recursive: true });
await mkdir(resolve(output, "veri"), { recursive: true });
for (const file of veriFiles) await cp(resolve(root, file), resolve(output, file));
console.log(`Native web paketi hazır: ${output}`);
