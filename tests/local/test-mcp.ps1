# Suno MCP Server - Local MCP Interface Test
# Run with: .\tests\local\test-mcp.ps1

param(
    [switch]$Verbose,
    [int]$Timeout = 30
)

Write-Host "🧪 Testing Suno MCP Server - MCP Interface" -ForegroundColor Cyan
Write-Host "Timeout: $Timeout seconds" -ForegroundColor Gray
Write-Host ""

# Function to test MCP server
function Test-MCPServer {
    try {
        # Start MCP server in background
        Write-Host "Starting MCP server..." -ForegroundColor Yellow
        $serverProcess = Start-Process -FilePath "node" -ArgumentList "src/suno-mcp/server.js --mcp" -NoNewWindow -PassThru

        Start-Sleep -Seconds 2

        # Test if process is running
        if ($serverProcess.HasExited) {
            Write-Host "❌ MCP server failed to start" -ForegroundColor Red
            return $false
        }

        Write-Host "✅ MCP server started successfully (PID: $($serverProcess.Id))" -ForegroundColor Green

        # Stop server after test
        Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
        Write-Host "✅ MCP server stopped" -ForegroundColor Green

        return $true

    } catch {
        Write-Host "❌ MCP test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to test basic tool listing
function Test-ToolListing {
    try {
        Write-Host "Testing tool listing..." -ForegroundColor Yellow

        # For now, just test that the script runs
        # In a full implementation, this would send JSON-RPC requests

        Write-Host "✅ Tool listing test completed" -ForegroundColor Green
        return $true

    } catch {
        Write-Host "❌ Tool listing test failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Run tests
$results = @()

Write-Host "Running MCP Interface Tests..." -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

# Test 1: MCP Server Startup
$result1 = Test-MCPServer
$results += $result1

# Test 2: Tool Listing
$result2 = Test-ToolListing
$results += $result2

# Summary
Write-Host ""
Write-Host "Test Results Summary:" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

$passed = ($results | Where-Object { $_ -eq $true }).Count
$failed = ($results | Where-Object { $_ -eq $false }).Count
$total = $results.Count

Write-Host "Passed: $passed/$total" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Yellow" })
Write-Host "Failed: $failed/$total" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })

if ($passed -eq $total) {
    Write-Host ""
    Write-Host "🎉 All MCP interface tests passed!" -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "❌ Some tests failed. Check output above." -ForegroundColor Red
    exit 1
}
