import { useContext, useState } from "react";
import { FaBars } from "react-icons/fa";

import { ChatContext } from "../context/ChatContext";

import SidebarHeader from "../sidebar/SidebarHeader";
import NewChatButton from "../sidebar/NewChatButton";
import ChatList from "../sidebar/ChatList";
import KnowledgeExplorer from "../sidebar/KnowledgeExplorer";
import SidebarFooter from "../sidebar/SidebarFooter";
import FloatingMenu from "../sidebar/FloatingMenu";

function Sidebar() {

    const {
        chatSessions,
        currentChatId,
        setCurrentChatId,
        createChat,
        renameChat,
        deleteChat,
        pinChat
    } = useContext(ChatContext);

    const [sidebarOpen, setSidebarOpen] = useState(true);

    const [menuOpen, setMenuOpen] = useState(null);

    const [menuPosition, setMenuPosition] = useState({
        x: 0,
        y: 0
    });

    const selectedChat =
        chatSessions.find(chat => chat.id === menuOpen);

    return (
        <>

            {
                !sidebarOpen &&

                <button
                    onClick={() => setSidebarOpen(true)}
                    className="
                        fixed
                        top-4
                        left-4
                        z-50
                        p-3
                        rounded-xl
                        bg-slate-800
                        hover:bg-slate-700
                        transition
                        shadow-xl
                    "
                >
                    <FaBars />
                </button>
            }

            <aside

                onClick={() => setMenuOpen(null)}

                className={`
                    h-screen
                    bg-slate-900
                    border-r
                    border-slate-700
                    flex
                    flex-col
                    transition-all
                    duration-300
                    overflow-hidden
                    ${sidebarOpen ? "w-72" : "w-0"}
                `}
            >

                <SidebarHeader
                    sidebarOpen={sidebarOpen}
                    setSidebarOpen={setSidebarOpen}
                />

                <div
                className="
                    flex-1
                    overflow-y-auto
                    sidebar-scroll
                "
            >

                <NewChatButton
                    createChat={createChat}
                />

                <ChatList
                    chatSessions={chatSessions}
                    currentChatId={currentChatId}
                    setCurrentChatId={setCurrentChatId}
                    menuOpen={menuOpen}
                    setMenuOpen={setMenuOpen}
                    setMenuPosition={setMenuPosition}
                />

                <KnowledgeExplorer />

            </div>

            <SidebarFooter />
            </aside>

            <FloatingMenu

                chat={selectedChat}

                position={menuPosition}

                onRename={(chat) => {

                    const title = window.prompt(
                        "Rename chat",
                        chat.title
                    );

                    if (title && title.trim()) {

                        renameChat(
                            chat.id,
                            title.trim()
                        );

                    }

                }}

                onPin={pinChat}

                onDelete={deleteChat}

                onDuplicate={(chatId) => {

                    console.log(
                        "Duplicate:",
                        chatId
                    );

                }}

                onClose={() => setMenuOpen(null)}

            />

        </>
    );

}

export default Sidebar;