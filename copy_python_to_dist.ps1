$destination = ".\dist\src"
Remove-Item -Path $destination -Recurse -Force
Copy-Item -Path .\src\ -Destination $destination -Recurse -Force

$destination = ".\dist\python_scripts"
Remove-Item -Path $destination -Recurse -Force
Copy-Item -Path .\python_scripts\ -Destination $destination -Recurse -Force