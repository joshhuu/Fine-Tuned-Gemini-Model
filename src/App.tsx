import React, { useState, useRef } from 'react';
import { Send, Bot, User, Moon, ImagePlus, Mic, X } from 'lucide-react';
import axios from 'axios';

interface Message {
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  image?: string;
}

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    {
      text: "Hello! I'm Zombie. How can I help you today?",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isListening, setIsListening] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);

  // Initialize the Web Speech API
  React.useEffect(() => {
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const SpeechRecognition =
        (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognitionRef.current = recognition;
    } else {
      console.warn('Speech Recognition API not supported in this browser.');
    }
  }, []);

  const handleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert('Voice recognition is not supported in this browser.');
      return;
    }

    const recognition = recognitionRef.current;

    if (isListening) {
      recognition.stop();
      setIsListening(false);
    } else {
      recognition.start();
      setIsListening(true);

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        const transcript = event.results[0][0].transcript;
        setInput((prev) => prev + ' ' + transcript); // Append the spoken text to the input
      };

      recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
        handleSubmit(); // Automatically submit the message after speech ends
      };
    }
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();

    if (!input.trim() && !selectedImage) return;

    const newMessage: Message = {
      text: input,
      sender: 'user',
      timestamp: new Date(),
      image: selectedImage || undefined,
    };

    // Add the user's message to the chat
    setMessages((prev) => [...prev, newMessage]);
    setInput('');
    setSelectedImage(null);

    try {
      // Call the Flask API
      const response = await axios.post('http://127.0.0.1:5000/chat', {
        message: input, // Send the user input to the Flask API
      });

      // Append the bot's response to the chat
      setMessages((prev) => [
        ...prev,
        { text: response.data.response, sender: 'bot', timestamp: new Date() },
      ]);
    } catch (error) {
      console.error('Error communicating with the API:', error);

      // Add an error message to the chat
      setMessages((prev) => [
        ...prev,
        {
          text: 'There was an error processing your request.',
          sender: 'bot',
          timestamp: new Date(),
        },
      ]);
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setSelectedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const removeSelectedImage = () => {
    setSelectedImage(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="container mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="w-6 h-6 text-blue-400" />
            <h1 className="text-xl font-bold">-MULTILINGUAL CHATBOT-</h1>
          </div>
          <Moon className="w-5 h-5 text-gray-400" />
        </div>
      </header>

      {/* Chat Container */}
      <div className="container mx-auto max-w-4xl h-[calc(100vh-8rem)] flex flex-col">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex items-start space-x-2 ${
                message.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''
              }`}
            >
              <div
                className={`p-2 rounded-full ${
                  message.sender === 'user' ? 'bg-blue-600' : 'bg-gray-700'
                }`}
              >
                {message.sender === 'user' ? (
                  <User className="w-5 h-5" />
                ) : (
                  <Bot className="w-5 h-5" />
                )}
              </div>
              <div
                className={`max-w-[80%] p-3 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-blue-600'
                    : 'bg-gray-800 border border-gray-700'
                }`}
              >
                {message.image && (
                  <div className="mb-2">
                    <img
                      src={message.image}
                      alt="Uploaded content"
                      className="max-w-full rounded-lg"
                    />
                  </div>
                )}
                {message.text && <p className="text-sm">{message.text}</p>}
                <span className="text-xs text-gray-400 mt-1 block">
                  {message.timestamp.toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
        </div>

        {/* Input Form */}
        <form
          onSubmit={handleSubmit}
          className="p-4 border-t border-gray-700 bg-gray-800"
        >
          {selectedImage && (
            <div className="mb-2 relative inline-block">
              <img
                src={selectedImage}
                alt="Preview"
                className="h-20 rounded-lg"
              />
              <button
                type="button"
                onClick={removeSelectedImage}
                className="absolute -top-2 -right-2 bg-red-500 rounded-full p-1 hover:bg-red-600 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}
          <div className="flex space-x-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 focus:outline-none focus:border-blue-500 text-gray-100 placeholder-gray-400"
            />
            <input
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              ref={fileInputRef}
              className="hidden"
              id="image-upload"
            />
            <label
              htmlFor="image-upload"
              className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg cursor-pointer flex items-center transition-colors"
            >
              <ImagePlus className="w-4 h-4" />
            </label>
            <button
              type="button"
              onClick={handleVoiceInput}
              className={`${
                isListening ? 'bg-red-600 animate-pulse' : 'bg-green-600'
              } hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors`}
            >
              <Mic className="w-4 h-4" />
            </button>
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
            >
              <Send className="w-4 h-4" />
              <span>Send</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
