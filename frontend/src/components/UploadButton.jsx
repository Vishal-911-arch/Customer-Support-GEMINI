import {

    useRef,
    useContext

} from "react";

import { FaUpload } from "react-icons/fa";

import {

    uploadPDF,
    uploadImage

} from "../services/api";

import {

    ChatContext

} from "../context/ChatContext";


function UploadButton({

    setActiveImage

}) {

    const fileInput = useRef();

    const {

        addMessage,
        updateStatusMessage

    } = useContext(

        ChatContext

    );

    async function handleUpload(e) {

        const file = e.target.files[0];

        if (!file)
            return;

        try {

            const ext = file.name
                .split(".")
                .pop()
                .toLowerCase();

            let response;

            // =====================================
            // PDF Upload
            // =====================================

            if (ext === "pdf") {

                addMessage({

                    role: "assistant",

                    content:
                        `📄 Uploading ${file.name}...`,

                    isStatus: true

                });

                const interval =
                    setInterval(

                        async () => {

                            try {

                                const res =
                                    await fetch(

                                        "http://127.0.0.1:8000/upload-status"

                                    );

                                const data =
                                    await res.json();

                                updateStatusMessage(

                                    data.stage

                                );

                            }

                            catch (err) {

                                console.log(err);

                            }

                        },

                        1000

                    );

                response =
                    await uploadPDF(file);

                clearInterval(

                    interval

                );

                updateStatusMessage(

`✅ PDF indexed successfully.

📄 Pages Indexed : ${response.documents}

✂️ Chunks Created : ${response.chunks}

🧠 Embeddings Generated : ${response.embeddings}`

                );

            }

            // =====================================
            // IMAGE Upload
            // =====================================

            else {

                response =
                    await uploadImage(file);

                console.log(response);

                // Replace previous active image
                setActiveImage({

                    name:
                        file.name,

                    preview:
                        URL.createObjectURL(file),

                    path:
                        response.data.image_path

                });

                addMessage({

                    role: "assistant",

                    content:

`🖼️ Image attached.

Image : ${file.name}

You can now ask questions related to this image.`

                });

            }

        }

        catch (err) {

            console.log(err);

            updateStatusMessage(

                "❌ Upload failed."

            );

        }

    }

    return (

        <>

            <input

                hidden

                type="file"

                ref={fileInput}

                accept="
                    .pdf,
                    .png,
                    .jpg,
                    .jpeg,
                    .bmp,
                    .webp
                "

                onChange={handleUpload}

            />

            <button

                onClick={() =>

                    fileInput.current.click()

                }

                className="

                    p-3
                    rounded-xl
                    hover:bg-slate-700
                    text-gray-400
                    hover:text-cyan-400
                    transition

                "

            >

                <FaUpload size={18} />

            </button>

        </>

    );

}

export default UploadButton;