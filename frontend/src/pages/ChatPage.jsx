import { useState } from "react";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

function ChatPage({ onLogout }) {
    const [activeImage, setActiveImage] = useState(null);

    return (
        <div className="h-screen bg-slate-900 flex flex-col">
            <Navbar onLogout={onLogout} />

            <div className="flex flex-1 overflow-hidden">
                <Sidebar />

                <div className="flex flex-col flex-1">
                    <ChatWindow />

                    <ChatInput
                        activeImage={activeImage}
                        setActiveImage={setActiveImage}
                    />
                </div>
            </div>
        </div>
    );
}

export default ChatPage;