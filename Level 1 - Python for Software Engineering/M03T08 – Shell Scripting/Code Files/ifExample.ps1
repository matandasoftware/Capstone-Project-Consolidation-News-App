# If new_folder exists, create if_folder
if (Test-Path -Path "new_folder") {
    New-Item -ItemType Directory -Name "if_folder"
}

# If-else: check if if_folder exists
if (Test-Path -Path "if_folder") {
    New-Item -ItemType Directory -Name "hyperionDev"
} else {
    New-Item -ItemType Directory -Name "new-projects"
}