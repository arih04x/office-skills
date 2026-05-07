import fs from "node:fs";
import fsp from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import OpenAI from "openai";
import pptxgen from "pptxgenjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function loadEnvFile(envPath) {
  if (!envPath || !fs.existsSync(envPath)) return;
  const raw = fs.readFileSync(envPath, "utf8");
  for (const line of raw.split(/\r?\n/)) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eq = trimmed.indexOf("=");
    if (eq < 0) continue;
    const key = trimmed.slice(0, eq).trim();
    const value = trimmed.slice(eq + 1).trim();
    if (key && !(key in process.env)) process.env[key] = value;
  }
}

function argValue(name, fallback) {
  const index = process.argv.indexOf(name);
  return index >= 0 && process.argv[index + 1] ? process.argv[index + 1] : fallback;
}

function resolveDefaultEnvPath(skillRoot) {
  if (process.env.OFFICE_SKILLS_ENV) return path.resolve(process.env.OFFICE_SKILLS_ENV);
  return path.resolve(skillRoot, "..", "config", "office-skills.local.env");
}

async function generateImage({ envPath, stylePath, outPath, prompt }) {
  loadEnvFile(envPath);
  const apiKey = process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY;
  const baseURL = process.env.OPENAI_BASE_URL || process.env.ANTHROPIC_API_BASE_URL;
  if (!apiKey) {
    throw new Error("Missing image API key. Create config/office-skills.local.env, set OFFICE_SKILLS_ENV, pass --env, or set OPENAI_API_KEY.");
  }

  const client = new OpenAI({
    apiKey,
    ...(baseURL ? { baseURL } : {})
  });
  const model = process.env.PPT_IMAGE_MODEL || process.env.OPENAI_IMAGE_MODEL || "gpt-image-2";
  const size = process.env.PPT_IMAGE_SIZE || process.env.OPENAI_IMAGE_SIZE || "1536x1024";
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
  const skillRoot = path.resolve(argValue("--skill", path.resolve(__dirname, "../../")));
  const envPath = path.resolve(argValue("--env", resolveDefaultEnvPath(skillRoot)));
  const stylePath = path.resolve(argValue("--style", path.join(skillRoot, "assets/styles/onij.png")));
  const outDir = path.resolve(argValue("--out-dir", path.join(process.cwd(), "out")));
  const imagePath = path.join(outDir, "assets", "onij-background.png");
  const outPptx = path.join(outDir, "onij-one-slide.pptx");
  const title = argValue("--title", "ONIJ 风格自动化汇报");
  const subtitle = argValue(
    "--subtitle",
    "以本地样式图作为视觉参考，生成背景图，并用原生 PowerPoint 文本承载标题与说明。"
  );
  const prompt = argValue(
    "--prompt",
    "Create a 16:9 presentation background about modern office automation and creative document production. Use the supplied style reference for palette, texture, visual rhythm, and illustrative density. Keep clear negative space on the left for native PowerPoint text. No readable words, no logo, no UI screenshots."
  );

  await generateImage({ envPath, stylePath, outPath: imagePath, prompt });
  await createPptx({ imagePath, outPptx, title, subtitle });
  console.log(outPptx);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
