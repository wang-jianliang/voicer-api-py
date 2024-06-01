from gradio_client import Client

client = Client("Dzkaka/ChatTTS")
result = client.predict(
		text="四川美食确实以辣闻名，但也有不辣的选择。比如甜水面、赖汤圆、蛋烘糕、叶儿粑等，这些小吃口味温和，甜而不腻，也很受欢迎。",
		temperature=0.3,
		top_P=0.7,
		top_K=20,
		audio_seed_input=42,
		text_seed_input=42,
		refine_text_flag=True,
		api_name="/generate_audio"
)
print(result)
