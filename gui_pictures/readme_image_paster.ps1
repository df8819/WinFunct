$images = Get-ChildItem -Filter *.png
foreach ($image in $images) {
    Write-Output "![Image](GUI_Pics/$($image.Name))"
}

Write-Output "`nCopy the above lines and paste them into your README.md file."
Write-Output "Remember to adjust the path if necessary, depending on where your README.md is located."
Read-Host -Prompt "Press Enter to exit"
