import gradio as gr
from model import predict_frame

#Build the Gradio UI
with gr.Blocks(title="Real-Time Object Detection") as demo:
    gr.Markdown("# 🚀 Real-Time YOLO11 Object Detection")
    
    with gr.Row():
        with gr.Column():
            # Input webcam component
            input_img = gr.Image(
                sources=["webcam"], 
                type="numpy", 
                label="Webcam Feed", 
                streaming=True  # Enables continuous frame transmission
            )
            
            # Confidence and IoU controls
            conf_slider = gr.Slider(
                minimum=0.0, maximum=1.0, value=0.25, 
                step=0.01, label="Confidence Threshold"
            )
            iou_slider = gr.Slider(
                minimum=0.0, maximum=1.0, value=0.45, 
                step=0.01, label="IoU (Overlap) Threshold"
            )
            
        with gr.Column():
            # Output component to display detected objects
            output_img = gr.Image(label="Detections")

    # Define the streaming logic
    # The stream event triggers every 0.1s by default
    input_img.stream(
        fn=predict_frame, 
        inputs=[input_img, conf_slider, iou_slider], 
        outputs=[output_img],
        stream_every=0.1,  # Adjust frequency (seconds)
        concurrency_limit=10  # Ensures performance under load
    )

if __name__ == "__main__":
    demo.launch()