import { useRef } from "react";

import {
    FaUpload
} from "react-icons/fa";

import {
    uploadPDF,
    uploadImage
} from "../services/api";

function UploadButton() {

    const fileInput = useRef();

    async function handleUpload(e) {

        const file = e.target.files[0];

        if (!file) return;

        try {

            const ext = file.name
                .split(".")
                .pop()
                .toLowerCase();

            let response;

            if (ext === "pdf") {

                response = await uploadPDF(file);

            }

            else {

                response = await uploadImage(file);

            }

            alert(response.message);

        }

        catch (err) {

            console.error(err);

            alert("Upload failed.");

        }

    }

    return (

        <>

            <input

                type="file"

                hidden

                ref={fileInput}

                accept=".pdf,.png,.jpg,.jpeg,.bmp,.tif,.tiff,.webp"

                onChange={handleUpload}

            />

            <button

                onClick={() => fileInput.current.click()}

                className="p-3 rounded-xl hover:bg-slate-700 text-gray-400 hover:text-cyan-400 transition"

            >

                <FaUpload size={18}/>

            </button>

        </>

    );

}

export default UploadButton;