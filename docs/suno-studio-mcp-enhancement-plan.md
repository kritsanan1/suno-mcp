# Suno Studio MCP Tools Enhancement Plan

## Overview

This document outlines the enhancement of the existing Suno MCP server to support the new Suno Studio features. The current implementation focuses on basic Suno AI generation, but needs to be expanded to handle the advanced DAW-like capabilities of Suno Studio.

## Current MCP Tools Analysis

### Existing Tools
1. `suno_open_browser` - Basic browser opening
2. `suno_login` - Authentication
3. `suno_generate_track` - Simple track generation
4. `suno_download_track` - Track downloading
5. `suno_get_status` - Status checking
6. `suno_close_browser` - Cleanup

### Limitations
- No Suno Studio specific functionality
- Limited to basic track generation
- No project management
- No stem generation
- No timeline manipulation
- No advanced export options

## Enhanced MCP Tools Design

### 1. Studio Management Tools

#### `suno_studio_open`
```javascript
{
  name: "suno_studio_open",
  description: "Open Suno Studio and initialize session",
  inputSchema: {
    type: "object",
    properties: {
      headless: { 
        type: "boolean", 
        description: "Run browser in headless mode",
        default: true 
      },
      restoreSession: { 
        type: "boolean", 
        description: "Restore previous session if available",
        default: true 
      },
      viewport: {
        type: "object",
        properties: {
          width: { type: "number", default: 1920 },
          height: { type: "number", default: 1080 }
        }
      }
    }
  }
}
```

#### `suno_studio_close`
```javascript
{
  name: "suno_studio_close",
  description: "Close Suno Studio and save session data",
  inputSchema: {
    type: "object",
    properties: {
      saveSession: { 
        type: "boolean", 
        description: "Save session data for future use",
        default: true 
      }
    }
  }
}
```

### 2. Project Management Tools

#### `suno_studio_create_project`
```javascript
{
  name: "suno_studio_create_project",
  description: "Create a new project in Suno Studio",
  inputSchema: {
    type: "object",
    properties: {
      name: { 
        type: "string", 
        description: "Project name" 
      },
      template: { 
        type: "string", 
        description: "Template to use (pop, rock, electronic, etc.)",
        default: "blank"
      },
      bpm: { 
        type: "number", 
        description: "Initial BPM",
        default: 120 
      },
      key: { 
        type: "string", 
        description: "Musical key",
        default: "C"
      }
    },
    required: ["name"]
  }
}
```

#### `suno_studio_open_project`
```javascript
{
  name: "suno_studio_open_project",
  description: "Open an existing project",
  inputSchema: {
    type: "object",
    properties: {
      projectId: { 
        type: "string", 
        description: "Project ID to open" 
      },
      projectName: { 
        type: "string", 
        description: "Project name to search for" 
      }
    }
  }
}
```

#### `suno_studio_save_project`
```javascript
{
  name: "suno_studio_save_project",
  description: "Save current project",
  inputSchema: {
    type: "object",
    properties: {
      name: { 
        type: "string", 
        description: "New name for the project (optional)" 
      },
      autoSave: { 
        type: "boolean", 
        description: "Enable auto-save",
        default: true 
      }
    }
  }
}
```

### 3. AI Generation Tools

#### `suno_studio_generate_stem`
```javascript
{
  name: "suno_studio_generate_stem",
  description: "Generate a musical stem using AI",
  inputSchema: {
    type: "object",
    properties: {
      prompt: { 
        type: "string", 
        description: "Detailed description of the stem to generate" 
      },
      type: { 
        type: "string", 
        description: "Stem type",
        enum: ["vocals", "drums", "bass", "guitar", "synth", "piano", "strings", "brass", "auto"],
        default: "auto"
      },
      position: { 
        type: "number", 
        description: "Timeline position in seconds",
        default: 0 
      },
      duration: { 
        type: "number", 
        description: "Duration in seconds",
        default: 30 
      },
      style: { 
        type: "string", 
        description: "Musical style/genre" 
      },
      mood: { 
        type: "string", 
        description: "Mood/emotion",
        enum: ["happy", "sad", "energetic", "calm", "dramatic", "mysterious", "romantic"]
      },
      lyrics: { 
        type: "string", 
        description: "Custom lyrics (for vocal stems)" 
      }
    },
    required: ["prompt"]
  }
}
```

