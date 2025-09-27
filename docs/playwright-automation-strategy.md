# Playwright Automation Strategy for Suno Studio

## Overview

This document outlines a comprehensive strategy for automating Suno Studio using Playwright, a powerful browser automation framework. The goal is to create robust, maintainable automation that can handle the complex workflows of AI music generation while being resilient to UI changes and network conditions.

## Why Playwright for Suno Studio?

### Advantages
- **Cross-Browser Support**: Works with Chromium, Firefox, and Safari
- **Modern Web Standards**: Handles complex SPAs and dynamic content
- **Reliable Selectors**: Multiple strategies for element targeting
- **Network Control**: Intercept and mock network requests
- **Screenshot/Video**: Visual debugging and documentation
- **Headless Mode**: Run automation without visible browser
- **Mobile Testing**: Emulate mobile devices for responsive testing

### Suno Studio Specific Benefits
- **Dynamic Content**: Handles AI generation progress indicators
- **File Downloads**: Manages audio file downloads and organization
- **Session Management**: Maintains login state across operations
- **Error Recovery**: Robust handling of network timeouts and failures
- **Performance Monitoring**: Track generation times and success rates

## Architecture Overview

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    Suno Studio Automation                    │
├─────────────────────────────────────────────────────────────┤
│  Playwright Browser Instance                                │
│  ├── Page Management                                        │
│  ├── Session Handling                                       │
│  ├── Element Interaction                                    │
│  └── Network Monitoring                                     │
├─────────────────────────────────────────────────────────────┤
│  Automation Layer                                           │
│  ├── Login Manager                                           │
│  ├── Project Manager                                        │
│  ├── Generation Controller                                  │
│  ├── Download Handler                                       │
│  └── Error Recovery                                         │
├─────────────────────────────────────────────────────────────┤
│  Data Management                                            │
│  ├── Configuration Store                                    │
│  ├── Session Persistence                                    │
│  ├── File Organization                                      │
│  └── Metadata Extraction                                    │
└─────────────────────────────────────────────────────────────┘
```

## Implementation Strategy

### 1. Browser Setup and Configuration

```javascript
// Browser configuration for Suno Studio
const browserConfig = {
  headless: process.env.HEADLESS !== 'false',
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--no-first-run',
    '--no-zygote',
    '--disable-gpu'
  ],
  viewport: { width: 1920, height: 1080 },
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
};

// Page configuration
const pageConfig = {
  timeout: 30000,
  waitUntil: 'networkidle',
  extraHTTPHeaders: {
    'Accept-Language': 'en-US,en;q=0.9'
  }
};
```

### 2. Session Management

```javascript
class SunoSessionManager {
  constructor(page) {
    this.page = page;
    this.isLoggedIn = false;
    this.sessionData = null;
  }

