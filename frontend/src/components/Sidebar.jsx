import {
    FaPlus,
    FaFilePdf,
    FaShieldAlt,
    FaTools,
    FaFolderOpen
} from "react-icons/fa";

function Sidebar() {

    return (

        <div className="w-72 bg-slate-800 border-r border-slate-700 flex flex-col">

            <button
                className="m-4 p-3 rounded-xl bg-cyan-600 hover:bg-cyan-700 transition"
            >
                <FaPlus className="inline mr-2" />

                New Chat

            </button>

            <div className="px-5 mt-3">

                <h2 className="text-gray-400 text-sm mb-3">

                    Knowledge Base

                </h2>

                <div className="space-y-4">

                    <div className="flex gap-3 items-center">

                        <FaFilePdf />

                        Manuals

                    </div>

                    <div className="flex gap-3 items-center">

                        <FaShieldAlt />

                        Safety

                    </div>

                    <div className="flex gap-3 items-center">

                        <FaTools />

                        Maintenance

                    </div>

                    <div className="flex gap-3 items-center">

                        <FaFolderOpen />

                        Uploaded Files

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Sidebar;