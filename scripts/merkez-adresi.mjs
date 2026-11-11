// TestFlight test sürümü: uygulama paketteki kopyayı değil, merkez sunucusundaki canlı sayfayı açar.
// Adres gizli yol içerdiği için depoda tutulmaz; Codemagic'te TY_MERKEZ_URL değişkeninden derleme anında yazılır.
// Değişken yoksa capacitor.config.json'a dokunulmaz ve uygulama paketteki gösteri sürümüyle açılır.
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const adres = (process.env.TY_MERKEZ_URL || "").trim();
if (!adres) {
  console.log("TY_MERKEZ_URL yok: uygulama paketteki gösteri sürümüyle derlenecek.");
  process.exit(0);
}
const url = new URL(adres);
if (url.protocol !== "https:") throw new Error("TY_MERKEZ_URL https ile başlamalı.");
if (!url.pathname.endsWith("/")) url.pathname += "/";

const dosya = resolve(import.meta.dirname, "..", "capacitor.config.json");
const ayar = JSON.parse(await readFile(dosya, "utf8"));
ayar.server = { ...(ayar.server || {}), url: url.href + "Eminevim%20Saha%20Paneli.dc.html?native=1", cleartext: false };
await writeFile(dosya, JSON.stringify(ayar, null, 2) + "\n");
console.log(`Merkez adresi yazıldı: ${url.host} (yol gizli)`);
