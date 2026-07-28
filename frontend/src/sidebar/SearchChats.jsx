import { FaSearch } from "react-icons/fa";

function SearchChats() {

    return (

        <div className="px-4 mb-3">

            <div className="
                flex
                items-center
                gap-3
                bg-slate-700
                rounded-xl
                px-4
                py-3
            ">

                <FaSearch className="text-slate-400"/>

                <input

                    placeholder="Search chats..."

                    className="
                        flex-1
                        bg-transparent
                        outline-none
                        text-sm
                    "

                />

            </div>

        </div>

    );

}

export default SearchChats;