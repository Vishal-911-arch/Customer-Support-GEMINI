import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
    timeout: 0,
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("chatbot_token");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// =========================
// Auth
// =========================

export const login = async (username, password) => {
    const response = await api.post("/auth/login", {
        username,
        password,
    });
    return response.data;
};

export const clearAuth = () => {
    localStorage.removeItem("chatbot_token");
    localStorage.removeItem("chatbot_auth");
};

// =========================
// Chat
// =========================

export const sendMessage = async (
    question,
    image_path = null,
    history = []
) => {
    const response = await api.post("/chat", {
        question,
        image_path,
        history,
    });

    return response.data;
};

// =========================
// Upload PDF
// =========================

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

// =========================
// Upload Image
// =========================

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

// =========================
// Knowledge Explorer
// =========================

export const getKnowledge = async () => {
    const response = await api.get("/knowledge");
    return response.data;
};

export default api;