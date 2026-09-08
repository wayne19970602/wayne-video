$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
$FfmpegBin = Join-Path $ProjectRoot 'tools\ffmpeg\bin'

if (-not (Test-Path -LiteralPath $VenvPython)) {
  throw "项目虚拟环境不存在: $VenvPython"
}
if (-not (Test-Path -LiteralPath (Join-Path $FfmpegBin 'ffmpeg.exe'))) {
  throw "项目 FFmpeg 不存在: $FfmpegBin"
}

$env:PATH = "$FfmpegBin;$env:PATH"
$env:DAIHUO_JY_PYTHON = $VenvPython
$env:DAIHUO_JY_DRAFTS = Join-Path $env:LOCALAPPDATA 'JianyingPro\User Data\Projects\com.lveditor.draft'
$env:PYTHONUTF8 = '1'

& $VenvPython (Join-Path $ProjectRoot 'doctor.py')
exit $LASTEXITCODE