#### `suno_studio_generate_multiple_stems`
```javascript
{
  name: "suno_studio_generate_multiple_stems",
  description: "Generate multiple stems in sequence",
  inputSchema: {
    type: "object",
    properties: {
      stems: {
        type: "array",
        items: {
          type: "object",
          properties: {
            prompt: { type: "string" },
            type: { type: "string" },
            position: { type: "number" },
            duration: { type: "number" }
          },
          required: ["prompt"]
        }
      },
      parallel: { 
        type: "boolean", 
        description: "Generate stems in parallel",
        default: false 
      }
    },
    required: ["stems"]
  }
}
```

#### `suno_studio_wait_generation`
```javascript
{
  name: "suno_studio_wait_generation",
  description: "Wait for AI generation to complete",
  inputSchema: {
    type: "object",
    properties: {
      generationId: { 
        type: "string", 
        description: "Generation ID to wait for" 
      },
      timeout: { 
        type: "number", 
        description: "Timeout in milliseconds",
        default: 300000 
      },
      checkInterval: { 
        type: "number", 
        description: "Check interval in milliseconds",
        default: 5000 
      }
    },
    required: ["generationId"]
  }
}
```

### 4. Timeline and Arrangement Tools

#### `suno_studio_arrange_track`
```javascript
{
  name: "suno_studio_arrange_track",
  description: "Arrange tracks on the timeline",
  inputSchema: {
    type: "object",
    properties: {
      trackId: { 
        type: "string", 
        description: "Track ID to arrange" 
      },
      startTime: { 
        type: "number", 
        description: "Start time in seconds" 
      },
      endTime: { 
        type: "number", 
        description: "End time in seconds" 
      },
      loop: { 
        type: "boolean", 
        description: "Loop the track",
        default: false 
      },
      fadeIn: { 
        type: "number", 
        description: "Fade in duration in seconds",
        default: 0 
      },
      fadeOut: { 
        type: "number", 
        description: "Fade out duration in seconds",
        default: 0 
      }
    },
    required: ["trackId", "startTime"]
  }
}
```

#### `suno_studio_set_bpm`
```javascript
{
  name: "suno_studio_set_bpm",
  description: "Set project BPM",
  inputSchema: {
    type: "object",
    properties: {
      bpm: { 
        type: "number", 
        description: "Beats per minute",
        minimum: 60,
        maximum: 200 
      },
      adjustExisting: { 
        type: "boolean", 
        description: "Adjust existing tracks to new BPM",
        default: true 
      }
    },
    required: ["bpm"]
  }
}
```

#### `suno_studio_create_sections`
```javascript
{
  name: "suno_studio_create_sections",
  description: "Create song sections (verse, chorus, bridge)",
  inputSchema: {
    type: "object",
    properties: {
      sections: {
        type: "array",
        items: {
          type: "object",
          properties: {
            name: { type: "string" },
            startTime: { type: "number" },
            endTime: { type: "number" },
            repeat: { type: "number", default: 1 }
          },
          required: ["name", "startTime", "endTime"]
        }
      }
    },
    required: ["sections"]
  }
}
```

### 5. Mixing and Effects Tools

#### `suno_studio_adjust_volume`
```javascript
{
  name: "suno_studio_adjust_volume",
  description: "Adjust track volume",
  inputSchema: {
    type: "object",
    properties: {
      trackId: { 
        type: "string", 
        description: "Track ID" 
      },
      volume: { 
        type: "number", 
        description: "Volume level (0-100)",
        minimum: 0,
        maximum: 100 
      },
      automation: {
        type: "object",
        properties: {
          enabled: { type: "boolean" },
          points: {
            type: "array",
            items: {
              type: "object",
              properties: {
                time: { type: "number" },
                volume: { type: "number" }
              }
            }
          }
        }
      }
    },
    required: ["trackId", "volume"]
  }
}
```

