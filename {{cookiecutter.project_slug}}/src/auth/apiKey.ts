{% if cookiecutter.sdk_choice == 'typescript' and cookiecutter.auth_mechanism == 'api_key' -%}
/**
 * API Key authentication handler
 * Note: OAuth 2.1 is recommended for public clients
 */

import { Request } from "express";
import * as dotenv from "dotenv";

dotenv.config();

const log = {
  info: (msg: string) => console.error(`[INFO] ${msg}`),
  warn: (msg: string) => console.error(`[WARN] ${msg}`),
};

export class APIKeyHandler {
  private validKeys: Set<string>;

  constructor(validKeys?: string[]) {
    if (validKeys) {
      this.validKeys = new Set(validKeys);
    } else {
      // Load from environment variable
      const keysStr = process.env.MCP_API_KEYS || "";
      this.validKeys = new Set(
        keysStr.split(",").map((k) => k.trim()).filter((k) => k)
      );
    }

    if (this.validKeys.size === 0) {
      log.warn("No API keys configured - all requests will be rejected");
    }
  }

  async authenticate(req: Request): Promise<boolean> {
    // Try Authorization header
    const authHeader = req.headers.authorization;
    if (authHeader && authHeader.startsWith("Bearer ")) {
      const apiKey = authHeader.substring(7);
      if (this.validKeys.has(apiKey)) {
        log.info("Request authenticated via Authorization header");
        return true;
      }
    }

    // Try query parameter
    const queryKey = req.query.api_key as string;
    if (queryKey && this.validKeys.has(queryKey)) {
      log.info("Request authenticated via query parameter");
      return true;
    }

    // Try custom header
    const headerKey = req.headers["x-api-key"] as string;
    if (headerKey && this.validKeys.has(headerKey)) {
      log.info("Request authenticated via X-API-Key header");
      return true;
    }

    log.warn("Authentication failed: Invalid or missing API key");
    return false;
  }

  addKey(apiKey: string): void {
    this.validKeys.add(apiKey);
    log.info("New API key added");
  }

  revokeKey(apiKey: string): void {
    this.validKeys.delete(apiKey);
    log.info("API key revoked");
  }
}
{%- endif %}
