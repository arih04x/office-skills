import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { deflateSync } from "node:zlib";
import { loadEnvFile, resolveEnvPath } from "../../../scripts/shared/load-env.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function arg(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function hasFlag(name) {
  return process.argv.includes(name);
}

function createMockPng() {
  const width = 64;
  const height = 40;
  const channels = 3;
  const raw = Buffer.alloc(height * (1 + width * channels));
  for (let y = 0; y < height; y++) {
    raw[y * (1 + width * channels)] = 0;
    for (let x = 0; x < width; x++) {
      const offset = y * (1 + width * channels) + 1 + x * channels;
      raw[offset] = 40;
      raw[offset + 1] = 60 + Math.floor(x * 3);
      raw[offset + 2] = 100 + Math.floor(y * 3);
    }
  }
  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const ihdr = createChunk("IHDR", (() => {
    const buf = Buffer.alloc(13);
    buf.writeUInt32BE(width, 0);
    buf.writeUInt32BE(height, 4);
    buf[8] = 8; buf[9] = 2; buf[10] = 0; buf[11] = 0; buf[12] = 0;
    return buf;
  })());
  const idat = createChunk("IDAT", deflateSync(raw));
  const iend = createChunk("IEND", Buffer.alloc(0));
  return Buffer.concat([signature, ihdr, idat, iend]);
}

function createChunk(type, data) {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length, 0);
  const typeB = Buffer.from(type, "ascii");
  const crcInput = Buffer.concat([typeB, data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(crcInput), 0);
  return Buffer.concat([len, typeB, data, crc]);
}

function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) {
    c ^= buf[i];
    for (let j = 0; j < 8; j++) c = (c >>> 1) ^ (c & 1 ? 0xedb88320 : 0);
  }
  return (c ^ 0xffffffff) >>> 0;
}

async function main() {
  const mock = hasFlag("--mock") || hasFlag("--no-network");
  const mockImagePath = arg("--mock-image", undefined);
  const skillRoot = path.resolve(arg("--skill", path.resolve(__dirname, "../../")));
  const outPath = path.resolve(arg("--out", "generated-figure-layer.png"));

  if (mock || mockImagePath) {
    await fsp.mkdir(path.dirname(outPath), { recursive: true });
    if (mockImagePath) {
      await fsp.copyFile(path.resolve(mockImagePath), outPath);
    } else {
      const png = await createMockPng();
      await fsp.writeFile(outPath, png);
    }
    console.log(`[mock] ${outPath}`);
    return;
  }

  const envPath = path.resolve(arg("--env", resolveEnvPath(skillRoot)));
  const stylePath = path.resolve(arg("--style", path.join(skillRoot, "assets/styles/onij.png")));
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

  const { default: OpenAI } = await import("openai");
  const client = new OpenAI({ apiKey, ...(baseURL ? { baseURL } : {}) });
  const model = process.env.FIGURE_IMAGE_MODEL || process.env.PPT_IMAGE_MODEL || "gpt-image-2";
  const size = process.env.FIGURE_IMAGE_SIZE || process.env.OPENAI_IMAGE_SIZE || "3840x2160";
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
