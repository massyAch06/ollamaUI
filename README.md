# OllamaUI 🤖

A modern, feature-rich user interface for Ollama built with Streamlit. This application provides a sleek, user-friendly way to interact with Ollama's language models through a web interface.

![OllamaUI Screenshot](screenshot.png)

## Features ✨

- **Modern Interface**: Clean and intuitive design with a side navigation system
- **Multiple Conversations**: Manage and switch between different chat conversations
- **Model Selection**: Choose from your installed Ollama models
- **Real-time Streaming**: See responses as they're generated
- **Temperature Control**: Adjust the model's creativity level
- **Chat History**: View and manage your conversation history
- **Status Monitoring**: Real-time connection status and model availability
- **Responsive Design**: Works well on different screen sizes

## Prerequisites 📋

Before running OllamaUI, make sure you have:

1. Python 3.8 or higher installed
2. Ollama installed and running on your system
   - [Install Ollama](https://ollama.ai/download)
   - Run `ollama serve` in a terminal

## Installation 🚀

1. Clone the repository:
   ```bash
   git clone https://github.com/massyAch06/ollamaUI.git
   cd ollama-ui
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage 💻

1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```

2. In a new terminal, start OllamaUI:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501`

## Features Guide 📚

### Navigation
- Use the sidebar tabs to switch between different views:
  - **Chat**: Main conversation interface
  - **Settings**: Configure model parameters
  - **History**: View past conversations

### Chat Interface
- Select a model from the dropdown in the sidebar
- Adjust the temperature slider to control response randomness
- Type your message in the input field at the bottom
- Create new conversations or switch between existing ones

### Settings
- View current model configuration
- Monitor system connection status
- See available models

### History
- Access all your past conversations
- Review previous chats in an organized manner

## Contributing 🤝

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- [Ollama](https://ollama.ai/) for the amazing language model server
- [Streamlit](https://streamlit.io/) for the wonderful web framework

## Support 💪

If you find this project helpful, please give it a ⭐️ on GitHub!

## Contact 📧

For questions, suggestions, or issues, please use the GitHub issues page.

---
Made with ❤️ using Streamlit and Ollama
