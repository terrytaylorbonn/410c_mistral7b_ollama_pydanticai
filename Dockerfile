FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget ca-certificates file && \
    rm -rf /var/lib/apt/lists/*

# Download llamafile
RUN wget https://github.com/Mozilla-Ocho/llamafile/releases/download/0.9.3/llamafile-0.9.3 && \
    chmod +x llamafile-0.9.3

# Download TinyLlama model (example: Q4_K_M quantization)
RUN wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -O tinyllama.gguf

# Set entrypoint to run llamafile with the model
ENTRYPOINT ["./llamafile-0.9.3", "-m", "tinyllama.gguf"]
