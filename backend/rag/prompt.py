class PromptBuilder:
    """
    Builds a multimodal prompt using

    - PDF text
    - OCR text
    - Vision descriptions
    """

    MAX_CONTEXT_CHARS = 3000

    # --------------------------------------------------

    def build_prompt(
        self,
        question,
        retrieved_results,
        vision_context=None,
        linked_context="",
        graph_context=""
    ):

        documents = retrieved_results["documents"][0]
        metadatas = retrieved_results["metadatas"][0]

        context = ""
        length = 0

        # ---------------------------------------------
        # TEXT CONTEXT
        # ---------------------------------------------

        for doc, meta in zip(documents, metadatas):

            chunk = (
                f"[Document : {meta['filename']} | "
                f"Page : {meta['page']} | "
                f"Type : {meta.get('type', 'pdf')}]\n"
                f"{doc.strip()}\n\n"
            )

            if length + len(chunk) > self.MAX_CONTEXT_CHARS:
                break

            context += chunk
            length += len(chunk)

        # ---------------------------------------------
        # VISION CONTEXT
        # ---------------------------------------------

        vision_text = ""

        if vision_context:

            vision_text += "\n\n========== IMAGE ANALYSIS ==========\n\n"

            for page in vision_context:

                vision_text += (
                    f"\nDocument : {page['document']}"
                    f"\nPage : {page['page']}\n"
                )

                for image in page["images"]:

                    vision_text += (
                        f"\n[{image['type'].upper()}]\n"
                        f"{image['description']}\n"
                    )

        # ---------------------------------------------
        # FINAL PROMPT
        # ---------------------------------------------

        prompt = f"""
You are an aerospace engineering assistant.

Use ONLY the provided context.

Follow these formatting rules exactly:
- Write the answer in clean Markdown.
- Use bold section headings.
- Keep the tone clear, professional, and GPT-like.
- Use short paragraphs and bullet points where helpful.
- Do not write in all caps.
- Do not add unnecessary filler.
- If information is missing, say so clearly.
- Do not invent numerical values.

Priority of information:

1. Graph Context
2. Linked Context
3. Document Context
4. Vision Analysis

------------------------------------------------

QUESTION

{question}

------------------------------------------------

GRAPH CONTEXT

{graph_context}

------------------------------------------------

LINKED CONTEXT

{linked_context}

------------------------------------------------

DOCUMENT CONTEXT

{context}

------------------------------------------------

VISION ANALYSIS

{vision_text}

------------------------------------------------

Return the answer in exactly this format:

**Direct Answer**

<one short direct response>

**Engineering Explanation**

<clear explanation with bullets if needed>

**References Used**

- <document name and page>
- <document name and page>

If no references are available, write:
- Not available from the provided context
"""
        return prompt

    # --------------------------------------------------

    def build_graph_prompt(
        self,
        question,
        graph
    ):

        return f"""
You are an aerospace engineering assistant.

Answer ONLY using the graph below.

Follow these formatting rules exactly:
- Write the answer in clean Markdown.
- Use bold section headings.
- Keep the tone clear, professional, and GPT-like.
- Use short paragraphs and bullet points where helpful.
- Do not invent numerical values.
- Always mention the graph title.
- If information is unavailable, say so clearly.

===========================
GRAPH
===========================

Title:
{graph.get("title", "")}

Domain:
{graph.get("engineering_domain", "")}

X Axis:
{graph.get("x_axis", "")}

Y Axis:
{graph.get("y_axis", "")}

Summary:

{graph.get("llm_summary", "")}

===========================

User Question

{question}

===========================

Return the answer in exactly this format:

**Direct Answer**

<short direct response>

**Engineering Explanation**

<clear explanation of the graph>

**References Used**

- Graph title: <title>
- Graph page/context if available

If the answer is not in the graph, write:

**Direct Answer**

I couldn't find that information in this graph.
"""