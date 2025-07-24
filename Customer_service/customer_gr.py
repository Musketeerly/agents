import gradio as gr
from dotenv import load_dotenv
from customer_agent import customer

load_dotenv(override=True)





with gr.Blocks(theme=gr.themes.Soft(primary_hue="sky")) as chatbot_ui:
    gr.Markdown(
        """
        <div style="display: flex; align-items: center; gap: 16px;">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" width="60" style="border-radius: 50%; border: 2px solid #38bdf8;">
            <div>
                <h1 style="margin-bottom: 0; color: #0ea5e9;">Musketeerly AI Customer Service</h1>
                <p style="margin-top: 4px; color: #64748b;">Your friendly AI assistant for all Musketeerly support needs.</p>
            </div>
        </div>
        """,
        elem_id="header"
    )

    chatbot = gr.Chatbot(
        label="Musketeerly AI Support Chat",
        avatar_images=("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", None),
        bubble_full_width=False,
        show_copy_button=True,
        height=420,
        show_label=False,
        render_markdown=True,
    )

    with gr.Row():
        user_input = gr.Textbox(
            show_label=False,
            placeholder="Type your question or request here...",
            scale=8,
            container=False,
            autofocus=True,
        )
        send_btn = gr.Button("Send", variant="primary", scale=1)

    gr.Markdown(
        """
        <div style="text-align: center; color: #94a3b8; font-size: 0.95em; margin-top: 16px;">
            Powered by <b>Musketeerly AI</b> | For urgent issues, please contact <a href="mailto:support@musketeerly.com">support@musketeerly.com</a>
        </div>
        """,
        elem_id="footer"
    )

    def chat_interface(history, message):
        # history: list of [user, ai] pairs
        if history is None:
            history = []
        # Add user message
        history = history + [[message, None]]
        # Get AI response (awaitable)
        import asyncio
        ai_response = asyncio.run(customer(message))
        # Add AI response
        history[-1][1] = ai_response
        return history, ""

    send_btn.click(
        chat_interface,
        inputs=[chatbot, user_input],
        outputs=[chatbot, user_input]
    )
    user_input.submit(
        chat_interface,
        inputs=[chatbot, user_input],
        outputs=[chatbot, user_input]
    )

chatbot_ui.launch(inbrowser=True)


