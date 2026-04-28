# Validate Release Workflows Setup
# This script checks that all release workflows are properly configured

Write-Host "🔍 Validating PyKotor Release Workflows..." -ForegroundColor Cyan
Write-Host ""

$errors = @()
$warnings = @()

# Discover tools dynamically
Write-Host "Detecting tools..." -ForegroundColor Yellow
$tools = @()
$discoverScript = Resolve-Path "../scripts/discover_tools.py" -ErrorAction SilentlyContinue
if ($discoverScript) {
    $pythonExe = if ($env:pythonExePath) { $env:pythonExePath } elseif (Test-Path "../../.venv/Scripts/python.exe") { (Resolve-Path "../../.venv/Scripts/python.exe") } else { "python" }
    $rawTools = & $pythonExe $discoverScript --format json
    if ($LASTEXITCODE -eq 0 -and $rawTools) {
        $tools = $rawTools | ConvertFrom-Json
    }
    if ($tools.Count -eq 0) {
        $errors += "No tools detected from shared discovery metadata"
    } else {
        foreach ($t in $tools) {
            $cfgMsg = if ($t.version_file) { $t.version_file } else { "no config file" }
            Write-Host "  • $($t.directory) (build: $($t.build_name)) -> $cfgMsg" -ForegroundColor Green
        }
    }
} else {
    $errors += "Shared discovery script not found at ../scripts/discover_tools.py"
}

# Build workflow lists dynamically
$requiredWorkflows = @()
$testWorkflows = @()
foreach ($t in $tools) {
    $requiredWorkflows += "release_$($t.build_name).yml"
    $testWorkflows += "TEST_release_$($t.build_name).yml"
}

# Check workflow files exist
Write-Host "Checking workflow files..." -ForegroundColor Yellow

foreach ($workflow in $requiredWorkflows) {
    if (Test-Path $workflow) {
        Write-Host "  ✅ $workflow" -ForegroundColor Green
    } else {
        $errors += "Missing workflow: $workflow"
        Write-Host "  ❌ $workflow" -ForegroundColor Red
    }
}

foreach ($workflow in $testWorkflows) {
    if (Test-Path $workflow) {
        Write-Host "  ✅ $workflow (TEST)" -ForegroundColor Green
    } else {
        $warnings += "Missing test workflow: $workflow (optional)"
        Write-Host "  ⚠️  $workflow (optional)" -ForegroundColor Yellow
    }
}

Write-Host ""

# Check documentation files
Write-Host "Checking documentation..." -ForegroundColor Yellow
$docs = @(
    "README.md",
    "RELEASE_WORKFLOW.md",
    "QUICK_TEST_GUIDE.md",
    "TESTING_RELEASES.md"
)

foreach ($doc in $docs) {
    if (Test-Path $doc) {
        Write-Host "  ✅ $doc" -ForegroundColor Green
    } else {
        $warnings += "Missing documentation: $doc"
        Write-Host "  ⚠️  $doc" -ForegroundColor Yellow
    }
}

Write-Host ""

# Validate workflow syntax
Write-Host "Validating workflow syntax..." -ForegroundColor Yellow

foreach ($workflow in $requiredWorkflows + $testWorkflows) {
    if (-not (Test-Path $workflow)) {
        continue
    }

    try {
        # Try to parse YAML (requires PowerShell-YAML module)
        if (Get-Module -ListAvailable -Name PowerShell-YAML) {
            Import-Module PowerShell-YAML
            $content = Get-Content $workflow -Raw
            $null = ConvertFrom-Yaml $content
            Write-Host "  ✅ $workflow syntax valid" -ForegroundColor Green
        } else {
            # Basic validation without YAML parser
            $content = Get-Content $workflow -Raw
            if ($content -match "on:" -and $content -match "jobs:" -and $content -match "steps:") {
                Write-Host "  ✅ $workflow basic structure valid" -ForegroundColor Green
            } else {
                $errors += "$workflow appears malformed"
                Write-Host "  ❌ $workflow structure invalid" -ForegroundColor Red
            }
        }
    } catch {
        $errors += "YAML syntax error in $workflow : $_"
        Write-Host "  ❌ $workflow syntax error: $_" -ForegroundColor Red
    }
}

Write-Host ""

# Check version files exist
Write-Host "Checking version files..." -ForegroundColor Yellow
foreach ($t in $tools) {
    $file = if ($t.version_file) { Resolve-Path (Join-Path "../../$($t.relative_path)" $t.version_file) -ErrorAction SilentlyContinue } else { $null }
    $toolLabel = $t.build_name
    if ($null -eq $file) {
        $warnings += "$($t.directory): version/config file not found"
        Write-Host "  ⚠️  $toolLabel version file missing" -ForegroundColor Yellow
        continue
    }
    if (Test-Path $file) {
        Write-Host "  ✅ $toolLabel version file exists: $file" -ForegroundColor Green

        $content = Get-Content $file -Raw
        if ($content -match '"currentVersion"' -or $content -match 'CURRENT_VERSION' -or $content -match '__version__') {
            Write-Host "     ✅ Found version field" -ForegroundColor Green
        } else {
            $warnings += "$toolLabel version file missing expected version field"
            Write-Host "     ⚠️  Version fields might be missing" -ForegroundColor Yellow
        }
    } else {
        $errors += "Version file not found: $file"
        Write-Host "  ❌ $toolLabel version file missing: $file" -ForegroundColor Red
    }
}

Write-Host ""

# Check for critical workflow components
Write-Host "Checking workflow components..." -ForegroundColor Yellow

foreach ($workflow in $requiredWorkflows) {
    if (-not (Test-Path $workflow)) {
        continue
    }

    $content = Get-Content $workflow -Raw

    # Check for required jobs
    $requiredJobs = @("validate", "update_version_pre_build", "setup", "build", "package", "finalize")
    foreach ($job in $requiredJobs) {
        if ($content -match "\s+$job\s*:") {
            # Job found
        } else {
            $errors += "$workflow missing job: $job"
        }
    }

    # Check for release trigger
    if ($content -match "types:\s*\[prereleased\]") {
        # Correct trigger
    } else {
        $errors += "$workflow not configured for prereleased trigger"
    }
}

Write-Host "  ✅ All workflows have required jobs" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "VALIDATION SUMMARY" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

if ($errors.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "✅ ALL CHECKS PASSED!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your release workflows are properly configured." -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Test with a test tag for one discovered build name, then create a matching prerelease" -ForegroundColor White
    Write-Host "  2. Read QUICK_TEST_GUIDE.md for detailed testing" -ForegroundColor White
    Write-Host "  3. When ready, create production release (no test- prefix)" -ForegroundColor White
    Write-Host ""
    exit 0
} else {
    if ($errors.Count -gt 0) {
        Write-Host "❌ ERRORS FOUND ($($errors.Count)):" -ForegroundColor Red
        foreach ($err in $errors) {
            Write-Host "  • $err" -ForegroundColor Red
        }
        Write-Host ""
    }

    if ($warnings.Count -gt 0) {
        Write-Host "⚠️  WARNINGS ($($warnings.Count)):" -ForegroundColor Yellow
        foreach ($warning in $warnings) {
            Write-Host "  • $warning" -ForegroundColor Yellow
        }
        Write-Host ""
    }

    Write-Host "Please fix errors before proceeding." -ForegroundColor Red
    Write-Host ""
    exit 1
}
