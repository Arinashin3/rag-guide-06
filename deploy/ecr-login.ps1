# ECR 로그인 도우미 (Lab 5). 앞의 점(.)과 공백을 붙여서 실행합니다:  . .\deploy\ecr-login.ps1
# 하는 일: ① 내 계정의 ECR 주소를 $env:ECR_REGISTRY 에 담고 ② ECR 에 docker login 합니다.
# docker login 이 "error saving credentials ... stub received bad data" 로 실패하는 PC 를 위해,
# Windows 자격 증명 관리자에 저장하지 않고 이 PowerShell 창에서만 쓰는 Docker 설정 폴더를 사용합니다.
$region = "ap-northeast-2"
$acct = aws sts get-caller-identity --query Account --output text --profile lab-dev --region $region
if (-not $acct) { Write-Host "계정 ID 를 읽지 못했습니다. aws login 상태와 프로필(lab-dev)을 확인하세요."; return }
$env:ECR_REGISTRY = "$acct.dkr.ecr.$region.amazonaws.com"

$cfg = Join-Path $env:TEMP "docker-ecr"
New-Item -ItemType Directory -Force $cfg | Out-Null
Set-Content -Path (Join-Path $cfg "config.json") -Value '{"auths":{}}' -Encoding ascii
$env:DOCKER_CONFIG = $cfg

aws ecr get-login-password --region $region --profile lab-dev | docker login --username AWS --password-stdin $env:ECR_REGISTRY
Write-Host "ECR_REGISTRY = $env:ECR_REGISTRY"
