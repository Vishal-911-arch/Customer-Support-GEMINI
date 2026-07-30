import { FaRobot } from "react-icons/fa";
import { useEffect, useState } from "react";
import api from "../services/api";

function Navbar({ onLogout }) {
    const [online, setOnline] = useState(false);

    useEffect(() => {
        async function checkBackend() {
            try {
                const res = await api.get("/health");
                setOnline(res.status === 200);
            } catch {
                setOnline(false);
            }
        }

        checkBackend();
        const interval = setInterval(checkBackend, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-16 bg-slate-800 border-b border-slate-700 px-6 flex items-center justify-between gap-4">
            <div className="flex items-center gap-3 min-w-0">
                <FaRobot size={26} className="text-cyan-400 flex-shrink-0" />
                <div className="min-w-0">
                    <h1 className="font-bold text-xl text-white truncate">
                        AI Customer Support
                    </h1>
                    <p className="text-sm text-gray-400 truncate">
                         AI Assistant
                    </p>
                </div>
            </div>

            <div className="ml-auto flex items-center gap-4 whitespace-nowrap flex-shrink-0">
                <div
                    className={`font-medium text-sm flex items-center gap-2 ${
                        online ? "text-green-400" : "text-red-400"
                    }`}
                >
                    <span className={`w-2 h-2 rounded-full ${online ? "bg-green-400" : "bg-red-400"}`} />
                    {online ? "Backend Online" : "Backend Offline"}
                </div>

                {onLogout && (
                    <button
                        onClick={onLogout}
                        className="text-white hover:text-cyan-300 text-sm font-medium"
                    >
                        Logout
                    </button>
                )}
            </div>
        </div>
    );
}

export default Navbar;