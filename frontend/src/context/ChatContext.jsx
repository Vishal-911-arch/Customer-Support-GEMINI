import {
    createContext,
    useState
} from "react";

export const ChatContext = createContext();

export function ChatProvider({ children }) {

    // ==========================================
    // INITIAL CHAT
    // ==========================================

    const initialChat = {
        id: Date.now(),
        title: "New Chat",
        messages: [],
        pinned: false,
        createdAt: Date.now()
    };

    // ==========================================
    // STATE
    // ==========================================

    const [chatSessions, setChatSessions] = useState([
        initialChat
    ]);

    const [currentChatId, setCurrentChatId] =
        useState(initialChat.id);

    const [loading, setLoading] =
        useState(false);

    // ==========================================
    // CURRENT CHAT
    // ==========================================

    const currentChat =
        chatSessions.find(
            chat => chat.id === currentChatId
        );

    const messages =
        currentChat
            ? currentChat.messages
            : [];

    // ==========================================
    // RECENT HISTORY
    // ==========================================

    function getRecentHistory(limit = 6) {
        return messages
            .filter(msg => !msg.isStatus)
            .slice(-limit)
            .map(msg => ({
                role: msg.role,
                content: msg.content
            }));
    }

    // ==========================================
    // SORT CHATS
    // ==========================================

    function sortChats(chats) {
        return [...chats].sort((a, b) => {

            // Pinned chats always first
            if (a.pinned !== b.pinned) {
                return b.pinned - a.pinned;
            }

            // Then newest
            return b.createdAt - a.createdAt;
        });
    }

    // ==========================================
    // ADD MESSAGE
    // ==========================================

    function addMessage(message) {
        setChatSessions(prev =>
            prev.map(chat =>
                chat.id === currentChatId
                    ? {
                        ...chat,
                        messages: [
                            ...chat.messages,
                            message
                        ]
                    }
                    : chat
            )
        );
    }

    // ==========================================
    // REPLACE MESSAGES
    // ==========================================

    function setMessages(newMessages) {
        setChatSessions(prev =>
            prev.map(chat =>
                chat.id === currentChatId
                    ? {
                        ...chat,
                        messages:
                            typeof newMessages === "function"
                                ? newMessages(chat.messages)
                                : newMessages
                    }
                    : chat
            )
        );
    }

    // ==========================================
    // UPDATE STATUS MESSAGE
    // ==========================================

    function updateStatusMessage(text) {
        setChatSessions(prev =>
            prev.map(chat => {
                if (chat.id !== currentChatId)
                    return chat;

                const msgs = [...chat.messages];

                for (
                    let i = msgs.length - 1;
                    i >= 0;
                    i--
                ) {
                    if (msgs[i].isStatus) {
                        msgs[i] = {
                            ...msgs[i],
                            content: text
                        };
                        break;
                    }
                }

                return {
                    ...chat,
                    messages: msgs
                };
            })
        );
    }

    // ==========================================
    // CREATE CHAT
    // ==========================================

    function createChat() {
        const id = Date.now();

        const newChat = {
            id,
            title: "New Chat",
            messages: [],
            pinned: false,
            createdAt: Date.now()
        };

        const updated = sortChats([
            newChat,
            ...chatSessions
        ]);

        setChatSessions(updated);
        setCurrentChatId(id);
    }

    // ==========================================
    // DELETE CHAT
    // ==========================================

    function deleteChat(id) {
        const updated =
            chatSessions.filter(
                chat => chat.id !== id
            );

        setChatSessions(updated);

        if (
            currentChatId === id &&
            updated.length
        ) {
            setCurrentChatId(
                updated[0].id
            );
        }
    }

    // ==========================================
    // RENAME CHAT
    // ==========================================

    function renameChat(id, title) {
        setChatSessions(prev =>
            prev.map(chat =>
                chat.id === id
                    ? {
                        ...chat,
                        title
                    }
                    : chat
            )
        );
    }

    // ==========================================
    // PIN / UNPIN CHAT
    // ==========================================

    function pinChat(id) {
        setChatSessions(prev => {
            const updated = prev.map(chat =>
                chat.id === id
                    ? {
                        ...chat,
                        pinned: !chat.pinned
                    }
                    : chat
            );

            return sortChats(updated);
        });
    }

    // ==========================================
    // PROVIDER
    // ==========================================

    return (
        <ChatContext.Provider
            value={{
                chatSessions,
                currentChatId,
                setCurrentChatId,
                currentChat,
                messages,
                getRecentHistory,
                addMessage,
                setMessages,
                loading,
                setLoading,
                createChat,
                deleteChat,
                renameChat,
                pinChat,
                updateStatusMessage
            }}
        >
            {children}
        </ChatContext.Provider>
    );
}