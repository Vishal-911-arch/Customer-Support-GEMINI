import {
    FaChevronDown,
    FaChevronRight
} from "react-icons/fa";

function ExplorerSection({
    title,
    icon,
    items = [],
    isOpen,
    onToggle,
    showPages = true,
    onSelect
}) {
    return (
        <div className="mb-2">
            {/* HEADER */}
            <button
                onClick={onToggle}
                className="
                    w-full
                    flex
                    items-center
                    justify-between
                    px-3
                    py-2
                    rounded-xl
                    hover:bg-slate-700
                    transition-all
                    duration-200
                "
            >
                <div className="flex items-center gap-3 min-w-0">
                    <span className="text-cyan-400 flex-shrink-0">
                        {icon}
                    </span>

                    <span className="font-medium truncate">
                        {title}
                    </span>

                    <span
                        className="
                            text-xs
                            text-gray-400
                            bg-slate-700
                            px-2
                            py-0.5
                            rounded-full
                            flex-shrink-0
                        "
                    >
                        {items.length}
                    </span>
                </div>

                {isOpen ? <FaChevronDown /> : <FaChevronRight />}
            </button>

            {/* CONTENT */}
            {isOpen && (
                <div className="mt-2 ml-5 border-l border-slate-700 pl-4 space-y-2">
                    {items.length === 0 && (
                        <div
                            className="
                                text-gray-500
                                text-sm
                                italic
                                py-2
                            "
                        >
                            No files found
                        </div>
                    )}

                    {items.map((item) => {
                        const displayName = item.name || item.filename || "Untitled";

                        return (
                            <button
                                key={item.filename || item.name}
                                onClick={() => onSelect && onSelect(item)}
                                className="
                                    w-full
                                    text-left
                                    rounded-lg
                                    p-2
                                    hover:bg-slate-700
                                    transition-all
                                    duration-200
                                    group
                                "
                            >
                                <div className="relative">
                                    <div
                                        className="
                                            truncate
                                            font-medium
                                            group-hover:text-cyan-300
                                        "
                                        title={displayName}
                                    >
                                        📄 {displayName}
                                    </div>

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
                                        {displayName}
                                    </div>
                                </div>

                                {showPages && item.pages && (
                                    <div
                                        className="
                                            text-xs
                                            text-gray-400
                                            mt-1
                                        "
                                    >
                                        {item.pages} pages
                                    </div>
                                )}
                            </button>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default ExplorerSection;