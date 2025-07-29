# Ampere-Optimized AI Playground

The **Ampere Optimized AI Playground** is a Gradio-based interface that allows users to launch and interact with AI demos optimized for Ampere Computing platforms. This project provides a centralized launcher to start and stop three AI demos: LLM Chat with RAG (Ollama), Object Detection (YOLOv11), and Speech-to-Text (Whisper). Each demo runs in a Docker container, managed via Docker Compose, and is accessible through a web interface.

## Features
- **Interactive Gradio UI**: Select and launch demos with a clean, user-friendly interface.
- **Dockerized Demos**: Each demo runs in its own container for isolation and scalability.
- **Optimized for Ampere**: Leverages Ampere Computing's hardware for efficient AI workloads.
- **Easy Start/Stop**: Scripts to start and stop demos with a single command.

## Prerequisites
- **Ubuntu** (Tested on Ubuntu 24.04 or later)
- **Docker** and **Docker Compose** installed
- **Ports 7860-7863** open for the Gradio UI and demo services

## Installation

### 1. Install Docker and Docker Compose on Ubuntu
To set up Docker and Docker Compose, run the following commands in a terminal:

```bash
# Update package index
sudo apt-get update

# Install prerequisites
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to Docker group to run Docker without sudo
sudo usermod -aG docker $USER
newgrp docker
```

After running these commands, log out and back in to apply the group changes. Verify the installation:

```bash
docker --version
docker compose --version
```

### 2. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/AmpereComputingAI/ampere-ai-playground.git
cd ampere-ai-playground
```

### 3. Open Firewall Ports
The playground and demos use ports 7860 (Gradio UI), 7861 (Ollama), 7862 (YOLOv11), and 7863 (Whisper). Open these ports using ```firewall-cmd```:

```bash
# Ensure firewalld is installed
sudo apt-get install -y firewalld

# Start and enable firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Open ports 7860-7863
sudo firewall-cmd --permanent --add-port=7860-7863/tcp
sudo firewall-cmd --reload
```

Verify the ports are open:

```bash
sudo firewall-cmd --list-ports
```
### 4. Port Forwarding for Local and Cloud Instances
For **local instances**, access the playground and demos using ```localhost```. For **cloud instances**, use the public IP address of the instance. Ensure ports 7860-7863 are open in your cloud provider's security group or firewall settings.


## Demo Details
This project includes three AI demos, each optimized for Ampere Computing platforms. Below are details and links to their respective GitHub repositories for further information.

### LLM Chat with RAG (Ollama)
- **Description:** A conversational AI demo using the Ollama framework, optimized for Ampere hardware.
- **GitHub Repository:** Ollama Chat Demo
- **Port:** 7861
- **Access:** Once launched, access at ```http://<host>:7861``` (use ```localhost``` for local setups or the public IP for cloud instances)

### Object Detection (YOLOv11)
- **Description:** A real-time object detection demo using YOLOv11, optimized for Ampere hardware.
- **GitHub Repository:** YOLOv11 Demo
- **Port:** 7862
- **Access:** Once launched, access at ```http://<host>:7862``` (use ```localhost``` for local setups or the public IP for cloud instances)

### Speech-to-Text (Whisper)
- **Description:** An automatic speech recognition demo using the Whisper model, optimized for Ampere platforms.
- **GitHub Repository:** Whisper Demo
- **Port:** 7863
- **Access:** Once launched, access at ```http://<host>:7863``` (use ```localhost``` for local setups or the public IP for cloud instances)

## Running the Playground
### Starting the Playground
To start the Ampere Optimized AI Playground, use the provided ```start-app.sh``` script:
```bash
./start-app.sh
```
This script launches the Gradio interface, which allows you to select and start one of the demos. The interface runs on port 7860.

### Accessing the Playground
Once the playground is launched, open your web browser and navigate to:

```
http://<host>:7860
```

Replace ```<host>``` with ```localhost``` for local setups or the public IP address for cloud instances. From the Gradio UI, select a demo (Ollama, YOLOv11, or Whisper) and click "Launch Demo". The interface will display a link to the live demo (e.g., ```http://<host>:7861``` for Ollama). Click the link to access the running demo.

### Stopping the Demos
To stop all running demos and the playground, use the provided ```stop-app.sh``` script:

```bash
./stop-app.sh
```

This script stops and removes all demo containers, ensuring a clean state for the next run. Alternatively, you can stop demos directly from the Gradio UI by clicking "Stop All Demos".

### Accessing Live Demos
Once a demo is launched via the Gradio UI, the interface will display a confirmation message with a URL to the live demo. For example:
- **Ollama**: ```http://<host>:7861```
- **YOLOv11**: ```http://<host>:7862```
- **Whisper**: ```http://<host>:7863```

Replace ```<host>``` with ```localhost``` for local setups or the public IP address for cloud instances. Click the provided link in the Gradio UI to access the demo's web interface. It may take a moment for the demo to become available after launching.

## Troubleshooting
- **Port Conflicts**: If ports 7860-7863 are in use, stop conflicting services or change the ports in the ```compose.yaml``` file and update ```app.py``` accordingly.
- **Docker Permissions**: Ensure your user is in the ```docker``` group (```sudo usermod -aG docker $USER```) and log out/in to apply changes.
- **Demo Fails to Launch**: Check Docker logs for the specific service:

```bash
docker logs <service_name>
```
Replace ```<service_name>``` with ```ollama_demo_service```, ```yolo_demo_service```, or ```whisper_demo_service```.

## License
This project is licensed under the MIT License. See the LICENSE file for details.








