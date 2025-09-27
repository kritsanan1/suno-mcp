# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in the Suno MCP Server, please report it to us as follows:

### Contact Information
- **Email**: security@suno-mcp.dev (placeholder - update with actual contact)
- **GitHub Security Advisories**: [Report via GitHub](https://github.com/sandraschi/suno-mcp/security/advisories/new)
- **Response Time**: We aim to respond within 48 hours

### What to Include
Please include the following information in your report:
- A clear description of the vulnerability
- Steps to reproduce the issue
- Potential impact and severity
- Any suggested fixes or mitigations
- Your contact information for follow-up

### Our Process
1. **Acknowledgment**: We'll acknowledge receipt within 48 hours
2. **Investigation**: We'll investigate and validate the vulnerability
3. **Fix Development**: We'll develop and test a fix
4. **Disclosure**: We'll coordinate disclosure timing with you
5. **Release**: We'll release the fix and security advisory

## Security Considerations

### Browser Automation Security
- **Isolated Sessions**: Each automation session runs in isolated browser contexts
- **No Credential Storage**: User credentials are never stored or logged
- **Secure Parameter Passing**: Credentials are passed securely through tool parameters
- **Session Cleanup**: Browser sessions are properly cleaned up after use

### Network Security
- **HTTPS Only**: All connections use HTTPS encryption
- **API Security**: FastAPI endpoints follow security best practices
- **Rate Limiting**: Implemented where appropriate to prevent abuse
- **Input Validation**: All inputs are validated and sanitized

### Data Protection
- **No Personal Data Storage**: The server doesn't store personal information
- **Ephemeral Sessions**: Session data is temporary and cleaned up
- **Minimal Data Retention**: Only essential data is retained temporarily
- **GDPR Compliance**: Follows data protection principles

### Platform Compliance
- **Suno Terms**: Respects Suno AI's terms of service
- **MCP Standards**: Follows Model Context Protocol security guidelines
- **Claude Desktop**: Compatible with Anthropic's security requirements
- **Open Source**: Transparent security practices

## Known Security Limitations

### Current Limitations
1. **Browser Automation**: Relies on Playwright's security model
2. **API Dependencies**: Security depends on external API providers
3. **User Responsibility**: Users must secure their own Claude Desktop installations
4. **Network Dependencies**: Requires internet access for functionality

### Mitigations
- Regular dependency updates
- Security-focused code reviews
- Automated security testing
- Transparent logging practices

## Security Best Practices for Users

### Installation
- Install from official sources only
- Verify package integrity
- Keep dependencies updated
- Use secure network connections

### Configuration
- Use strong, unique credentials for Suno AI
- Configure Claude Desktop securely
- Limit network access if possible
- Regularly rotate API keys/tokens

### Operation
- Monitor for unusual activity
- Keep logs secure but accessible for debugging
- Report suspicious behavior
- Use in trusted environments

### Data Handling
- Don't share session logs publicly
- Secure any exported audio files
- Be aware of Suno AI's data usage policies
- Understand that AI-generated content may have usage restrictions

## Security Updates

### Update Process
- Security patches are released as soon as possible
- Critical vulnerabilities get immediate hotfixes
- All updates are documented in CHANGELOG.md
- Users are notified through GitHub releases

### Versioning
- Security fixes follow semantic versioning
- PATCH versions for security fixes
- MINOR versions for new features
- MAJOR versions for breaking changes

## Incident Response

### In Case of Breach
1. **Immediate Response**: Shut down affected systems
2. **Investigation**: Analyze the incident thoroughly
3. **Communication**: Notify affected users promptly
4. **Recovery**: Implement fixes and security improvements
5. **Prevention**: Update security measures

### Post-Incident
- Full incident report published
- Security improvements implemented
- User communication maintained
- Lessons learned documented

## Third-Party Dependencies

### Security Monitoring
- Dependencies are regularly audited
- Security vulnerabilities are tracked
- Updates are applied promptly
- Breaking changes are tested thoroughly

### Critical Dependencies
- **@modelcontextprotocol/sdk**: MCP protocol implementation
- **playwright**: Browser automation framework
- **fastify**: HTTP server framework
- **zod**: Input validation library

## Contact

For security-related questions or concerns:
- **Security Issues**: Use GitHub Security Advisories
- **General Questions**: Create GitHub Issues
- **Email**: security@suno-mcp.dev (placeholder)

## Acknowledgments

We appreciate the security research community for helping keep open source software secure. Responsible disclosure is greatly appreciated and will be acknowledged in security advisories.

---

*This security policy is reviewed and updated regularly to ensure the continued security of the Suno MCP Server.*
