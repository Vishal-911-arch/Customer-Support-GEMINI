import { FaRobot } from "react-icons/fa";
import { useEffect, useState } from "react";

function Navbar() {

    const [online, setOnline] = useState(false);

    useEffect(() => {

        async function checkBackend() {

            try {

                const res = await fetch(
                    "http://192.168.172.219:8000/health"
                );

                setOnline(res.ok);

            } catch {

                setOnline(false);

            }

        }

        checkBackend();

        const interval = setInterval(checkBackend, 5000);

        return () => clearInterval(interval);

    }, []);

    return (

        <div className="h-16 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-6">

            <div className="flex items-center gap-3">

                <FaRobot
                    size={26}
                    className="text-cyan-400"
                />

                <div>

                    <h1 className="font-bold text-xl">
                        AI Customer Support
                    </h1>

                    <p className="text-sm text-gray-400">
                        Offline AI Assistant
                    </p>

                </div>

            </div>

            <div
                className={`font-medium ${
                    online
                        ? "text-green-400"
                        : "text-red-400"
                }`}
            >
                ● {online ? "Backend Online" : "Backend Offline"}
            </div>

        </div>

    );

}

export default Navbar;