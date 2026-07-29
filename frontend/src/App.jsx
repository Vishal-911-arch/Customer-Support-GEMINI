import { useEffect, useState } from "react";
import ChatPage from "./pages/ChatPage";
import LoginPage from "./pages/LoginPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    localStorage.getItem("chatbot_token") !== null
  );

  useEffect(() => {
    setIsLoggedIn(localStorage.getItem("chatbot_token") !== null);
  }, []);

  function handleLogin() {
    setIsLoggedIn(true);
  }

  function handleLogout() {
    localStorage.removeItem("chatbot_token");
    localStorage.removeItem("chatbot_auth");
    setIsLoggedIn(false);
  }

  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return <ChatPage onLogout={handleLogout} />;
}

export default App;