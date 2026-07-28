import { useContext, useState } from "react";

import { ChatContext } from "../context/ChatContext";

import Message from "./Message";
import TypingIndicator from "./TypingIndicator";

function ChatWindow() {

    const {

        messages,
        loading

    } = useContext(ChatContext);

    const [previewImage, setPreviewImage] =
        useState(null);

    if (messages.length === 0) {

        return (

            <div className="flex-1 flex justify-center items-center">

                <div className="text-center">

                    <h1 className="text-5xl font-bold mb-5">

                        AI Assistant

                    </h1>

                    <p className="text-gray-400">

                        Upload manuals, engineering figures or graphs and ask questions.

                    </p>

                </div>

            </div>

        );

    }

    return (

        <>

            <div className="flex-1 overflow-y-auto p-8">

                <div className="max-w-5xl mx-auto">

                    {

                        messages.map(

                            (msg, index) => (

                                <div
                                    key={index}
                                    className="mb-6"
                                >

                                    {

                                        msg.role === "user" &&
                                        msg.image && (

                                            <div className="flex justify-end mb-3">

                                                <div

                                                    onClick={() =>
                                                        setPreviewImage(
                                                            msg.image.preview
                                                        )
                                                    }

                                                    className="
                                                        cursor-pointer
                                                        bg-slate-800
                                                        hover:bg-slate-700
                                                        transition
                                                        rounded-xl
                                                        px-3
                                                        py-3
                                                        inline-flex
                                                        items-center
                                                        gap-3
                                                        max-w-sm
                                                    "

                                                >

                                                    <img

                                                        src={msg.image.preview}

                                                        alt="Uploaded"

                                                        className="
                                                            w-14
                                                            h-14
                                                            rounded-lg
                                                            object-cover
                                                            border
                                                            border-slate-600
                                                            flex-shrink-0
                                                        "

                                                    />

                                                    <div>

                                                        <p className="text-white font-medium">

                                                            Image Attached

                                                        </p>

                                                        <p className="text-sm text-gray-400">

                                                            Click to view

                                                        </p>

                                                    </div>

                                                </div>

                                            </div>

                                        )

                                    }

                                    <Message

                                        message={msg}

                                    />

                                </div>

                            )

                        )

                    }

                    {

                        loading &&

                        <TypingIndicator />

                    }

                </div>

            </div>

            {

                previewImage && (

                    <div

                        onClick={() =>
                            setPreviewImage(null)
                        }

                        className="
                            fixed
                            inset-0
                            bg-black/80
                            flex
                            justify-center
                            items-center
                            z-50
                            p-8
                            cursor-pointer
                        "

                    >

                        <img

                            src={previewImage}

                            alt="Preview"

                            className="
                                max-w-[90vw]
                                max-h-[90vh]
                                rounded-xl
                                shadow-2xl
                            "

                            onClick={(e) =>
                                e.stopPropagation()
                            }

                        />

                    </div>

                )

            }

        </>

    );

}

export default ChatWindow;