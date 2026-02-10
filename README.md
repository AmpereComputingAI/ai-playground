# Ampere-Optimized AI Playground

The **Ampere Optimized AI Playground** is a Gradio-based interface that allows users to launch and interact with AI demos optimized for Ampere Computing platforms. This project provides a centralized launcher to start and stop six AI demos: LLM Chat with RAG (Ollama), Agentic AI (n8n, Ollama), Object Detection (YOLOv11), Speech-to-Text (Whisper), Text-to-SQL(Ollama, Open-WebUI), and Code Generation (Llama.cpp, Open-WebUI). Each demo runs in a Docker container, managed via Docker Compose, and is accessible through a web interface.

## Features
- **Interactive Gradio UI**: Select and launch demos with a clean, user-friendly interface.
- **Dockerized Demos**: Each demo runs in its own container for isolation and scalability.
- **Optimized for Ampere**: Leverages Ampere Computing's hardware for efficient AI workloads.
- **Easy Start/Stop**: Scripts to start and stop demos with a single command.

## Prerequisites
- **Ubuntu** (Tested on Ubuntu 24.04 or later)
- **Docker** and **Docker Compose** installed
- **Ports 7860-7866** open for the Gradio UI and demo services

## Installation

### 1. Install Docker and Docker Compose on Ubuntu
To set up Docker and Docker Compose, run the following commands in a terminal:

```bash
# Update package index and base image
sudo apt-get update
sudo apt-get upgrade -y

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
# The Docker group should be created when installing the docker-ce package, but if it is not, also run "sudo groupadd docker"
sudo usermod -aG docker $USER
newgrp docker
```

After running these commands, log out and back in to apply the group changes. Verify the installation:

```bash
docker --version
docker compose version
```

### 2. Clone the Repository
Clone this repository to your local machine:

```bash
git clone https://github.com/AmpereComputingAI/ai-playground.git
cd ai-playground
git checkout <latest-release>
```

### 3. Open Firewall Ports
The playground and demos use ports 7860 (Gradio UI), 7861 (Ollama), 7862 (YOLOv11), 7863 (Whisper), 7864 (Agentic AI), 7865 (Text-to-SQL) and 7866 (Code Generation).

In addition, we need to be able to download models from the Internet to the ollama service, which will
require us to NAT traffic from the container bridge network to the host's Ethernet interface.
We accomplish these tasks by using ```firewall-cmd```:

```bash
# Ensure firewalld is installed
sudo apt-get install -y firewalld

# Start and enable firewalld
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Find your Ethernet interface name
ip a

# We are looking for the Ethernet device for the host - in recent Linux distributions, these are commonly
# ethX, or begin with en (usually enp or ens)
#
# Add the Ethernet interface to the public Firewall zone, and enable IP masquerading
sudo firewall-cmd --zone=public --add-interface=<YOUR_ETHERNET_DEVICE_NAME> --permanent
sudo firewall-cmd --zone=public --add-masquerade --permanent

# Open ports 7860-7864
sudo firewall-cmd --permanent --add-port=7860-7866/tcp
sudo firewall-cmd --reload
```

Verify the ports are open, that the Ethernet device is allowed to relay traffic, and that IP Masquerade is set:

```bash
sudo firewall-cmd --list-all
```
### 4. Port Forwarding for Local and Cloud Instances
For **local instances**, access the playground and demos using ```localhost```. For **cloud instances**, use the public IP address of the instance. Ensure ports 7860-7866 are open in your cloud provider's security group or firewall settings.


## Demo Details
This project includes three AI demos, each optimized for Ampere Computing platforms. Below are details and links to their respective GitHub repositories for further information.

