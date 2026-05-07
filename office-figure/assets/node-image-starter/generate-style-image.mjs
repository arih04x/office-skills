import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import OpenAI from "openai";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function loadEnvFile(envPath) {
  if (!envPath || !fs.existsSync(envPath)) return;
  for (const line of fs.readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq < 0) continue;
    const key = trimmed.slice(0, eq).trim();
    const value = trimmed.slice(eq + 1).trim();
    if (key && !(key in process.env)) process.env[key] = value;
  }
}

function arg(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function resolveDefaultEnvPath(skillRoot) {
  if (process.env.OFFICE_SKILLS_ENV) return path.resolve(process.env.OFFICE_SKILLS_ENV);
  return path.resolve(skillRoot, "..", "config", "office-skills.local.env");
}

async function main() {
  const skillRoot = path.resolve(arg("--skill", path.resolve(__dirname, "../../")));
  const envPath = path.resolve(arg("--env", resolveDefaultEnvPath(skillRoot)));
  const stylePath = path.resolve(arg("--style", path.join(skillRoot, "assets/styles/onij.png")));
  const outPath = path.resolve(arg("--out", "generated-figure-layer.png"));
  const prompt = arg("--prompt", [
    "Create a wide scientific figure background.",
    "Use the supplied style reference for palette, texture, and density.",
    "Leave open space for editable labels and arrows.",
    "No readable words, no logos, no screenshots."
  ].join(" "));

  loadEnvFile(envPath);
  const apiKey = process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY;
  const baseURL = process.env.OPENAI_BASE_URL || process.env.ANTHROPIC_API_BASE_URL;
  if (!apiKey) {
    throw new Error("Missing image API key. Create config/office-skills.local.env, set OFFICE_SKILLS_ENV, pass --env, or set OPENAI_API_KEY.");
  }

  const client = new OpenAI({ apiKey, ...(baseURL ? { baseURL } : {}) });
  const model = process.env.FIGURE_IMAGE_MODEL || process.env.PPT_IMAGE_MODEL || "gpt-image-2";
  const size = process.env.FIGURE_IMAGE_SIZE || process.env.OPENAI_IMAGE_SIZE || "1536x1024";
  const quality = process.env.FIGURE_IMAGE_QUALITY || process.env.OPENAI_IMAGE_QUALITY || "medium";

  let result;
  if (fs.existsSync(stylePath)) {
    result = await client.images.edit({
      model,
      image: fs.createReadStream(stylePath),
      prompt,
      size,
      quality,
      input_fidelity: process.env.FIGURE_IMAGE_INPUT_FIDELITY || process.env.PPT_IMAGE_INPUT_FIDELITY || "high"
    });
  } else {
    result = await client.images.generate({ model, prompt, size, quality });
  }

  const b64 = result.data?.[0]?.b64_json;
  if (!b64) throw new Error("Image API returned no b64_json image.");
  await fsp.mkdir(path.dirname(outPath), { recursive: true });
  await fsp.writeFile(outPath, Buffer.from(b64, "base64"));
  console.log(outPath);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
