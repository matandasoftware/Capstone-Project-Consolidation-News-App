# Create three new folders
New-Item -ItemType Directory -Name "FolderA"
New-Item -ItemType Directory -Name "FolderB"
New-Item -ItemType Directory -Name "FolderC"

# Navigate into FolderA
Set-Location "FolderA"

# Create three new folders inside FolderA
New-Item -ItemType Directory -Name "SubFolder1"
New-Item -ItemType Directory -Name "SubFolder2"
New-Item -ItemType Directory -Name "SubFolder3"

# Go back to parent directory
Set-Location ..

# Remove FolderB and FolderC
Remove-Item -Recurse -Force "FolderB"
Remove-Item -Recurse -Force "FolderC"