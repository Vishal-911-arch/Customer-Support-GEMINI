import { useContext } from "react";
import { ChatContext } from "../context/ChatContext";

import Message from "./Message";
import TypingIndicator from "./TypingIndicator";

function ChatWindow() {

    const { messages, loading } = useContext(ChatContext);

    if (messages.length === 0) {

        return (

            <div className="flex-1 flex justify-center items-center">

                <div className="text-center">

                    <h1 className="text-5xl font-bold mb-5">

                        HAL AI Assistant

                    </h1>

                    <p className="text-gray-400">

                        Upload manuals, engineering figures or graphs and ask questions.

                    </p>

                </div>

            </div>

        );

    }

    return (

        <div className="flex-1 overflow-y-auto p-8">

            <div className="max-w-5xl mx-auto">

                {

                    messages.map((msg, index) => (

                        <Message
                            key={index}
                            message={msg}
                        />

                    ))

                }

                {

                    loading && <TypingIndicator />

                }

            </div>

        </div>

    );

}

export default ChatWindow;