#### `suno_studio_add_effect`
```javascript
{
  name: "suno_studio_add_effect",
  description: "Add audio effect to track",
  inputSchema: {
    type: "object",
    properties: {
      trackId: { 
        type: "string", 
        description: "Track ID" 
      },
      effect: { 
        type: "string", 
        description: "Effect type",
        enum: ["reverb", "delay", "chorus", "distortion", "compressor", "eq", "filter"]
      },
      parameters: {
        type: "object",
        description: "Effect parameters"
      },
      wetDry: { 
        type: "number", 
        description: "Wet/Dry mix (0-100)",
        default: 50 
      }
    },
    required: ["trackId", "effect"]
  }
}
```

### 6. Export and Download Tools

#### `suno_studio_export_project`
```javascript
{
  name: "suno_studio_export_project",
  description: "Export project as audio files",
  inputSchema: {
    type: "object",
    properties: {
      format: { 
        type: "string", 
        description: "Export format",
        enum: ["mp3", "wav", "flac", "aac"],
        default: "mp3" 
      },
      quality: { 
        type: "string", 
        description: "Export quality",
        enum: ["low", "medium", "high", "lossless"],
        default: "high" 
      },
      includeStems: { 
        type: "boolean", 
        description: "Include individual stems",
        default: true 
      },
      includeMIDI: { 
        type: "boolean", 
        description: "Include MIDI files",
        default: false 
      },
      downloadPath: { 
        type: "string", 
        description: "Download directory path",
        default: "D:\\Dev\\repos\\temp" 
      },
      fileName: { 
        type: "string", 
        description: "Custom file name" 
      }
    }
  }
}
```

#### `suno_studio_export_section`
```javascript
{
  name: "suno_studio_export_section",
  description: "Export specific section of the project",
  inputSchema: {
    type: "object",
    properties: {
      sectionName: { 
        type: "string", 
        description: "Section name to export" 
      },
      startTime: { 
        type: "number", 
        description: "Start time in seconds" 
      },
      endTime: { 
        type: "number", 
        description: "End time in seconds" 
      },
      format: { 
        type: "string", 
        enum: ["mp3", "wav", "flac"],
        default: "mp3" 
      },
      downloadPath: { 
        type: "string", 
        default: "D:\\Dev\\repos\\temp" 
      }
    },
    required: ["sectionName"]
  }
}
```

### 7. Monitoring and Status Tools

#### `suno_studio_get_status`
```javascript
{
  name: "suno_studio_get_status",
  description: "Get comprehensive Studio status",
  inputSchema: {
    type: "object",
    properties: {
      includeGenerations: { 
        type: "boolean", 
        description: "Include active generation status",
        default: true 
      },
      includeProject: { 
        type: "boolean", 
        description: "Include current project info",
        default: true 
      },
      includeTracks: { 
        type: "boolean", 
        description: "Include track information",
        default: true 
      }
    }
  }
}
```

#### `suno_studio_get_generation_status`
```javascript
{
  name: "suno_studio_get_generation_status",
  description: "Get status of specific generation",
  inputSchema: {
    type: "object",
    properties: {
      generationId: { 
        type: "string", 
        description: "Generation ID" 
      }
    },
    required: ["generationId"]
  }
}
```

#### `suno_studio_list_projects`
```javascript
{
  name: "suno_studio_list_projects",
  description: "List available projects",
  inputSchema: {
    type: "object",
    properties: {
      limit: { 
        type: "number", 
        description: "Maximum number of projects to return",
        default: 20 
      },
      sortBy: { 
        type: "string", 
        enum: ["name", "created", "modified"],
        default: "modified" 
      }
    }
  }
}
```

## Implementation Plan

### Phase 1: Core Studio Integration (Week 1-2)
1. **Update browser automation** to handle Suno Studio interface
2. **Implement session management** for Studio-specific features
3. **Add project creation and management** tools
4. **Basic stem generation** functionality

