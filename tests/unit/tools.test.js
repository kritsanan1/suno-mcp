import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { SunoMCPServer } from '../../src/suno-mcp/index.js';

describe('Suno MCP Tools', () => {
  let server;

  beforeEach(() => {
    server = new SunoMCPServer();
  });

  afterEach(async () => {
    // Cleanup browser instances
    if (server.browser) {
      await server.browser.close().catch(() => {});
    }
  });

  describe('Basic Tools', () => {
    it('should have suno_open_browser tool', async () => {
      // Test that tools are properly defined
      const mockRequest = {
        jsonrpc: '2.0',
        id: 1,
        method: 'tools/list',
        params: {}
      };

      // This would normally test the actual tool listing
      // For now, just verify server initialization
      expect(server).toBeDefined();
      expect(typeof server.openBrowser).toBe('function');
    });

    it('should have suno_login tool', () => {
      expect(typeof server.login).toBe('function');
    });

    it('should have suno_generate_track tool', () => {
      expect(typeof server.generateTrack).toBe('function');
    });

    it('should have suno_download_track tool', () => {
      expect(typeof server.downloadTrack).toBe('function');
    });

    it('should have suno_get_status tool', () => {
      expect(typeof server.getStatus).toBe('function');
    });

    it('should have suno_close_browser tool', () => {
      expect(typeof server.closeBrowser).toBe('function');
    });
  });

  describe('Studio Tools', () => {
    it('should have suno_studio_open tool', () => {
      expect(typeof server.studioOpen).toBe('function');
    });

    it('should have suno_studio_create_project tool', () => {
      expect(typeof server.studioCreateProject).toBe('function');
    });

    it('should have suno_studio_generate_stem tool', () => {
      expect(typeof server.studioGenerateStem).toBe('function');
    });

    it('should have suno_studio_export_project tool', () => {
      expect(typeof server.studioExportProject).toBe('function');
    });

    it('should have suno_studio_get_status tool', () => {
      expect(typeof server.studioGetStatus).toBe('function');
    });
  });

  describe('Tool Responses', () => {
    it('should return proper response format for placeholder tools', async () => {
      const result = await server.studioOpen({});
      expect(result).toHaveProperty('content');
      expect(result.content[0]).toHaveProperty('type', 'text');
      expect(result.content[0].text).toContain('Implementation needed');
    });

    it('should get server status', async () => {
      const result = await server.getStatus();
      expect(result).toHaveProperty('content');
      expect(result.content[0]).toHaveProperty('type', 'text');
      expect(result.content[0].text).toContain('Suno MCP Status');
    });
  });
});
