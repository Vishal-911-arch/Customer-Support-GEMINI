import { useState, useContext, useEffect } from "react";
import UploadButton from "./UploadButton";
import { FaPaperPlane } from "react-icons/fa";

import { ChatContext } from "../context/ChatContext";
import { sendMessage } from "../services/api";

function ChatInput({

    activeImage,
    setActiveImage

}) {

    const [question, setQuestion] = useState("");

    const [useImageContext,
        setUseImageContext] = useState(true);

    const [previewImage,
        setPreviewImage] = useState(null);

    // Controls whether thumbnail is shown
    const [showThumbnail,
        setShowThumbnail] = useState(true);

    const {
    setMessages,
    loading,
    setLoading,
    currentChat,
    renameChat
    } = useContext(ChatContext);

    // Whenever a NEW image is uploaded,
    // show thumbnail again.
    useEffect(() => {

        if (activeImage) {

            setShowThumbnail(true);

        }

    }, [activeImage]);


    async function handleSend() {

        if (!question.trim())
            return;

        const currentQuestion = question;
        // Rename only once

        const shouldSendImage =

            activeImage &&
            useImageContext;

        const userMessage = {

            role: "user",

            content: currentQuestion,

            image:
                shouldSendImage
                    ? activeImage
                    : null

        };

        setMessages(prev => [

            ...prev,
            userMessage

        ]);

        setQuestion("");

        setLoading(true);

        try {

            const response =
                await sendMessage(

                    currentQuestion,

                    shouldSendImage
                        ? activeImage.path
                        : null

                );

            // Rename only once using backend-generated title
            if (

                currentChat.title === "New Chat" &&

                response.title

            ) {

                renameChat(

                    currentChat.id,

                    response.title

                );

            }

            const aiMessage = {

                role: "assistant",

                content:
                    response.answer,

                sources:
                    response.sources || [],

                graph:
                    response.graph || null,

                figure:
                    response.figure || null

            };

            setMessages(prev => [

                ...prev,
                aiMessage

            ]);

            // Hide thumbnail after first image question
            if (shouldSendImage) {

                setShowThumbnail(false);

            }

        }

        catch (error) {

            console.log(error);

            setMessages(prev => [

                ...prev,

                {

                    role: "assistant",

                    content:
                        "Unable to connect to backend."

                }

            ]);

        }

        setLoading(false);

    }

    return (

        <>

            <div className="border-t border-slate-700 p-5 bg-slate-800">

                {

                    activeImage && (

                        <div className="max-w-5xl mx-auto mb-3">

                            <div
                                className="
                                flex
                                items-center
                                gap-3
                                bg-slate-700
                                px-4
                                py-2
                                rounded-lg
                                w-fit"
                            >

                                {

                                    showThumbnail ? (

                                        <>

                                            <img

                                                src={activeImage.preview}

                                                alt="preview"

                                                onClick={() =>
                                                    setPreviewImage(
                                                        activeImage.preview
                                                    )
                                                }

                                                className="
                                                w-10
                                                h-10
                                                rounded
                                                object-cover
                                                cursor-pointer
                                                hover:scale-110
                                                transition"

                                            />

                                            <span
                                                className="text-sm"
                                            >

                                                {

                                                    activeImage.name

                                                }

                                            </span>

                                        </>

                                    ) : (

                                        <span
                                            className="text-sm font-medium"
                                        >

                                            🖼 Using Previous Image

                                        </span>

                                    )

                                }

                                <button

                                    onClick={() =>

                                        setUseImageContext(

                                            !useImageContext

                                        )

                                    }

                                    className={

                                        `text-xs px-3 py-1 rounded-lg ${

                                            useImageContext

                                                ?

                                                "bg-green-600"

                                                :

                                                "bg-slate-600"

                                        }`

                                    }

                                >

                                    {

                                        useImageContext

                                            ?

                                            "Using Image ✓"

                                            :

                                            "Image Off"

                                    }

                                </button>

                                <button

                                    onClick={() => {

                                        setActiveImage(null);

                                        setUseImageContext(true);

                                        setShowThumbnail(true);

                                    }}

                                    className="
                                    text-red-400
                                    hover:text-red-500"

                                >

                                    ✕

                                </button>

                            </div>

                        </div>

                    )

                }

                <div
                    className="
                    max-w-5xl
                    mx-auto
                    flex
                    items-center
                    gap-3"
                >

                    <UploadButton

                        setActiveImage={
                            setActiveImage
                        }

                    />

                    <input

                        value={question}

                        onChange={(e) =>

                            setQuestion(
                                e.target.value
                            )

                        }

                        onKeyDown={(e) => {

                            if (

                                e.key === "Enter"

                            ) {

                                handleSend();

                            }

                        }}

                        className="
                        flex-1
                        bg-slate-700
                        rounded-xl
                        px-5
                        py-3
                        outline-none"

                        placeholder="Ask anything..."

                    />

                    <button

                        onClick={handleSend}

                        disabled={loading}

                        className="
                        bg-cyan-600
                        hover:bg-cyan-700
                        rounded-xl
                        p-3"

                    >

                        <FaPaperPlane />

                    </button>

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

export default ChatInput;