### Phase 2: Advanced Generation Features (Week 3-4)
1. **Multiple stem generation** with parallel processing
2. **Generation status monitoring** and progress tracking
3. **Error recovery** for failed generations
4. **Generation queue management**

### Phase 3: Timeline and Arrangement (Week 5-6)
1. **Timeline manipulation** tools
2. **Track arrangement** and positioning
3. **BPM and tempo control**
4. **Section creation** and management

### Phase 4: Mixing and Effects (Week 7-8)
1. **Volume and panning control**
2. **Audio effects** integration
3. **Automation** capabilities
4. **Real-time monitoring**

### Phase 5: Export and Integration (Week 9-10)
1. **Advanced export options**
2. **Stem separation** and individual downloads
3. **MIDI export** capabilities
4. **Cloud integration** options

### Phase 6: Testing and Optimization (Week 11-12)
1. **Comprehensive testing** suite
2. **Performance optimization**
3. **Error handling** improvements
4. **Documentation** updates

## Code Structure Updates

### Enhanced Server Class
```javascript
class SunoStudioMCPServer extends SunoMCPServer {
  constructor() {
    super();
    this.studioManager = new SunoStudioManager();
    this.projectManager = new SunoProjectManager();
    this.generationController = new SunoGenerationController();
    this.timelineManager = new SunoTimelineManager();
    this.mixingEngine = new SunoMixingEngine();
    this.exportManager = new SunoExportManager();
  }

  // Override existing methods and add new ones
  async setupToolHandlers() {
    await super.setupToolHandlers();
    await this.setupStudioToolHandlers();
  }

  async setupStudioToolHandlers() {
    // Add Studio-specific tool handlers
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;
      
      switch (name) {
        case "suno_studio_open":
          return await this.openStudio(args);
        case "suno_studio_create_project":
          return await this.createProject(args);
        case "suno_studio_generate_stem":
          return await this.generateStem(args);
        // ... other Studio tools
      }
    });
  }
}
```

### Manager Classes
```javascript
class SunoStudioManager {
  constructor(page) {
    this.page = page;
    this.isStudioOpen = false;
    this.currentProject = null;
  }

  async openStudio(headless = true) {
    // Implementation for opening Studio
  }

  async closeStudio(saveSession = true) {
    // Implementation for closing Studio
  }
}

class SunoProjectManager {
  constructor(page) {
    this.page = page;
    this.projects = new Map();
  }

  async createProject(name, template = 'blank') {
    // Implementation for project creation
  }

  async openProject(projectId) {
    // Implementation for opening projects
  }
}

class SunoGenerationController {
  constructor(page) {
    this.page = page;
    this.activeGenerations = new Map();
    this.generationQueue = [];
  }

  async generateStem(prompt, type = 'auto') {
    // Implementation for stem generation
  }

  async waitForGeneration(generationId, timeout = 300000) {
    // Implementation for waiting for generation completion
  }
}
```

## Testing Strategy

### Unit Tests
- Test individual manager classes
- Test tool parameter validation
- Test error handling scenarios

### Integration Tests
- Test complete workflows
- Test Studio-specific features
- Test error recovery

### Performance Tests
- Test concurrent generation handling
- Test large project management
- Test export performance

## Documentation Updates

### User Guide
- Update README with Studio features
- Add Studio-specific examples
- Document new workflow patterns

### API Documentation
- Document all new tools
- Provide usage examples
- Document parameter specifications

### Troubleshooting Guide
- Studio-specific issues
- Generation troubleshooting
- Export problems

## Conclusion

This enhancement plan transforms the basic Suno MCP server into a comprehensive Suno Studio automation platform. The phased approach ensures stable development while adding powerful new capabilities that leverage the full potential of Suno Studio's DAW-like features.

The modular architecture allows for easy maintenance and future enhancements, while the comprehensive tool set provides users with professional-level automation capabilities for AI music production.

---

*This implementation plan provides a roadmap for enhancing the Suno MCP server to support Suno Studio's advanced features. Regular updates and testing will ensure compatibility as the platform evolves.*
