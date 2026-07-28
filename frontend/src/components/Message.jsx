import { useState } from "react";

import SourceCard from "./SourceCard";

function Message({ message }) {

    const isUser =
        message.role === "user";

    const [showSources,
        setShowSources] =
        useState(false);

    // ===========================
    // Group duplicate sources
    // ===========================

    const groupedSources = {};

    if (message.sources) {

        message.sources.forEach((src) => {

            const file =
                src.filename;

            if (!groupedSources[file]) {

                groupedSources[file] = {

                    pages: [],

                    types: []

                };

            }

            if (
                src.page &&
                !groupedSources[file]
                    .pages.includes(src.page)
            ) {

                groupedSources[file]
                    .pages.push(src.page);

            }

            if (
                src.type &&
                !groupedSources[file]
                    .types.includes(src.type)
            ) {

                groupedSources[file]
                    .types.push(src.type);

            }

        });

    }

    return (

        <div
            className={`w-full flex ${
                isUser
                    ? "justify-end"
                    : "justify-start"
            } mb-6`}
        >

            <div
                className={`max-w-4xl rounded-xl px-5 py-4 whitespace-pre-wrap ${
                    isUser
                        ? "bg-cyan-600 text-white"
                        : "bg-slate-800 text-gray-100"
                }`}
            >

                {/* MESSAGE */}

                <div>

                    {message.content}

                </div>

                {/* SOURCES */}

                {

                    !isUser &&
                    Object.keys(groupedSources)
                        .length > 0 && (

                        <div className="mt-6">

                            <button

                                onClick={() =>
                                    setShowSources(
                                        !showSources
                                    )
                                }

                                className="
                                flex
                                items-center
                                gap-2
                                text-cyan-400
                                hover:text-cyan-300
                                font-semibold
                                "
                            >

                                {

                                    showSources
                                    ? "▼"
                                    : "▶"

                                }

                                Sources Used

                                (

                                {

                                    Object.keys(
                                        groupedSources
                                    ).length

                                }

                                )

                            </button>

                            {

                                showSources && (

                                    <div
                                        className="
                                        mt-4
                                        space-y-4
                                        "
                                    >

                                        {

                                            Object.entries(
                                                groupedSources
                                            ).map(

                                                (

                                                    [

                                                        filename,

                                                        data

                                                    ],

                                                    index

                                                ) => (

                                                    <SourceCard

                                                        key={index}

                                                        filename={
                                                            filename
                                                        }

                                                        pages={
                                                            data.pages.sort(
                                                                (
                                                                    a,
                                                                    b
                                                                ) =>
                                                                    a -
                                                                    b
                                                            )
                                                        }

                                                        types={
                                                            data.types
                                                        }

                                                    />

                                                )

                                            )

                                        }

                                    </div>

                                )

                            }

                        </div>

                    )

                }

                {/* GRAPH */}

                {

                    !isUser &&
                    message.graph && (

                        <div
                            className="
                            mt-5
                            p-4
                            rounded-lg
                            border
                            border-cyan-600
                            bg-slate-900
                            "
                        >

                            <h4
                                className="
                                text-cyan-400
                                font-semibold
                                mb-3
                                "
                            >

                                📊 Graph Analysis

                            </h4>

                            <p>

                                <strong>

                                    Title :

                                </strong>

                                {" "}

                                {

                                    message.graph.title

                                }

                            </p>

                            <p>

                                <strong>

                                    X Axis :

                                </strong>

                                {" "}

                                {

                                    message.graph.x_axis

                                }

                            </p>

                            <p>

                                <strong>

                                    Y Axis :

                                </strong>

                                {" "}

                                {

                                    message.graph.y_axis

                                }

                            </p>

                            <p
                                className="mt-3"
                            >

                                {

                                    message.graph.summary

                                }

                            </p>

                        </div>

                    )

                }

                {/* FIGURE */}

                {

                    !isUser &&
                    message.figure && (

                        <div
                            className="
                            mt-5
                            p-4
                            rounded-lg
                            border
                            border-cyan-600
                            bg-slate-900
                            "
                        >

                            <h4
                                className="
                                text-cyan-400
                                font-semibold
                                mb-2
                                "
                            >

                                🖼 Figure Information

                            </h4>

                            <p>

                                <strong>

                                    {

                                        message.figure.title

                                    }

                                </strong>

                            </p>

                            <p
                                className="mt-2"
                            >

                                {

                                    message.figure.description

                                }

                            </p>

                        </div>

                    )

                }

            </div>

        </div>

    );

}

export default Message;