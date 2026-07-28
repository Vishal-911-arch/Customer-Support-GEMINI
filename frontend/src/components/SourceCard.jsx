function SourceCard({ filename, pages, types }) {

    return (

        <div
            className="
            rounded-xl
            border
            border-slate-700
            bg-slate-900
            p-4
            hover:border-cyan-500
            transition
            "
        >

            <div
                className="
                flex
                justify-between
                items-start
                "
            >

                <div>

                    <div
                        className="
                        text-cyan-400
                        font-semibold
                        text-lg
                        "
                    >

                        📄 {filename}

                    </div>

                    <div
                        className="
                        text-sm
                        text-gray-400
                        mt-2
                        "
                    >

                        Pages :

                        {

                            pages.join(", ")

                        }

                    </div>

                </div>

                <div
                    className="
                    flex
                    gap-2
                    flex-wrap
                    "
                >

                    {

                        types.map(

                            (t, i) => (

                                <span
                                    key={i}
                                    className="
                                    px-3
                                    py-1
                                    rounded-full
                                    bg-cyan-700
                                    text-xs
                                    "
                                >

                                    {t}

                                </span>

                            )

                        )

                    }

                </div>

            </div>

        </div>

    );

}

export default SourceCard;