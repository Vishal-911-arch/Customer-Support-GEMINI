import { FaRobot, FaBars } from "react-icons/fa";

function SidebarHeader({ sidebarOpen, setSidebarOpen }) {

    return (

        <div className="border-b border-slate-700 p-4">

            <div className="flex items-center justify-between">

                <div className="flex items-center gap-3">

                    <div className="
                        w-11
                        h-11
                        rounded-xl
                        bg-cyan-600
                        flex
                        items-center
                        justify-center
                        text-white
                        text-lg
                    ">

                        <FaRobot />

                    </div>

                    <div>

                        <h1 className="font-bold text-lg">

                            Support Interface

                        </h1>

                        <p className="text-xs text-slate-400">

                             Assistant

                        </p>

                    </div>

                </div>

                <button

                    onClick={() => setSidebarOpen(!sidebarOpen)}

                    className="
                        p-2
                        rounded-lg
                        hover:bg-slate-700
                    "

                >

                    <FaBars />

                </button>

            </div>

        </div>

    );

}

export default SidebarHeader;