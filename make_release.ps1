# WorldTamerCNTr - 构建脚本
# 从 chinese_simp/（唯一真源）生成两个发布版本的 zip
#
# 深度翻译 = chinese_simp 全量
# 流畅翻译 = chinese_simp 去掉深度版专有的 6 个文件
#
# 用法：双击 make_release.bat，或右键本文件「使用 PowerShell 运行」

$ErrorActionPreference = "Stop"

# 先加载 zip 相关程序集（后面的 New-Object / 方法调用依赖它）
Add-Type -AssemblyName System.IO.Compression.FileSystem

$root = $PSScriptRoot
$src  = Join-Path $root "chinese_simp"
$docs = Join-Path $root "release_docs"
$out  = Join-Path $root "build"

if (-not (Test-Path $src))  { throw "找不到 $src" }
if (-not (Test-Path $docs)) { throw "找不到 $docs" }

if (Test-Path $out) { Remove-Item $out -Recurse -Force }
New-Item -ItemType Directory -Path $out -Force | Out-Null

# 深度版专有文件：流畅翻译版需要剔除
$deepOnly = @(
    "forcechange.rpy",
    "name.rpy",
    "replace_cn.rpy",
    "NotoSerifCJKsc-Bold.otf",
    "OFL.txt",
    "FONT-NOTICE.txt"
)

# ---- 深度翻译：全量 ----
$deep = Join-Path $out "深度翻译"
New-Item -ItemType Directory -Path (Join-Path $deep "chinese_simp") -Force | Out-Null
Copy-Item (Join-Path $src "*") (Join-Path $deep "chinese_simp") -Recurse -Force
Copy-Item (Join-Path $docs "说明.txt")     $deep -Force
Copy-Item (Join-Path $docs "更新日志.txt") $deep -Force

# ---- 流畅翻译：剔除深度版专有文件 ----
$lite = Join-Path $out "流畅翻译"
New-Item -ItemType Directory -Path (Join-Path $lite "chinese_simp") -Force | Out-Null
Copy-Item (Join-Path $src "*") (Join-Path $lite "chinese_simp") -Recurse -Force
foreach ($f in $deepOnly) {
    $p = Join-Path $lite "chinese_simp\$f"
    if (Test-Path $p) { Remove-Item $p -Force }
}
Copy-Item (Join-Path $docs "说明.txt")     $lite -Force
Copy-Item (Join-Path $docs "字体说明.txt") $lite -Force

# ---- 打包 ----
# 不用 [System.IO.Compression.ZipFile]::CreateFromDirectory：
# Windows PowerShell 5.1 跑在 .NET Framework 上，它会把条目名写成反斜杠
# （"深度翻译\chinese_simp\x.rpy"），不符合 ZIP 规范，部分解压工具和
# GitHub 的 zip 预览会解析异常。这里手动写入正斜杠。
#
# 另外这里刻意不写 [System.IO.Compression.ZipArchiveMode] 之类的类型字面量：
# 用 -File 执行脚本时类型字面量在编译期解析，Add-Type 来不及生效。
# 枚举参数一律传字符串，交给 PowerShell 的绑定器转换。
function New-VariantZip {
    param(
        [string]$BuildDir,
        [string]$Variant,
        [string]$ZipPath
    )

    if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }

    $base   = (Resolve-Path $BuildDir).Path.TrimEnd('\')
    $prefix = $Variant + '/'

    # 用 ZipFile.Open（在 System.IO.Compression.FileSystem 里，肯定已加载），
    # 避免直接引用 System.IO.Compression 里的 zip 类型。
    $zip = [System.IO.Compression.ZipFile]::Open($ZipPath, "Create")
    try {
        Get-ChildItem (Join-Path $BuildDir $Variant) -Recurse -File | ForEach-Object {
            $rel = $_.FullName.Substring($base.Length + 1) -replace '\\', '/'
            if (-not $rel.StartsWith($prefix)) { return }

            $entry = $zip.CreateEntry($rel, "Optimal")
            $es = $entry.Open()
            try {
                $in = [System.IO.File]::OpenRead($_.FullName)
                try { $in.CopyTo($es) } finally { $in.Dispose() }
            } finally { $es.Dispose() }
        }
    } finally { $zip.Dispose() }
}

foreach ($v in @("深度翻译", "流畅翻译")) {
    New-VariantZip -BuildDir $out -Variant $v -ZipPath (Join-Path $out "WorldTamer-中文-$v.zip")
}

Write-Host ""
Write-Host "构建完成，输出在 build\ 下：" -ForegroundColor Green
Get-ChildItem $out -Filter *.zip |
    Select-Object Name, @{ n = "大小(MB)"; e = { [math]::Round($_.Length / 1MB, 2) } } |
    Format-Table -AutoSize
