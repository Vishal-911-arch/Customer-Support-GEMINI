import {

    FaCircle,
    FaDatabase,
    FaCog

} from "react-icons/fa";

function SidebarFooter() {

    return (

        <div className="border-t border-slate-700 p-4 space-y-4">

            <div className="space-y-2 text-sm">

                <div className="flex justify-between">

                    <span>Ollama</span>

                    <span className="text-green-400 flex items-center gap-2">

                        <FaCircle size={8}/>

                        Running

                    </span>

                </div>

                <div className="flex justify-between">

                    <span>Knowledge Base</span>

                    <span>

                        1058 Chunks

                    </span>

                </div>

                <div className="flex justify-between">

                    <span>Documents</span>

                    <span>

                        26 PDFs

                    </span>

                </div>

            </div>

            <button

                className="
                    w-full
                    flex
                    items-center
                    gap-3
                    rounded-xl
                    bg-slate-700
                    px-4
                    py-3
                    hover:bg-slate-600
                "

            >

                <FaCog/>

                Settings

            </button>

        </div>

    );

}

export default SidebarFooter;