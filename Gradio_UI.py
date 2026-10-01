"""A minimal Gradio chat interface for a smolagents agent."""

import gradio as gr


class GradioUI:
    def __init__(self, agent, file_upload_folder: str | None = None):
        self.agent = agent
        self.file_upload_folder = file_upload_folder

    def interact_with_agent(self, prompt, history):
        try:
            response = self.agent.run(prompt)
        except Exception as e:
            response = f"Error: {e}"
        history = history + [(prompt, str(response))]
        return history, history

    def launch(self, **kwargs):
        with gr.Blocks() as demo:
            gr.Markdown("# Hugging Face AI Agent")
            chatbot = gr.Chatbot()
            msg = gr.Textbox(label="Ask the agent something")
            clear = gr.Button("Clear")

            def respond(message, chat_history):
                chat_history, _ = self.interact_with_agent(message, chat_history)
                return "", chat_history

            msg.submit(respond, [msg, chatbot], [msg, chatbot])
            clear.click(lambda: None, None, chatbot, queue=False)

        demo.launch(**kwargs)
