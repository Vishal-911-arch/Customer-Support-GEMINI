import {

    useEffect,
    useState

} from "react";

import {

    FaBook,
    FaFilePdf,
    FaTools,
    FaShieldAlt,
    FaImage,
    FaUpload,

} from "react-icons/fa";

import ExplorerSection from "./ExplorerSection";

import {

    getKnowledge

} from "../services/api";

function KnowledgeExplorer() {

    const [knowledge, setKnowledge] = useState({

        manuals: [],
        maintenance: [],
        safety: [],
        images: [],
        uploaded: []

    });

    const [loading, setLoading] = useState(true);

    const [search, setSearch] = useState("");

    const [manualsOpen, setManualsOpen] = useState(true);

    const [maintenanceOpen, setMaintenanceOpen] = useState(false);

    const [safetyOpen, setSafetyOpen] = useState(false);

    const [imagesOpen, setImagesOpen] = useState(false);

    const [uploadedOpen, setUploadedOpen] = useState(false);

    // ==========================================
    // LOAD KNOWLEDGE
    // ==========================================

    useEffect(() => {

        loadKnowledge();

    }, []);

    async function loadKnowledge() {

        try {

            const data = await getKnowledge();

            setKnowledge(data);

        }

        catch (err) {

            console.error(err);

        }

        finally {

            setLoading(false);

        }

    }

    // ==========================================
    // FILTER
    // ==========================================

    function filter(items) {

        if (!search)

            return items;

        return items.filter(item =>

            item.name

                .toLowerCase()

                .includes(

                    search.toLowerCase()

                )

        );

    }

    // ==========================================
    // OPEN FILE
    // ==========================================

    function openDocument(item) {

        console.log(item);

        // Next:
        // Open preview drawer

    }

    // ==========================================
    // UI
    // ==========================================

    return (

        <div className="border-t border-slate-700">

            {/* HEADER */}

            <div className="px-4 pt-4">

                <div className="flex items-center gap-2 font-semibold text-white">

                    <FaBook className="text-cyan-400" />

                    Knowledge Explorer

                </div>

                <div className="text-xs text-gray-400 mt-1">

                    Browse indexed documents

                </div>

            </div>



            {

                loading ?

                    (

                        <div className="p-4 text-gray-400">

                            Loading...

                        </div>

                    )

                    :

                    (

                        <div

                            className="
                                mt-3
                                px-2
                                max-h-[320px]
                                overflow-y-auto
                                sidebar-scroll
                            "

                        >

                            <ExplorerSection

                                title="Manuals"

                                icon={<FaFilePdf />}

                                items={filter(

                                    knowledge.manuals

                                )}

                                isOpen={manualsOpen}

                                onToggle={()=>

                                    setManualsOpen(

                                        !manualsOpen

                                    )

                                }

                                onSelect={openDocument}

                            />

                            <ExplorerSection

                                title="Maintenance"

                                icon={<FaTools />}

                                items={filter(

                                    knowledge.maintenance

                                )}

                                isOpen={maintenanceOpen}

                                onToggle={()=>

                                    setMaintenanceOpen(

                                        !maintenanceOpen

                                    )

                                }

                                onSelect={openDocument}

                            />

                            <ExplorerSection

                                title="Safety"

                                icon={<FaShieldAlt />}

                                items={filter(

                                    knowledge.safety

                                )}

                                isOpen={safetyOpen}

                                onToggle={()=>

                                    setSafetyOpen(

                                        !safetyOpen

                                    )

                                }

                                onSelect={openDocument}

                            />

                            <ExplorerSection

                                title="Images"

                                icon={<FaImage />}

                                items={filter(

                                    knowledge.images

                                )}

                                isOpen={imagesOpen}

                                onToggle={()=>

                                    setImagesOpen(

                                        !imagesOpen

                                    )

                                }

                                showPages={false}

                                onSelect={openDocument}

                            />

                            <ExplorerSection

                                title="Uploaded"

                                icon={<FaUpload />}

                                items={filter(

                                    knowledge.uploaded

                                )}

                                isOpen={uploadedOpen}

                                onToggle={()=>

                                    setUploadedOpen(

                                        !uploadedOpen

                                    )

                                }

                                showPages={false}

                                onSelect={openDocument}

                            />

                        </div>

                    )

            }

        </div>

    );

}

export default KnowledgeExplorer;