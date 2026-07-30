import { useEffect, useState } from "react";
import ChatPage from "./pages/ChatPage";
import LoginPage from "./pages/LoginPage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    sessionStorage.getItem("chatbot_token") !== null
  );

  useEffect(() => {
    setIsLoggedIn(sessionStorage.getItem("chatbot_token") !== null);
  }, []);

  function handleLogin() {
    setIsLoggedIn(true);
  }

  function handleLogout() {
    sessionStorage.removeItem("chatbot_token");
    sessionStorage.removeItem("chatbot_auth");
    setIsLoggedIn(false);
  }

  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return <ChatPage onLogout={handleLogout} />;
}

export default App;
