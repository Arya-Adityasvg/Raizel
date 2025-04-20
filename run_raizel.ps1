# Change to the script directory
Set-Location -Path $PSScriptRoot

# Run the Python script directly
& "$PSScriptRoot\venv\Scripts\python.exe" "$PSScriptRoot\voice_chatbot.py"

# Pause to see any output
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 