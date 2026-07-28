import {
    FaEdit,
    FaThumbtack,
    FaTrash,
    FaCopy
} from "react-icons/fa";

function FloatingMenu({

    chat,

    position,

    onRename,

    onPin,

    onDelete,
    onDuplicate,

    onClose

}) {

    if (!chat) return null;

    return (

        <div

            onClick={(e) => e.stopPropagation()}

            style={{

                position: "fixed",

                left: position.x,

                top: position.y,

                zIndex: 9999

            }}

            className="
                w-56
                rounded-2xl
                bg-slate-900/95
                backdrop-blur-xl
                border
                border-slate-700
                shadow-2xl
                overflow-hidden
                animate-in
                fade-in
                zoom-in-95
            "

        >

            {/* HEADER */}

            <div className="px-4 py-3 border-b border-slate-700">

                <div className="font-medium truncate">

                    {chat.title}

                </div>

            </div>

            {/* RENAME */}

            <button

                onClick={() => {

                    onRename(chat);

                    onClose();

                }}

                className="
                    w-full
                    flex
                    items-center
                    gap-3
                    px-4
                    py-3
                    hover:bg-slate-800
                    transition
                "

            >

                <FaEdit />

                Rename

            </button>

            {/* PIN */}

            <button

                onClick={() => {

                    onPin(chat.id);

                    onClose();

                }}

                className="
                    w-full
                    flex
                    items-center
                    gap-3
                    px-4
                    py-3
                    hover:bg-slate-800
                    transition
                "

            >

                <FaThumbtack />

                {

                    chat.pinned

                        ? "Unpin Chat"

                        : "Pin Chat"

                }

            </button>

            {/* DUPLICATE */}

            <button

                onClick={() => {

                    if (onDuplicate)

                        onDuplicate(chat.id);

                    onClose();

                }}

                className="
                    w-full
                    flex
                    items-center
                    gap-3
                    px-4
                    py-3
                    hover:bg-slate-800
                    transition
                "

            >

                <FaCopy />

                Duplicate

            </button>

            <div className="border-t border-slate-700" />

            {/* DELETE */}

            <button

                onClick={() => {

                    if (

                        window.confirm(

                            "Delete this chat?"

                        )

                    ) {

                        onDelete(chat.id);

                    }

                    onClose();

                }}

                className="
                    w-full
                    flex
                    items-center
                    gap-3
                    px-4
                    py-3
                    text-red-400
                    hover:bg-red-500/10
                    transition
                "

            >

                <FaTrash />

                Delete Chat

            </button>

        </div>

    );

}

export default FloatingMenu;