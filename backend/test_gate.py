from rag.vision_gate import VisionGate

gate = VisionGate()

questions = [

    "What is stall speed?",

    "Explain Figure 3-22",

    "What is shown in Figure 4-1?",

    "Describe this diagram",

    "Explain adverse yaw",

    "Analyze the graph"

]

for q in questions:

    print(q)

    print(gate.requires_vision(q))

    print("-"*40)