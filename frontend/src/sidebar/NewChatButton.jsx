import { FaPlus } from "react-icons/fa";

function NewChatButton({ createChat }) {

    return (

        <div className="p-4">

            <button

                onClick={createChat}

                className="
                    w-full
                    rounded-xl
                    bg-cyan-600
                    hover:bg-cyan-700
                    py-3
                    font-medium
                    transition
                    shadow-lg
                "

            >

                <FaPlus className="inline mr-2"/>

                New Chat

            </button>

        </div>

    );

}

export default NewChatButton;