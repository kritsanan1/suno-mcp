# Suno MCP Server - Local FastAPI Interface Test
# Run with: .\tests\local\test-api.ps1

param(
    [switch]$Verbose,
    [int]$Timeout = 30,
    [int]$Port = 8000
)

Write-Host "🧪 Testing Suno MCP Server - FastAPI Interface" -ForegroundColor Cyan
Write-Host "Port: $Port, Timeout: $Timeout seconds" -ForegroundColor Gray
Write-Host ""

# Function to test health endpoint
function Test-HealthEndpoint {
    param([string]$BaseUrl)

    try {
        Write-Host "Testing /health endpoint..." -ForegroundColor Yellow

        $response = Invoke-RestMethod -Uri "$BaseUrl/health" -Method GET -TimeoutSec $Timeout

        if ($response.status -eq "healthy") {
            Write-Host "✅ Health check passed: $($response.status)" -ForegroundColor Green
            if ($Verbose) {
                Write-Host "   Version: $($response.version)" -ForegroundColor Gray
                Write-Host "   Uptime: $([math]::Round($response.uptime, 2)) seconds" -ForegroundColor Gray
            }
            return $true
        } else {
            Write-Host "❌ Health check failed: $($response.status)" -ForegroundColor Red
            return $false
        }

    } catch {
        Write-Host "❌ Health endpoint test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to test API v1 tools endpoint
function Test-ToolsEndpoint {
    param([string]$BaseUrl)

    try {
        Write-Host "Testing /api/v1/tools endpoint..." -ForegroundColor Yellow

        $response = Invoke-RestMethod -Uri "$BaseUrl/api/v1/tools" -Method GET -TimeoutSec $Timeout

        if ($response.count -eq 24) {
            Write-Host "✅ Tools endpoint passed: $($response.count) tools available" -ForegroundColor Green
            if ($Verbose) {
                Write-Host "   Sample tools:" -ForegroundColor Gray
                $response.tools | Select-Object -First 3 | ForEach-Object {
                    Write-Host "   - $($_.name)" -ForegroundColor Gray
                }
            }
            return $true
        } else {
            Write-Host "❌ Tools endpoint failed: Expected 24 tools, got $($response.count)" -ForegroundColor Red
            return $false
        }

    } catch {
        Write-Host "❌ Tools endpoint test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to test API v1 status endpoint
function Test-StatusEndpoint {
    param([string]$BaseUrl)

    try {
        Write-Host "Testing /api/v1/status endpoint..." -ForegroundColor Yellow

        $response = Invoke-RestMethod -Uri "$BaseUrl/api/v1/status" -Method GET -TimeoutSec $Timeout

        if ($response.status -eq "running") {
            Write-Host "✅ Status endpoint passed: $($response.status)" -ForegroundColor Green
            if ($Verbose) {
                Write-Host "   Tools: $($response.tools.total) total ($($response.tools.basic) basic + $($response.tools.studio) studio)" -ForegroundColor Gray
            }
            return $true
        } else {
            Write-Host "❌ Status endpoint failed: $($response.status)" -ForegroundColor Red
            return $false
        }

    } catch {
        Write-Host "❌ Status endpoint test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to test tool execution endpoint
function Test-ToolExecution {
    param([string]$BaseUrl)

    try {
        Write-Host "Testing tool execution endpoint..." -ForegroundColor Yellow

        $body = @{
            headless = $true
        } | ConvertTo-Json

        $response = Invoke-RestMethod -Uri "$BaseUrl/api/v1/tools/suno_open_browser" -Method POST -Body $body -ContentType "application/json" -TimeoutSec $Timeout

        if ($response.success -and $response.executed_via -eq "fastapi") {
            Write-Host "✅ Tool execution test passed" -ForegroundColor Green
            if ($Verbose) {
                Write-Host "   Tool: $($response.tool)" -ForegroundColor Gray
                Write-Host "   Via: $($response.executed_via)" -ForegroundColor Gray
            }
            return $true
        } else {
            Write-Host "❌ Tool execution test failed" -ForegroundColor Red
            return $false
        }

    } catch {
        Write-Host "❌ Tool execution test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to start and test FastAPI server
function Test-FastAPIServer {
    try {
        # Start FastAPI server in background
        Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
        $serverProcess = Start-Process -FilePath "node" -ArgumentList "src/suno-mcp/server.js" -NoNewWindow -PassThru

        # Wait for server to start
        Start-Sleep -Seconds 3

        # Test if process is running
        if ($serverProcess.HasExited) {
            Write-Host "❌ FastAPI server failed to start" -ForegroundColor Red
            return $false
        }

        $baseUrl = "http://localhost:$Port"

        # Run endpoint tests
        $results = @(
            (Test-HealthEndpoint -BaseUrl $baseUrl),
            (Test-ToolsEndpoint -BaseUrl $baseUrl),
            (Test-StatusEndpoint -BaseUrl $baseUrl),
            (Test-ToolExecution -BaseUrl $baseUrl)
        )

        # Stop server
        Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
        Write-Host "✅ FastAPI server stopped" -ForegroundColor Green

        # Return overall result
        return -not ($results -contains $false)

    } catch {
        Write-Host "❌ FastAPI server test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Run tests
Write-Host "Running FastAPI Interface Tests..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$result = Test-FastAPIServer

# Summary
Write-Host ""
Write-Host "FastAPI Interface Test Results:" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan

if ($result) {
    Write-Host "✅ All FastAPI interface tests passed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 FastAPI server endpoints verified:" -ForegroundColor Cyan
    Write-Host "   • /health - Health check" -ForegroundColor White
    Write-Host "   • /api/v1/tools - Tool listing" -ForegroundColor White
    Write-Host "   • /api/v1/status - Server status" -ForegroundColor White
    Write-Host "   • /api/v1/tools/:name - Tool execution" -ForegroundColor White
    exit 0
} else {
    Write-Host "❌ FastAPI interface tests failed. Check output above." -ForegroundColor Red
    exit 1
}
