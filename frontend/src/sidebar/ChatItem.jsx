import {
    FaComments,
    FaEllipsisH
} from "react-icons/fa";

function ChatItem({

    chat,

    currentChatId,

    setCurrentChatId,

    setMenuOpen,

    menuOpen,

    setMenuPosition

}) {

    return (

        <div

            className={`
                group
                rounded-xl
                cursor-pointer
                transition
                ${

                    currentChatId === chat.id

                        ? "bg-slate-700"

                        : "hover:bg-slate-700/60"

                }
            `}

            onClick={() => {

                setCurrentChatId(chat.id);

                setMenuOpen(null);

            }}

        >

            <div className="flex items-center gap-3 px-3 py-3">

                <FaComments className="text-slate-400 shrink-0"/>

                <span className="truncate flex-1">

                    {

                        chat.pinned && "📌 "

                    }

                    {chat.title}

                </span>

                <button

                    onClick={(e)=>{

                        e.stopPropagation();

                        const rect =

                            e.currentTarget.getBoundingClientRect();

                        setMenuPosition({

                            x: rect.right + 10,

                            y: rect.top

                        });

                        setMenuOpen(

                            menuOpen===chat.id

                                ? null

                                : chat.id

                        );

                    }}

                    className="
                        opacity-0
                        group-hover:opacity-100
                        transition
                        p-2
                        rounded-lg
                        hover:bg-slate-600
                    "

                >

                    <FaEllipsisH/>

                </button>

            </div>

        </div>

    );

}

export default ChatItem;