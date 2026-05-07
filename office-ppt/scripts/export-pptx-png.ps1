param(
  [Parameter(Mandatory = $true)]
  [string]$Pptx,

  [Parameter(Mandatory = $true)]
  [string]$Out
)

$ErrorActionPreference = "Stop"
$PptxPath = (Resolve-Path $Pptx).Path
$OutDir = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Out)
New-Item -ItemType Directory -Force $OutDir | Out-Null

$powerPoint = $null
$presentation = $null

try {
  $powerPoint = New-Object -ComObject PowerPoint.Application
  $presentation = $powerPoint.Presentations.Open($PptxPath, $true, $false, $false)
  $presentation.Export($OutDir, "PNG", 1920, 1080)

  $index = 1
  Get-ChildItem -LiteralPath $OutDir -Filter "*.PNG" | Sort-Object Name | ForEach-Object {
    $target = Join-Path $OutDir ("slide-{0:D2}.png" -f $index)
    if (Test-Path -LiteralPath $target) {
      Remove-Item -LiteralPath $target -Force
    }
    Move-Item -LiteralPath $_.FullName -Destination $target
    $index++
  }
}
finally {
  if ($presentation) {
    $presentation.Close()
  }
  if ($powerPoint) {
    $powerPoint.Quit()
  }
}
