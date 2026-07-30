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
                ${currentChatId === chat.id
                    ? "bg-slate-700"
                    : "hover:bg-slate-700/60"
                }
            `}
            onClick={() => {
                setCurrentChatId(chat.id);
                setMenuOpen(null);
            }}
        >
            <div className="flex items-center gap-3 px-3 py-3 min-w-0">
                <FaComments className="text-slate-400 shrink-0" />

                <div className="relative min-w-0 flex-1">
                    <span
                        className="truncate block"
                        title={chat.title}
                    >
                        {chat.pinned && "📌 "}
                        {chat.title}
                    </span>

                    <div className="
                        pointer-events-none
                        absolute left-0 top-full mt-2 z-50
                        hidden group-hover:block
                        max-w-[320px]
                        rounded-lg bg-slate-950 text-white
                        px-3 py-2 text-sm shadow-xl
                        border border-slate-700
                        whitespace-normal
                    ">
                        {chat.pinned && "📌 "}
                        {chat.title}
                    </div>
                </div>

                <button
                    onClick={(e) => {
                        e.stopPropagation();

                        const rect =
                            e.currentTarget.getBoundingClientRect();

                        setMenuPosition({
                            x: rect.right + 10,
                            y: rect.top
                        });

                        setMenuOpen(
                            menuOpen === chat.id
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
                        shrink-0
                    "
                >
                    <FaEllipsisH />
                </button>
            </div>
        </div>
    );
}

export default ChatItem;