import ChatItem from "./ChatItem";

function ChatList({

    chatSessions,

    currentChatId,

    setCurrentChatId,

    menuOpen,

    setMenuOpen,

    setMenuPosition

}) {

    const pinned =

        chatSessions.filter(

            c=>c.pinned

        );

    const others =

        chatSessions.filter(

            c=>!c.pinned

        );

    return(

        <div

            className="
                px-4
                pb-6
                space-y-6
            "

        >

            {

                pinned.length>0 &&

                <>

                    <p className="text-xs text-slate-400 uppercase">

                        Pinned

                    </p>

                    <div className="space-y-2">

                        {

                            pinned.map(chat=>

                                <ChatItem

                                    key={chat.id}

                                    chat={chat}

                                    currentChatId={currentChatId}

                                    setCurrentChatId={setCurrentChatId}

                                    menuOpen={menuOpen}

                                    setMenuOpen={setMenuOpen}

                                    setMenuPosition={setMenuPosition}

                                />

                            )

                        }

                    </div>

                </>

            }

            <>

                <p className="text-xs text-slate-400 uppercase">

                    Chats

                </p>

                <div className="space-y-2">

                    {

                        others.map(chat=>

                            <ChatItem

                                key={chat.id}

                                chat={chat}

                                currentChatId={currentChatId}

                                setCurrentChatId={setCurrentChatId}

                                menuOpen={menuOpen}

                                setMenuOpen={setMenuOpen}

                                setMenuPosition={setMenuPosition}

                            />

                        )

                    }

                </div>

            </>

        </div>

    );

}

export default ChatList;