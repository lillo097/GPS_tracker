from pyngrok import ngrok

# Chiude tutti i tunnel attivi
ngrok.kill()
print("Tutti i tunnel Ngrok sono stati chiusi.")