### LLM Chat with RAG (Ollama)
- **Description:** A conversational AI demo using the Ollama framework, optimized for Ampere hardware.
- **GitHub Repository:** [Ollama Chat Demo](https://github.com/AmpereComputingAI/ampere-ai-llama-chat/tree/0.0.12)
- **Port:** 7861
- **Access:** Once launched, access at ```http://<host>:7861``` (use ```localhost``` for local setups or the public IP for cloud instances)

### Agentic AI Demo (n8n, Ollama)
- **Description:** Agentic AI Demo with n8n workflow automation tool, Ollama optimized for Ampere hardware.
- **GitHub Repository:** [Agentic AI Demo](https://github.com/AmpereComputingAI/ampere-ai-agents/tree/0.1.1)
- **Port:** 7864
- **Access:** Once launched, access at ```http://<host>:7864``` (use ```localhost``` for local setups or the public IP for cloud instances)

### Object Detection (YOLOv11)
- **Description:** A real-time object detection demo using YOLOv11, optimized for Ampere hardware.
- **GitHub Repository:** [YOLOv11 Demo](https://github.com/AmpereComputingAI/ampere-ai-ref-apps/tree/main/vision/object-detection/YOLOv11)
- **Port:** 7862
- **Access:** Once launched, access at ```http://<host>:7862``` (use ```localhost``` for local setups or the public IP for cloud instances)

### Speech-to-Text (Whisper)
- **Description:** An automatic speech recognition demo using the Whisper model, optimized for Ampere platforms.
- **GitHub Repository:** [Whisper Demo](https://github.com/AmpereComputingAI/ampere-ai-ref-apps/tree/main/audio/automatic-speech-recognition/whisper)
- **Port:** 7863
- **Access:** Once launched, access at ```http://<host>:7863``` (use ```localhost``` for local setups or the public IP for cloud instances)

### Text-to-SQL (Ollama, Open-WebUI)
- **Description:** Turn your natural language questions into executable SQL using Open WebUI and LlamaIndex on Ampere CPUs.
- **GitHub Repository:** [Text-to-SQL Demo](https://github.com/AmpereComputingAI/ampere-ai-text2sql)
- **Port:** 7865
- **Access:** Once launched, access at ```http://<host>:7865``` (use ```localhost``` for local setups or the public IP for cloud instances)

### Code Generation (Llama.cpp, Open-WebUI)
- **Description:** Generate robust Python solutions using AI models on Ampere CPUs.
- **GitHub Repository:** [Code Generation Demo](https://github.com/AmpereComputingAI/ampere-ai-codegen)
- **Port:** 7866
- **Access:** Once launched, access at ```http://<host>:7866``` (use ```localhost``` for local setups or the public IP for cloud instances)

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

Replace ```<host>``` with ```localhost``` for local setups or the public IP address for cloud instances. From the Gradio UI, select a demo (Ollama, Agentic AI, YOLOv11, or Whisper) and click "Launch Demo". The interface will display a link to the live demo (e.g., ```http://<host>:7861``` for Ollama). Click the link to access the running demo.

### Stopping the Demos
To stop all running demos and the playground, use the provided ```stop-app.sh``` script:

```bash
./stop-app.sh
```

This script stops and removes all demo containers, ensuring a clean state for the next run. Alternatively, you can stop demos directly from the Gradio UI by clicking "Stop All Demos".

### Accessing Live Demos
Once a demo is launched via the Gradio UI, the interface will display a confirmation message with a URL to the live demo. For example:
- **Ollama**: ```http://<host>:7861```
- **Agentic AI**: ```http://<host>:7864```
- **YOLOv11**: ```http://<host>:7862```
- **Whisper**: ```http://<host>:7863```
- **Text-to-SQL**: ```http://<host>:7865```
- **Code Generation**: ```http://<host>:7866```

Replace ```<host>``` with ```localhost``` for local setups or the public IP address for cloud instances. Click the provided link in the Gradio UI to access the demo's web interface. It may take a moment for the demo to become available after launching.

## Troubleshooting
- **Port Conflicts**: If ports 7860-7866 are in use, stop conflicting services or change the ports in the ```compose.yaml``` file and update ```app.py``` accordingly.
- **Docker Permissions**: Ensure your user is in the ```docker``` group (```sudo usermod -aG docker $USER```) and log out/in to apply changes.
- **Demo Fails to Launch**: Check Docker logs for the specific service:

```bash
docker logs <service_name>
```
Replace ```<service_name>``` with ```ollama_demo_service```, ```yolo_demo_service```, ```whisper_demo_service```, ```agentic_ai_demo_service```, ```text2sql_demo_service```, or ```codegen_demo_service```.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
