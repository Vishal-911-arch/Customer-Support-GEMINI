import { createContext, useState } from "react";

export const ChatContext = createContext();

export function ChatProvider({ children }) {

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    return (

        <ChatContext.Provider

            value={{

                messages,

                setMessages,

                loading,

                setLoading

            }}

        >

            {children}

        </ChatContext.Provider>

    );

}