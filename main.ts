// Front page for Friday 20 November 2026.
//
// The page is drawn by draw.py (Pillow) into entry.png; this program only
// places that finished image where the grader expects it, /output/entry.png.
// It runs with no network and no dependencies beyond the Node standard library.
// The image is copied byte for byte, so the output is exactly the page.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, 'entry.png'));
writeFileSync(join(outDir, 'entry.png'), bytes);
