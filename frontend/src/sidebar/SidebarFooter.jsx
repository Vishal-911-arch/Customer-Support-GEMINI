import {
    FaDatabase,
    FaCog
} from "react-icons/fa";

function SidebarFooter() {
    return (
        <div className="border-t border-slate-700 px-4 py-3">
            <div className="space-y-3 text-sm">
                <div className="flex items-center justify-between">
                    <span className="text-slate-200">Knowledge Base</span>
                    <span className="text-slate-100 font-medium">
                        1058 Chunks
                    </span>
                </div>

                <div className="flex items-center justify-between">
                    <span className="text-slate-200">Documents</span>
                    <span className="text-slate-100 font-medium">
                        26 PDFs
                    </span>
                </div>
            </div>

            <button
                className="
                    mt-4
                    w-full
                    flex
                    items-center
                    gap-3
                    rounded-xl
                    bg-slate-700
                    px-4
                    py-3
                    hover:bg-slate-600
                    transition
                "
            >
                <FaCog />
                Settings
            </button>
        </div>
    );
}

export default SidebarFooter;