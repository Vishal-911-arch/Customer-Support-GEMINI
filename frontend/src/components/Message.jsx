import SourceCard from "./SourceCard";

function Message({ message }) {

    const isUser = message.role === "user";

    return (

        <div
            className={`w-full flex ${
                isUser ? "justify-end" : "justify-start"
            } mb-6`}
        >

            <div
                className={`max-w-4xl rounded-xl px-5 py-4 whitespace-pre-wrap ${
                    isUser
                        ? "bg-cyan-600 text-white"
                        : "bg-slate-800 text-gray-100"
                }`}
            >

                {/* Message */}

                <div>{message.content}</div>

                {/* Sources */}

                {!isUser &&
                    message.sources &&
                    message.sources.length > 0 && (

                    <div className="mt-4">

                        <h4 className="text-cyan-400 font-semibold mb-3">
                            Sources
                        </h4>

                        {message.sources.map((src, i) => (

                            <SourceCard
                                key={i}
                                source={src}
                            />

                        ))}

                    </div>

                )}

                {/* Graph */}

                {!isUser &&
                    message.graph && (

                    <div className="mt-5 p-4 rounded-lg border border-cyan-600 bg-slate-900">

                        <h4 className="text-cyan-400 font-semibold mb-2">

                            Graph Analysis

                        </h4>

                        <p>

                            <strong>Title :</strong>

                            {" "}

                            {message.graph.title}

                        </p>

                        <p>

                            <strong>X Axis :</strong>

                            {" "}

                            {message.graph.x_axis}

                        </p>

                        <p>

                            <strong>Y Axis :</strong>

                            {" "}

                            {message.graph.y_axis}

                        </p>

                        <p className="mt-3">

                            {message.graph.summary}

                        </p>

                    </div>

                )}

                {/* Figure */}

                {!isUser &&
                    message.figure && (

                    <div className="mt-5 p-4 rounded-lg border border-cyan-600 bg-slate-900">

                        <h4 className="text-cyan-400 font-semibold mb-2">

                            Figure Information

                        </h4>

                        <p>

                            <strong>{message.figure.title}</strong>

                        </p>

                        <p className="mt-2">

                            {message.figure.description}

                        </p>

                    </div>

                )}

            </div>

        </div>

    );

}

export default Message;