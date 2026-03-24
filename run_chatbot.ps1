Write-Host ""
Write-Host "Starting Offline RAG Chatbot..."
Write-Host ""

# Activate virtual environment
& .\venv\Scripts\Activate.ps1

# Run chatbot
python backend/terminal_chat.py