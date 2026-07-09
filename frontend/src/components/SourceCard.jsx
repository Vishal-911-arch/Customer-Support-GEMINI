function SourceCard({ source }) {

    return (

        <div className="mt-2 rounded-lg border border-slate-700 bg-slate-900 p-3">

            <div className="flex items-center justify-between">

                <div>

                    <div className="text-cyan-400 font-semibold">

                        📄 {source.filename}

                    </div>

                    <div className="text-sm text-gray-400">

                        Page {source.page}

                    </div>

                </div>

                <div>

                    <span className="px-2 py-1 rounded bg-cyan-700 text-xs">

                        {source.type || "pdf"}

                    </span>

                </div>

            </div>

        </div>

    );

}

export default SourceCard;