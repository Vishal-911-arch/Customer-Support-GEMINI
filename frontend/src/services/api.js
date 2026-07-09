import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 300000,
});

// -----------------------------
// Chat
// -----------------------------

export const sendMessage = async (question) => {

    const response = await api.post("/chat", {
        question,
    });

    return response.data;
};

// -----------------------------
// Upload PDF
// -----------------------------

export const uploadPDF = async (file) => {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/upload/pdf",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};

// -----------------------------
// Upload Image
// -----------------------------

export const uploadImage = async (file) => {

    const formData = new FormData();

    formData.append("file", file);

    const response = await api.post(
        "/upload/image",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};

export default api;