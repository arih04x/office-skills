import fs from "node:fs";
import path from "node:path";

/**
 * Reads a .env file and sets process.env for any key not already present.
 * Skips comments (#) and blank lines.
 */
export function loadEnvFile(envPath) {
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

/**
 * Returns the resolved path to the env file.
 * Priority: OFFICE_SKILLS_ENV env var > config/office-skills.local.env relative to skillRoot parent.
 */
export function resolveEnvPath(skillRoot) {
  if (process.env.OFFICE_SKILLS_ENV) return path.resolve(process.env.OFFICE_SKILLS_ENV);
  return path.resolve(skillRoot, "..", "config", "office-skills.local.env");
}

/**
 * Returns { apiKey, baseURL } from env vars, or null if no key is available.
 */
export function getImageConfig() {
  const apiKey = process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return null;
  const baseURL = process.env.OPENAI_BASE_URL || process.env.ANTHROPIC_API_BASE_URL;
  return { apiKey, baseURL };
}
