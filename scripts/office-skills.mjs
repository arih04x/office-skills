#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const COMMANDS = {
  help: "Show available commands",
  validate: "Run repository structure and metadata validation",
  "smoke:syntax": "Check Python and Node script syntax",
  "smoke:image": "Run safe mock image generation smoke test",
  smoke: "Run validate + smoke:syntax + smoke:image",
  install: "Link skill collection into agent skill discovery path",
  "pack:check": "Verify npm pack contents exclude secrets and generated output",
};

// --- Utilities ---

function resolvePython() {
  for (const cmd of ["python", "python3"]) {
    const r = spawnSync(cmd, ["--version"], { stdio: "pipe", shell: true });
    if (r.status === 0) return cmd;
  }
  if (process.platform === "win32") {
    const r = spawnSync("py", ["-3", "--version"], { stdio: "pipe", shell: true });
    if (r.status === 0) return "py -3";
  }
  return null;
}

function run(cmd, args, opts = {}) {
  const result = spawnSync(cmd, args, {
    cwd: opts.cwd || ROOT,
    stdio: "inherit",
    shell: true,
    ...opts,
  });
  return result.status || 0;
}

function die(msg) {
  console.error(`ERROR: ${msg}`);
  process.exit(1);
}

// --- Commands ---

async function cmdHelp() {
  console.log("\noffice-skills - CLI for the Office Skills collection\n");
  console.log("Usage: office-skills <command> [options]\n");
  console.log("Commands:");
  for (const [name, desc] of Object.entries(COMMANDS)) {
    console.log(`  ${name.padEnd(16)} ${desc}`);
  }
  console.log("\nExamples:");
  console.log("  npx office-skills validate");
  console.log("  npx office-skills smoke");
  console.log("  npx office-skills install --dry-run");
  console.log("");
}

async function cmdValidate() {
  const py = resolvePython();
  if (!py) die("Python not found. Install Python 3.11+ and ensure it is on PATH.");
  const script = path.join(ROOT, ".claude/skills/office-skills-review/scripts/validate_skills.py");
  if (!fs.existsSync(script)) die(`Validator not found: ${script}`);
  const code = run(py, [script], { cwd: ROOT });
  if (code !== 0) die("Validation failed.");
  return code;
}

async function cmdSmokeSyntax() {
  const py = resolvePython();
  if (!py) die("Python not found.");

  const pyScripts = [
    "office-pdf/scripts/pdf_toolkit.py",
    "office-figure/scripts/render-tikz.py",
    "office-motion/scripts/motion_toolkit.py",
  ].filter((s) => fs.existsSync(path.join(ROOT, s)));

  if (pyScripts.length > 0) {
    console.log("Checking Python syntax...");
    const code = run(py, ["-m", "py_compile", ...pyScripts]);
    if (code !== 0) die("Python syntax check failed.");
  }

  const nodeScripts = [
    "office-ppt/assets/node-starter/create-onij-slide.mjs",
    "office-figure/assets/node-image-starter/generate-style-image.mjs",
  ].filter((s) => fs.existsSync(path.join(ROOT, s)));

  for (const s of nodeScripts) {
    console.log(`Checking ${s}...`);
    const code = run("node", ["--check", s]);
    if (code !== 0) die(`Node syntax check failed: ${s}`);
  }

  console.log("Syntax checks passed.");
  return 0;
}

async function cmdSmokeImage() {
  const outDir = path.join(ROOT, "out/smoke-image");
  await fsp.mkdir(outDir, { recursive: true });

  const figureScript = path.join(ROOT, "office-figure/assets/node-image-starter/generate-style-image.mjs");
  const figureOut = path.join(outDir, "figure-mock.png");
  console.log("Running figure image mock...");
  const c1 = run("node", [figureScript, "--mock", "--out", figureOut]);
  if (c1 !== 0) die("Figure mock image smoke failed.");

  const pptScript = path.join(ROOT, "office-ppt/assets/node-starter/create-onij-slide.mjs");
  const pptOutDir = path.join(outDir, "ppt");
  const pptNodeModules = path.join(ROOT, "office-ppt/assets/node-starter/node_modules");
  if (!fs.existsSync(pptNodeModules)) {
    console.log("Installing PPT starter dependencies...");
    run("npm", ["install"], { cwd: path.join(ROOT, "office-ppt/assets/node-starter") });
  }
  console.log("Running PPT mock slide...");
  const c2 = run("node", [pptScript, "--mock", "--out-dir", pptOutDir]);
  if (c2 !== 0) die("PPT mock slide smoke failed.");

  console.log(`Smoke image outputs: ${outDir}`);
  return 0;
}

