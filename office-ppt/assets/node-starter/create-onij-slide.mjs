import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { deflateSync } from "node:zlib";
import { createRequire } from "node:module";
import { loadEnvFile, resolveEnvPath } from "../../../scripts/shared/load-env.mjs";

const require = createRequire(import.meta.url);
const pptxgen = require("pptxgenjs");

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function hasFlag(name) {
  return process.argv.includes(name);
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

async function generateImage({ envPath, stylePath, outPath, prompt }) {
  loadEnvFile(envPath);
  const apiKey = process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY;
  const baseURL = process.env.OPENAI_BASE_URL || process.env.ANTHROPIC_API_BASE_URL;
  if (!apiKey) {
    throw new Error("Missing image API key. Create config/office-skills.local.env, set OFFICE_SKILLS_ENV, pass --env, or set OPENAI_API_KEY.");
  }

  const { default: OpenAI } = await import("openai");
  const client = new OpenAI({
    apiKey,
    ...(baseURL ? { baseURL } : {})
  });
  const model = process.env.PPT_IMAGE_MODEL || process.env.OPENAI_IMAGE_MODEL || "gpt-image-2";
  const size = process.env.PPT_IMAGE_SIZE || process.env.OPENAI_IMAGE_SIZE || "3840x2160";
  const quality = process.env.PPT_IMAGE_QUALITY || process.env.OPENAI_IMAGE_QUALITY || "medium";

  let result;
  if (stylePath && fs.existsSync(stylePath)) {
    result = await client.images.edit({
      model,
      image: fs.createReadStream(stylePath),
      prompt,
      size,
      quality,
      input_fidelity: process.env.PPT_IMAGE_INPUT_FIDELITY || "high"
    });
  } else {
    result = await client.images.generate({ model, prompt, size, quality });
  }

  const b64 = result.data?.[0]?.b64_json;
  if (!b64) {
    throw new Error("Image API returned no b64_json image.");
  }
  await fsp.mkdir(path.dirname(outPath), { recursive: true });
  await fsp.writeFile(outPath, Buffer.from(b64, "base64"));
}

async function createPptx({ imagePath, outPptx, title, subtitle }) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  pptx.author = "ARIHOAX Office";
  pptx.subject = "Onij-style generated slide";
  pptx.title = title;
  pptx.theme = {
    headFontFace: "Microsoft YaHei",
    bodyFontFace: "Microsoft YaHei",
    lang: "zh-CN"
  };

  const slide = pptx.addSlide();
  slide.background = { color: "0B1020" };
  slide.addImage({ path: imagePath, x: 0, y: 0, w: 13.333, h: 7.5 });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 7.5,
    fill: { color: "000000", transparency: 44 },
    line: { color: "000000", transparency: 100 }
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.62,
    y: 0.58,
    w: 0.08,
    h: 1.55,
    fill: { color: "F4C542" },
    line: { color: "F4C542", transparency: 100 }
  });
  slide.addText(title, {
    x: 0.82,
    y: 0.62,
    w: 7.4,
    h: 0.82,
    fontFace: "Microsoft YaHei",
    fontSize: 31,
    bold: true,
    color: "FFFFFF",
    margin: 0
  });
  slide.addText(subtitle, {
    x: 0.84,
    y: 1.58,
    w: 6.9,
    h: 0.86,
    fontFace: "Microsoft YaHei",
    fontSize: 14.5,
    color: "DDE7F3",
    breakLine: false,
    fit: "shrink",
    margin: 0.03
  });
  slide.addText("GPT image + PptxGenJS", {
    x: 0.84,
    y: 6.82,
    w: 2.3,
    h: 0.24,
    fontFace: "Aptos",
    fontSize: 8.5,
    color: "B8C2CC",
    margin: 0
  });

  await fsp.mkdir(path.dirname(outPptx), { recursive: true });
  await pptx.writeFile({ fileName: outPptx });
}

async function main() {
  const mock = hasFlag("--mock") || hasFlag("--no-network");
  const mockImagePath = argValue("--mock-image", undefined);
  const skillRoot = path.resolve(argValue("--skill", path.resolve(__dirname, "../../")));
  const outDir = path.resolve(argValue("--out-dir", path.join(process.cwd(), "out")));
  const imagePath = path.join(outDir, "assets", "onij-background.png");
  const outPptx = path.join(outDir, "onij-one-slide.pptx");
  const title = argValue("--title", "ONIJ 风格自动化汇报");
  const subtitle = argValue(
    "--subtitle",
    "以本地样式图作为视觉参考，生成背景图，并用原生 PowerPoint 文本承载标题与说明。"
  );

  if (mock || mockImagePath) {
    await fsp.mkdir(path.dirname(imagePath), { recursive: true });
    if (mockImagePath) {
      await fsp.copyFile(path.resolve(mockImagePath), imagePath);
    } else {
      const png = createMockPngWithZlib(deflateSync);
      await fsp.writeFile(imagePath, png);
    }
    await createPptx({ imagePath, outPptx, title, subtitle });
    console.log(`[mock] ${outPptx}`);
    return;
  }

  const envPath = path.resolve(argValue("--env", resolveEnvPath(skillRoot)));
  const stylePath = path.resolve(argValue("--style", path.join(skillRoot, "assets/styles/onij.png")));
  const prompt = argValue(
    "--prompt",
    "Create a 16:9 presentation background about modern office automation and creative document production. Use the supplied style reference for palette, texture, visual rhythm, and illustrative density. Keep clear negative space on the left for native PowerPoint text. No readable words, no logo, no UI screenshots."
  );

  await generateImage({ envPath, stylePath, outPath: imagePath, prompt });
  await createPptx({ imagePath, outPptx, title, subtitle });
  console.log(outPptx);
}

function createMockPngWithZlib(deflateSync) {
  const width = 64;
  const height = 36;
  const channels = 3;
  const raw = Buffer.alloc(height * (1 + width * channels));
  for (let y = 0; y < height; y++) {
    raw[y * (1 + width * channels)] = 0;
    for (let x = 0; x < width; x++) {
      const offset = y * (1 + width * channels) + 1 + x * channels;
      raw[offset] = 11;
      raw[offset + 1] = 16 + Math.floor(x * 0.5);
      raw[offset + 2] = 32 + Math.floor(y * 1.5);
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

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