  async login(email, password) {
    try {
      // Navigate to login page
      await this.page.goto('https://app.suno.ai/login');
      
      // Wait for login form
      await this.page.waitForSelector('input[type="email"]');
      
      // Fill credentials
      await this.page.fill('input[type="email"]', email);
      await this.page.fill('input[type="password"]', password);
      
      // Submit form
      await this.page.click('button[type="submit"]');
      
      // Wait for successful login
      await this.page.waitForURL('**/create/**', { timeout: 10000 });
      
      // Save session data
      this.sessionData = await this.page.context().cookies();
      this.isLoggedIn = true;
      
      return { success: true, message: 'Login successful' };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  async restoreSession(cookies) {
    try {
      await this.page.context().addCookies(cookies);
      await this.page.goto('https://app.suno.ai/create');
      
      // Verify session is still valid
      const isLoggedIn = await this.page.locator('[data-testid="user-menu"]').isVisible();
      this.isLoggedIn = isLoggedIn;
      
      return isLoggedIn;
    } catch (error) {
      return false;
    }
  }
}
```

### 3. Project Management

```javascript
class SunoProjectManager {
  constructor(page) {
    this.page = page;
    this.currentProject = null;
  }

  async createProject(name, template = null) {
    try {
      // Navigate to Studio
      await this.page.goto('https://app.suno.ai/studio');
      
      // Click new project button
      await this.page.click('[data-testid="new-project"]');
      
      // Fill project name
      await this.page.fill('input[placeholder*="project name"]', name);
      
      // Select template if provided
      if (template) {
        await this.page.click(`[data-template="${template}"]`);
      }
      
      // Create project
      await this.page.click('button:has-text("Create")');
      
      // Wait for project to load
      await this.page.waitForSelector('[data-testid="timeline"]');
      
      this.currentProject = {
        name,
        id: await this.extractProjectId(),
        url: this.page.url()
      };
      
      return { success: true, project: this.currentProject };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  async saveProject() {
    try {
      await this.page.click('[data-testid="save-project"]');
      await this.page.waitForSelector('[data-testid="save-success"]');
      return { success: true };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }
}
```

### 4. AI Generation Controller

```javascript
class SunoGenerationController {
  constructor(page) {
    this.page = page;
    this.generationQueue = [];
    this.activeGenerations = new Map();
  }

  async generateStem(prompt, type = 'auto', position = null) {
    try {
      // Open generation panel
      await this.page.click('[data-testid="generate-stem"]');
      
      // Fill prompt
      await this.page.fill('textarea[placeholder*="describe"]', prompt);
      
      // Select stem type
      if (type !== 'auto') {
        await this.page.selectOption('select[name="stem-type"]', type);
      }
      
      // Set position if specified
      if (position) {
        await this.page.fill('input[name="position"]', position.toString());
      }
      
      // Start generation
      await this.page.click('button:has-text("Generate")');
      
      // Wait for generation to start
      const generationId = await this.waitForGenerationStart();
      
      // Track generation
      this.activeGenerations.set(generationId, {
        prompt,
        type,
        startTime: Date.now(),
        status: 'generating'
      });
      
      return { success: true, generationId };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  async waitForGenerationComplete(generationId, timeout = 300000) {
    try {
      // Wait for generation to complete
      await this.page.waitForSelector(
        `[data-generation-id="${generationId}"][data-status="completed"]`,
        { timeout }
      );
      
      // Update tracking
      const generation = this.activeGenerations.get(generationId);
      if (generation) {
        generation.status = 'completed';
        generation.endTime = Date.now();
        generation.duration = generation.endTime - generation.startTime;
      }
      
      return { success: true, generation };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  async getGenerationStatus(generationId) {
    try {
      const statusElement = await this.page.locator(
        `[data-generation-id="${generationId}"]`
      );
      
      const status = await statusElement.getAttribute('data-status');
      const progress = await statusElement.getAttribute('data-progress');
      
      return {
        status,
        progress: progress ? parseInt(progress) : 0,
        timestamp: Date.now()
      };
    } catch (error) {
      return { status: 'error', progress: 0, error: error.message };
    }
  }
}
```

### 5. Download Management

```javascript
class SunoDownloadManager {
  constructor(page, downloadPath) {
    this.page = page;
    this.downloadPath = downloadPath;
    this.downloads = new Map();
  }

  async setupDownloads() {
    // Set download path
    await this.page._client.send('Page.setDownloadBehavior', {
      behavior: 'allow',
      downloadPath: this.downloadPath
    });
  }

  async downloadTrack(trackId, format = 'mp3') {
    try {
      // Navigate to track
      await this.page.goto(`https://app.suno.ai/track/${trackId}`);
      
      // Wait for download button
      await this.page.waitForSelector('[data-testid="download-button"]');
      
      // Set up download promise
      const downloadPromise = this.page.waitForEvent('download');
      
      // Click download button
      await this.page.click('[data-testid="download-button"]');
      
      // Wait for download to start
      const download = await downloadPromise;
      
      // Save file
      const fileName = `${trackId}_${Date.now()}.${format}`;
      const filePath = path.join(this.downloadPath, fileName);
      await download.saveAs(filePath);
      
      // Track download
      this.downloads.set(trackId, {
        filePath,
        fileName,
        downloadTime: Date.now(),
        format
      });
      
      return { success: true, filePath, fileName };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }

  async downloadStems(trackId) {
    try {
      // Navigate to track
      await this.page.goto(`https://app.suno.ai/track/${trackId}`);
      
      // Click stems download
      await this.page.click('[data-testid="download-stems"]');
      
      // Wait for zip download
      const downloadPromise = this.page.waitForEvent('download');
      const download = await downloadPromise;
      
      // Save stems zip
      const fileName = `${trackId}_stems_${Date.now()}.zip`;
      const filePath = path.join(this.downloadPath, fileName);
      await download.saveAs(filePath);
      
      return { success: true, filePath, fileName };
    } catch (error) {
      return { success: false, message: error.message };
    }
  }
}
```

### 6. Error Recovery and Resilience

```javascript
class SunoErrorRecovery {
  constructor(page) {
    this.page = page;
    this.retryAttempts = 3;
    this.retryDelay = 2000;
  }

  async withRetry(operation, maxRetries = 3) {
    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error;
        
        if (attempt < maxRetries) {
          console.log(`Attempt ${attempt} failed, retrying in ${this.retryDelay}ms...`);
          await this.page.waitForTimeout(this.retryDelay);
          
          // Try to recover from common errors
          await this.recoverFromError(error);
        }
      }
    }
    
    throw lastError;
  }

  async recoverFromError(error) {
    const errorMessage = error.message.toLowerCase();
    
    if (errorMessage.includes('timeout')) {
      // Refresh page and wait for load
      await this.page.reload({ waitUntil: 'networkidle' });
    } else if (errorMessage.includes('element not found')) {
      // Wait a bit longer for dynamic content
      await this.page.waitForTimeout(5000);
    } else if (errorMessage.includes('network')) {
      // Check connection and retry
      await this.page.waitForTimeout(10000);
    }
  }

  async handleGenerationFailure(generationId) {
    try {
      // Check if generation is still running
      const status = await this.getGenerationStatus(generationId);
      
      if (status.status === 'failed') {
        // Try to restart generation
        await this.page.click(`[data-generation-id="${generationId}"] button[data-action="retry"]`);
        return { success: true, action: 'retried' };
      }
      
      return { success: false, reason: 'generation_still_running' };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}
```

## MCP Integration Strategy

### Tool Definitions

```javascript
// Enhanced MCP tools for Suno Studio
const sunoStudioTools = [
  {
    name: "suno_studio_open",
    description: "Open Suno Studio and initialize session",
    inputSchema: {
      type: "object",
      properties: {
        headless: { type: "boolean", default: true },
        restoreSession: { type: "boolean", default: true }
      }
    }
  },
  {
    name: "suno_studio_create_project",
    description: "Create a new project in Suno Studio",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string", description: "Project name" },
        template: { type: "string", description: "Template to use" }
      },
      required: ["name"]
    }
  },
  {
    name: "suno_studio_generate_stem",
    description: "Generate a musical stem using AI",
    inputSchema: {
      type: "object",
      properties: {
        prompt: { type: "string", description: "Generation prompt" },
        type: { type: "string", description: "Stem type (vocals, drums, bass, etc.)" },
        position: { type: "number", description: "Timeline position" }
      },
      required: ["prompt"]
    }
  },
  {
    name: "suno_studio_wait_generation",
    description: "Wait for AI generation to complete",
    inputSchema: {
      type: "object",
      properties: {
        generationId: { type: "string", description: "Generation ID to wait for" },
        timeout: { type: "number", description: "Timeout in milliseconds" }
      },
      required: ["generationId"]
    }
  },
  {
    name: "suno_studio_export_project",
    description: "Export project as audio files",
    inputSchema: {
      type: "object",
      properties: {
        format: { type: "string", description: "Export format (mp3, wav, etc.)" },
        includeStems: { type: "boolean", description: "Include individual stems" },
        downloadPath: { type: "string", description: "Download directory" }
      }
    }
  }
];
```

### Workflow Automation

```javascript
class SunoStudioWorkflow {
  constructor() {
    this.sessionManager = null;
    this.projectManager = null;
    this.generationController = null;
    this.downloadManager = null;
  }

  async executeWorkflow(workflowConfig) {
    try {
      // Initialize components
      await this.initialize();
      
      // Login if needed
      if (!this.sessionManager.isLoggedIn) {
        await this.sessionManager.login(
          workflowConfig.email,
          workflowConfig.password
        );
      }
      
      // Create project
      const project = await this.projectManager.createProject(
        workflowConfig.projectName
      );
      
      // Generate stems
      const generations = [];
      for (const stemConfig of workflowConfig.stems) {
        const generation = await this.generationController.generateStem(
          stemConfig.prompt,
          stemConfig.type,
          stemConfig.position
        );
        generations.push(generation);
      }
      
      // Wait for all generations
      for (const generation of generations) {
        await this.generationController.waitForGenerationComplete(
          generation.generationId
        );
      }
      
      // Export project
      const exportResult = await this.downloadManager.exportProject(
        workflowConfig.exportFormat,
        workflowConfig.includeStems,
        workflowConfig.downloadPath
      );
      
      return {
        success: true,
        project,
        generations,
        export: exportResult
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}
```

## Best Practices

### 1. Robust Element Selection

```javascript
// Use multiple selector strategies
const selectors = {
  loginButton: [
    'button:has-text("Sign in")',
    '[data-testid="login-button"]',
    'a[href*="login"]',
    '.login-btn'
  ],
  generateButton: [
    'button:has-text("Generate")',
    '[data-testid="generate-button"]',
    'button[type="submit"]',
    '.generate-btn'
  ]
};

async function clickElement(page, selectorKey) {
  const strategies = selectors[selectorKey];
  
  for (const strategy of strategies) {
    try {
      await page.click(strategy, { timeout: 5000 });
      return true;
    } catch (error) {
      continue;
    }
  }
  
  throw new Error(`Could not find element: ${selectorKey}`);
}
```

### 2. Wait Strategies

```javascript
// Comprehensive wait strategies
class WaitStrategies {
  static async waitForGenerationStart(page) {
    // Wait for generation indicator
    await page.waitForSelector('[data-testid="generation-indicator"]');
    
    // Wait for progress bar
    await page.waitForSelector('[data-testid="progress-bar"]');
    
    // Wait for generation ID to be assigned
    const generationId = await page.waitForFunction(() => {
      const indicator = document.querySelector('[data-generation-id]');
      return indicator ? indicator.getAttribute('data-generation-id') : null;
    });
    
    return generationId;
  }

  static async waitForPageLoad(page, url) {
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.waitForLoadState('domcontentloaded');
    await page.waitForTimeout(2000); // Additional buffer
  }
}
```

### 3. Error Handling

```javascript
// Comprehensive error handling
class ErrorHandler {
  static async handleNetworkError(page, error) {
    if (error.message.includes('net::ERR_INTERNET_DISCONNECTED')) {
      // Wait for connection to be restored
      await page.waitForTimeout(10000);
      return { retry: true, delay: 5000 };
    }
    
    if (error.message.includes('timeout')) {
      // Increase timeout and retry
      return { retry: true, delay: 2000 };
    }
    
    return { retry: false, error: error.message };
  }

  static async handleUIError(page, error) {
    if (error.message.includes('element not found')) {
      // Take screenshot for debugging
      await page.screenshot({ path: 'error-screenshot.png' });
      
      // Try to refresh page
      await page.reload();
      return { retry: true, delay: 3000 };
    }
    
    return { retry: false, error: error.message };
  }
}
```

## Testing Strategy

### 1. Unit Tests

```javascript
// Test individual components
describe('SunoSessionManager', () => {
  test('should login successfully', async () => {
    const page = await browser.newPage();
    const sessionManager = new SunoSessionManager(page);
    
    const result = await sessionManager.login('test@example.com', 'password');
    expect(result.success).toBe(true);
  });
});
```

### 2. Integration Tests

```javascript
// Test complete workflows
describe('Suno Studio Workflow', () => {
  test('should create project and generate stems', async () => {
    const workflow = new SunoStudioWorkflow();
    
    const result = await workflow.executeWorkflow({
      projectName: 'Test Project',
      stems: [
        { prompt: 'upbeat drums', type: 'drums' },
        { prompt: 'melodic bass line', type: 'bass' }
      ]
    });
    
    expect(result.success).toBe(true);
    expect(result.generations).toHaveLength(2);
  });
});
```

### 3. Performance Tests

```javascript
// Test performance and reliability
describe('Performance Tests', () => {
  test('should handle multiple concurrent generations', async () => {
    const startTime = Date.now();
    
    const promises = Array(5).fill().map(async (_, i) => {
      return await generateStem(`test prompt ${i}`);
    });
    
    const results = await Promise.all(promises);
    const duration = Date.now() - startTime;
    
    expect(results.every(r => r.success)).toBe(true);
    expect(duration).toBeLessThan(300000); // 5 minutes
  });
});
```

## Monitoring and Logging

### 1. Performance Monitoring

```javascript
class PerformanceMonitor {
  constructor() {
    this.metrics = new Map();
  }

  startOperation(operationId) {
    this.metrics.set(operationId, {
      startTime: Date.now(),
      status: 'running'
    });
  }

  endOperation(operationId, success = true) {
    const metric = this.metrics.get(operationId);
    if (metric) {
      metric.endTime = Date.now();
      metric.duration = metric.endTime - metric.startTime;
      metric.success = success;
    }
  }

  getMetrics() {
    return Array.from(this.metrics.values());
  }
}
```

### 2. Logging Strategy

```javascript
class SunoLogger {
  constructor() {
    this.logs = [];
  }

  log(level, message, data = null) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      data
    };
    
    this.logs.push(logEntry);
    console.log(`[${level.toUpperCase()}] ${message}`, data || '');
  }

  error(message, error) {
    this.log('error', message, {
      error: error.message,
      stack: error.stack
    });
  }

  info(message, data) {
    this.log('info', message, data);
  }

  debug(message, data) {
    this.log('debug', message, data);
  }
}
```

## Conclusion

This automation strategy provides a comprehensive approach to automating Suno Studio using Playwright. The modular architecture allows for easy maintenance and extension, while the robust error handling ensures reliable operation even when facing network issues or UI changes.

The key to success is implementing proper wait strategies, comprehensive error recovery, and maintaining flexibility in element selection. With this foundation, you can build sophisticated automation workflows that leverage the full power of Suno Studio's AI capabilities.

---

*This strategy document provides the technical foundation for implementing robust Suno Studio automation. Regular updates will be needed as the platform evolves and new features are added.*
