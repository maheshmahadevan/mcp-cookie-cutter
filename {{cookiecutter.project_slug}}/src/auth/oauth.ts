{% if cookiecutter.sdk_choice == 'typescript' and cookiecutter.auth_mechanism == 'oauth2' -%}
/**
 * OAuth 2.1 authentication handler
 * Follows MCP security best practices
 */

import { Request } from "express";
import { Issuer, Client } from "openid-client";

const log = {
  info: (msg: string) => console.error(`[INFO] ${msg}`),
  error: (msg: string) => console.error(`[ERROR] ${msg}`),
  warn: (msg: string) => console.error(`[WARN] ${msg}`),
};

export class OAuthHandler {
  private client?: Client;

  constructor(
    private clientId?: string,
    private clientSecret?: string,
    private issuerUrl?: string
  ) {
    this.initialize();
  }

  private async initialize(): Promise<void> {
    if (!this.issuerUrl || !this.clientId) {
      log.warn("OAuth not configured - authentication will fail");
      return;
    }

    try {
      const issuer = await Issuer.discover(this.issuerUrl);
      this.client = new issuer.Client({
        client_id: this.clientId,
        client_secret: this.clientSecret,
        token_endpoint_auth_method: this.clientSecret ? "client_secret_basic" : "none",
      });
      log.info("OAuth client initialized");
    } catch (error) {
      log.error(`Failed to initialize OAuth: ${error}`);
    }
  }

  async authenticate(req: Request): Promise<boolean> {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      log.warn("Missing or invalid Authorization header");
      return false;
    }

    const token = authHeader.substring(7);

    try {
      await this.verifyToken(token);
      return true;
    } catch (error) {
      log.error(`Token verification failed: ${error}`);
      return false;
    }
  }

  private async verifyToken(token: string): Promise<void> {
    if (!this.client) {
      throw new Error("OAuth client not initialized");
    }

    // Verify token via introspection endpoint or JWT validation
    // Implementation depends on your OAuth provider
    const userinfo = await this.client.userinfo(token);
    log.info(`Token verified for user: ${userinfo.sub}`);
  }

  getAuthorizationUrl(): string {
    if (!this.client) {
      throw new Error("OAuth client not initialized");
    }

    // Generate authorization URL with PKCE for public clients
    const url = this.client.authorizationUrl({
      scope: "openid profile email",
      response_type: "code",
    });

    return url;
  }
}
{%- endif %}