async function cmdSmoke() {
  await cmdValidate();
  await cmdSmokeSyntax();
  await cmdSmokeImage();
  console.log("\nAll smoke tests passed.");
}

async function cmdInstall() {
  const args = process.argv.slice(3);
  const dryRun = args.includes("--dry-run");
  const force = args.includes("--force");
  const targetIdx = args.indexOf("--target");
  const defaultTarget = path.join(os.homedir(), ".agents/skills/office-skills");
  const target = targetIdx >= 0 && args[targetIdx + 1] ? path.resolve(args[targetIdx + 1]) : defaultTarget;

  console.log(`Source:  ${ROOT}`);
  console.log(`Target:  ${target}`);

  if (fs.existsSync(target)) {
    if (!force) {
      die(`Target already exists: ${target}\nUse --force to overwrite.`);
    }
    if (!dryRun) {
      await fsp.rm(target, { recursive: true, force: true });
      console.log("Removed existing target.");
    } else {
      console.log("[dry-run] Would remove existing target.");
    }
  }

  const parentDir = path.dirname(target);
  if (!dryRun) {
    await fsp.mkdir(parentDir, { recursive: true });
    if (process.platform === "win32") {
      const r = spawnSync("cmd", ["/c", "mklink", "/J", target, ROOT], { stdio: "pipe" });
      if (r.status !== 0) {
        await fsp.cp(ROOT, target, { recursive: true, filter: (src) => !src.includes("node_modules") && !src.includes(".git") });
        console.log("Copied (junction failed, used copy fallback).");
      } else {
        console.log("Created junction.");
      }
    } else {
      await fsp.symlink(ROOT, target, "dir");
      console.log("Created symlink.");
    }
  } else {
    console.log(`[dry-run] Would create link: ${target} -> ${ROOT}`);
  }

  console.log("Done. Restart your agent/Codex to discover the skills.");
}

async function cmdPackCheck() {
  console.log("Checking npm pack contents...");
  const r = spawnSync("npm", ["pack", "--dry-run", "--json"], {
    cwd: ROOT,
    stdio: "pipe",
    shell: true,
  });
  if (r.status !== 0) die("npm pack --dry-run failed.");

  let files;
  try {
    const parsed = JSON.parse(r.stdout.toString());
    files = parsed[0]?.files?.map((f) => f.path) || [];
  } catch {
    die("Failed to parse npm pack output.");
  }

  const forbidden = [
    "config/office-skills.local.env",
    ".env",
    ".claude/settings.local.json",
  ];
  const forbiddenPrefixes = [
    ".claude/worktrees/",
    "node_modules/",
    "out/",
    "generated/",
    "tmp/",
    "temp/",
  ];
  const forbiddenExts = [".pem", ".key", ".p12", ".pfx", ".crt", ".cer"];

  const violations = [];
  for (const f of files) {
    const norm = f.replace(/\\/g, "/");
    if (forbidden.includes(norm)) { violations.push(f); continue; }
    for (const pat of forbiddenPrefixes) {
      if (norm.startsWith(pat)) { violations.push(f); break; }
    }
    for (const ext of forbiddenExts) {
      if (norm.endsWith(ext)) { violations.push(f); break; }
    }
  }

  if (violations.length > 0) {
    console.error("Forbidden files found in pack:");
    for (const v of violations) console.error(`  ${v}`);
    die("Fix package.json files list or .npmignore before publishing.");
  }

  console.log(`Pack check passed. ${files.length} files would be published.`);
}

// --- Main dispatch ---

const command = process.argv[2] || "help";
const handlers = {
  help: cmdHelp,
  "--help": cmdHelp,
  "-h": cmdHelp,
  validate: cmdValidate,
  "smoke:syntax": cmdSmokeSyntax,
  "smoke:image": cmdSmokeImage,
  smoke: cmdSmoke,
  install: cmdInstall,
  "pack:check": cmdPackCheck,
};

const handler = handlers[command];
if (!handler) {
  console.error(`Unknown command: ${command}`);
  cmdHelp();
  process.exit(1);
}

handler().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
