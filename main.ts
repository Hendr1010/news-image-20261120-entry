import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png not found next to main.ts");
}
copyFileSync(src, dst);
import { statSync } from "node:fs";
if (statSync(dst).size !== statSync(src).size) {
  throw new Error("copied entry.png differs in size from the source");
}
