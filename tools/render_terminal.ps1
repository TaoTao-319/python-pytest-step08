param([string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot))

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

function Render-Log {
    param([string]$LogName, [string]$ImageName, [string]$Title, [string]$Accent)
    $logPath = Join-Path $ProjectRoot ('artifacts\' + $LogName)
    $lines = @(Get-Content -LiteralPath $logPath -Encoding UTF8)
    if ($lines.Count -gt 36) {
        $lines = @($lines[0..14]) + @('[... middle output omitted; see the complete text log ...]') + @($lines[($lines.Count - 16)..($lines.Count - 1)])
    }
    $displayLines = foreach ($line in $lines) {
        if ($line.Length -gt 108) {
            for ($offset = 0; $offset -lt $line.Length; $offset += 108) {
                $line.Substring($offset, [Math]::Min(108, $line.Length - $offset))
            }
        } else { $line }
    }
    $width = 1480
    $height = 128 + @($displayLines).Count * 25
    $bitmap = New-Object System.Drawing.Bitmap($width, $height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $graphics.Clear([System.Drawing.ColorTranslator]::FromHtml('#0f172a'))
    $bodyFont = New-Object System.Drawing.Font('Consolas', 15)
    $titleFont = New-Object System.Drawing.Font('Segoe UI', 18, [System.Drawing.FontStyle]::Bold)
    $footerFont = New-Object System.Drawing.Font('Segoe UI', 11)
    $bodyBrush = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#e2e8f0'))
    $accentBrush = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml($Accent))
    $mutedBrush = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#94a3b8'))
    try {
        $graphics.FillRectangle($accentBrush, 0, 0, $width, 5)
        $graphics.DrawString($Title, $titleFont, $accentBrush, 28, 22)
        $row = 72
        foreach ($line in $displayLines) {
            $graphics.DrawString([string]$line, $bodyFont, $bodyBrush, 28, $row)
            $row += 25
        }
        $graphics.DrawString('Rendered from captured output; full text logs are preserved.', $footerFont, $mutedBrush, 28, $height - 35)
        $outputPath = Join-Path $ProjectRoot ('artifacts\' + $ImageName)
        $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        Write-Output $outputPath
    } finally {
        $graphics.Dispose()
        $bitmap.Dispose()
        $bodyFont.Dispose()
        $titleFont.Dispose()
        $footerFont.Dispose()
        $bodyBrush.Dispose()
        $accentBrush.Dispose()
        $mutedBrush.Dispose()
    }
}

Render-Log 'pytest-pass.txt' 'pytest-pass.png' 'pytest | normal test suite' '#34d399'
Render-Log 'pytest-failure.txt' 'pytest-failure.png' 'pytest | isolated assertion failure example' '#fb7185'
