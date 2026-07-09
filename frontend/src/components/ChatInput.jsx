import { useState, useContext } from "react";
import UploadButton from "./UploadButton";
import {
    FaPaperclip,
    FaImage,
    FaPaperPlane
} from "react-icons/fa";

import { ChatContext } from "../context/ChatContext";

import { sendMessage } from "../services/api";

function ChatInput() {

    const [question, setQuestion] = useState("");

    const {

    messages,

    setMessages,

    loading,

    setLoading

} = useContext(ChatContext);

    async function handleSend() {

        if (!question.trim()) return;

        const userMessage = {
            role: "user",
            content: question
        };

        setMessages(prev => [...prev, userMessage]);

        setLoading(true);

        try {

            const response = await sendMessage(question);

            const aiMessage = {

                role: "assistant",

                content: response.answer,

                sources: response.sources || [],

                graph: response.graph || null,

                figure: response.figure || null

            };

            setMessages(prev => [...prev, aiMessage]);

        }

        catch (error) {

            setMessages(prev => [

                ...prev,

                {

                    role: "assistant",

                    content: "Unable to connect to backend."

                }

            ]);

        }

        setQuestion("");

        setLoading(false);

    }

    return (

        <div className="border-t border-slate-700 p-5 bg-slate-800">

            <div className="max-w-5xl mx-auto flex items-center gap-3">

                <UploadButton />

                <input

                    value={question}

                    onChange={(e)=>setQuestion(e.target.value)}

                    onKeyDown={(e)=>{

                        if(e.key==="Enter")

                            handleSend();

                    }}

                    className="flex-1 bg-slate-700 rounded-xl px-5 py-3 outline-none"

                    placeholder="Ask anything..."

                />

                <button

                    onClick={handleSend}

                    disabled={loading}

                    className="bg-cyan-600 hover:bg-cyan-700 rounded-xl p-3"

                >

                    <FaPaperPlane/>

                </button>

            </div>

        </div>

    );

}

export default ChatInput;