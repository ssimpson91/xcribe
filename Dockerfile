##docker build -t whisper-app .
##docker run --gpus all whisper-app
##docker run -v /path/to/local/audio:/usr/src/app/audio my-whisper-container
# Use an official PyTorch runtime as a parent image
FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

# Set the working directory in the container
WORKDIR /usr/src/app

# Install ffmpeg and git
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

    
# Use a base Python image with Python 3.8 or higher
FROM python:3.8

# Install Rust non-interactively
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install setuptools-rust, which is required for tiktoken
RUN pip install setuptools-rust

# Install tiktoken from GitHub release
RUN pip install --no-cache-dir git+https://github.com/openai/tiktoken.git@0.3.3

# Install Whisper
RUN pip install --no-cache-dir -U openai-whisper

# Copy the entire current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg && ffmpeg -version
RUN echo $PATH


# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "./transcribe.py"]