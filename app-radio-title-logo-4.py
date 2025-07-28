# launcher/launcher.py
import gradio as gr
import docker
import time

# --- Configuration ---
DEMOS = {
    "Object Detection (YOLO)": {
        "service_name": "yolo_demo_service",
        "url": "http://localhost:7861"
    },
    "Speech-to-Text (Whisper)": {
        "service_name": "whisper_demo_service",
        "url": "http://localhost:7862"
    },
    "LLM Chat (Ollama)": {
        "service_name": "llmchat_demo_service",
        "url": "http://localhost:7863"
    }
}

# --- State & Docker Client ---
# Initialize the Docker client from the environment (which includes the mounted socket)
client = docker.from_env()
# A simple way to track the currently running container object
current_container = None

def get_running_container(service_name):
    """Check if a container for a given service is running."""
    try:
        return client.containers.get(service_name)
    except docker.errors.NotFound:
        return None

def stop_all_demos():
    """Stops any running demo container managed by this launcher."""
    global current_container
    print("Stopping all demos...")
    for demo_info in DEMOS.values():
        container_to_stop = get_running_container(demo_info['service_name'])
        if container_to_stop:
            print(f"Stopping {demo_info['service_name']}...")
            container_to_stop.stop()
            container_to_stop.remove() # Remove to ensure a clean start next time
            print(f"{demo_info['service_name']} stopped.")

            # Stop and remove dependent ollama container
            if demo_info['service_name'] == 'llmchat_demo_service':
                cont_name = 'ollama_demo_service'
                container_to_stop = get_running_container(cont_name)
                if container_to_stop:
                    print(f"Stopping {cont_name}...")
                    container_to_stop.stop()
                    container_to_stop.remove() # Remove to ensure a clean start next time
                    print(f"{cont_name} stopped.")

    current_container = None
    return "All demos have been stopped."

def launch_demo(demo_name):
    """
    Launches the selected demo container and stops any other.
    """
    global current_container

    # 1. Stop any running demos first.
    stop_all_demos()
    time.sleep(2) # Give a moment for ports to free up.

    if not demo_name:
        return "Please select a demo to launch."

    # 2. Start the selected demo container.
    service_name = DEMOS[demo_name]['service_name']
    demo_url = DEMOS[demo_name]['url']

    print(f"Attempting to launch {service_name}...")
    try:
        # The docker-compose file has all the config (image, ports, network).
        # We just need to tell docker-compose to start the service.
        # A more direct approach is to run the container using the client with configs.
        # For simplicity with docker-compose definitions, we can use `compose.up`
        # but a more robust way is to re-create the container from its image.
        
        # We will use the docker client to start the service defined in compose
        # This assumes images are pre-built or pulled.
        # Note: `docker-compose up -d <service>` is easier but this is the Pythonic way.
        
        # The easiest method is to simply use subprocess to call docker-compose
        import subprocess
        subprocess.run(["docker", "compose", "up", "-d", service_name], check=True)
        #subprocess.run(["./yolo_demo_service.sh"], check=True)
        current_container = client.containers.get(service_name)

        return (
            f"✅ **{demo_name} is starting!** It may take a moment to become available.\n\n"
            f"Access it here: [{demo_url}]({demo_url})"
        )
    except Exception as e:
        print(f"Error launching {service_name}: {e}")
        return f"❌ Error launching {demo_name}. Check logs for details."

# --- Gradio Interface ---
with gr.Blocks(theme=gr.themes.Soft(), css=".centered-title { text-align: center; flex: 0 0 80%; } .header-row { display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 20px; } .logo-container { flex: 0 0 20%; }") as demo_launcher:
    with gr.Row(elem_classes=["header-row"]):
        gr.Image("ampere_logo_1530x780.png", width=80, height=40, show_label=False, container=False, elem_classes=["logo-container"])
        gr.Markdown(
            "# Ampere Optimized AI Playground",
            elem_classes=["centered-title"]
        )
    
    with gr.Column():
        status_output = gr.Markdown("Select a demo and click launch.")
        demo_selection = gr.Radio(choices=list(DEMOS.keys()), label="Available Demos")
        with gr.Row():
            launch_button = gr.Button("🚀 Launch Demo", variant="primary")
            stop_button = gr.Button("⏹️ Stop All Demos")

    launch_button.click(fn=launch_demo, inputs=demo_selection, outputs=status_output)
    stop_button.click(fn=stop_all_demos, inputs=None, outputs=status_output)

if __name__ == "__main__":
    # Clean up on initial start
    stop_all_demos()
    demo_launcher.launch(server_name="0.0.0.0", server_port=7860)
