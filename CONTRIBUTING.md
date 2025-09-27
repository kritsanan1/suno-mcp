# Contributing to Suno MCP Server

Thank you for your interest in contributing to the Suno MCP Server! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Claude Desktop (for testing MCP integration)
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/sandraschi/suno-mcp.git
cd suno-mcp

# Install dependencies
npm install

# Run tests
npm test

# Start development server
npm run dev
```

## Development Workflow

### Branching Strategy
- `main` - Production-ready code
- `develop` - Development integration branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches
- `hotfix/*` - Critical fixes for production

### Commit Messages
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

### Pull Requests
1. Create a feature branch from `develop`
2. Make your changes with tests
3. Ensure all tests pass
4. Update documentation if needed
5. Submit PR with clear description
6. Wait for review and CI checks

## Code Standards

### JavaScript/Node.js
- Use ES6+ features
- Follow Airbnb JavaScript Style Guide
- Use meaningful variable and function names
- Add JSDoc comments for public APIs
- Use async/await for asynchronous operations

### MCP Tools
- Each tool must have proper input validation
- Include comprehensive error handling
- Provide clear, helpful error messages
- Follow consistent parameter naming
- Document tool behavior in comments

### Testing
- Write unit tests for all new functionality
- Include integration tests for tool workflows
- Test both MCP and FastAPI interfaces
- Maintain >80% code coverage
- Test error conditions and edge cases

## Architecture Guidelines

### Dual Interface Design
The server implements both MCP (stdio) and FastAPI (HTTP) interfaces:

```javascript
// MCP Interface (Claude Desktop)
class SunoMCPServer {
  // MCP protocol handlers
}

// FastAPI Interface (Web/Testing)
class DualInterfaceServer {
  // HTTP endpoints
}
```

### Tool Organization
- Tools are organized by category
- Each tool has consistent error handling
- Placeholder implementations for planned features
- Clear separation between basic and advanced tools

### Error Handling
```javascript
try {
  // Tool implementation
  return { success: true, result: data };
} catch (error) {
  return {
    success: false,
    error: error.message,
    tool: toolName
  };
}
```

## Testing

### Running Tests
```bash
# Unit tests
npm test

# Local interface tests
npm run test:local

# Watch mode
npm run test:watch
```

### Test Structure
```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── local/          # PowerShell interface tests
```

### Coverage Requirements
- Minimum 80% code coverage
- All public functions tested
- Error conditions covered
- Edge cases included

## Documentation

### Requirements
- Update README.md for new features
- Add JSDoc comments for new functions
- Update CHANGELOG.md for changes
- Include examples in documentation

### API Documentation
- Use OpenAPI/Swagger for FastAPI endpoints
- Document MCP tool schemas
- Include request/response examples
- Provide troubleshooting guides

## Security Considerations

### Credentials
- Never log or store user credentials
- Use secure parameter passing
- Implement proper session handling
- Follow least privilege principle

### Browser Automation
- Use isolated browser contexts
- Implement proper cleanup
- Handle sensitive data carefully
- Respect platform terms of service

## Performance Guidelines

### MCP Tools
- Respond within 2 seconds for simple operations
- Handle timeouts gracefully
- Implement proper resource cleanup
- Monitor memory usage

### FastAPI Endpoints
- Return appropriate HTTP status codes
- Implement rate limiting where needed
- Use efficient data structures
- Cache results when appropriate

## Release Process

### Versioning
Follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes (backward compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped appropriately
- [ ] Git tag created
- [ ] GitHub release created

## Getting Help

### Issues
- Use GitHub Issues for bugs and feature requests
- Provide detailed reproduction steps
- Include relevant log output
- Specify your environment (OS, Node version, etc.)

### Discussions
- Use GitHub Discussions for questions
- Share ideas and use cases
- Discuss architecture decisions
- Get community help

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors:

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn and contribute
- Maintain professional communication
- Respect differing viewpoints

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

Thank you for contributing to the Suno MCP Server! 🎵🤖
