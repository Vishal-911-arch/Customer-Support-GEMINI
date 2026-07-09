import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

function ChatPage() {
  return (
    <div className="h-screen bg-slate-900 flex flex-col">

      <Navbar />

      <div className="flex flex-1 overflow-hidden">

        <Sidebar />

        <div className="flex flex-col flex-1">

          <ChatWindow />

          <ChatInput />

        </div>

      </div>

    </div>
  );
}

export default ChatPage;